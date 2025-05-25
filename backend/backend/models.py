from django.db import models
from django.contrib.auth.models import User
from pathlib import Path
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
import secrets

from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from .metadata_utils import MetadataExtractor
import time

class UserImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='uploads/')
    image_name = models.CharField(max_length=255, blank=True)  # Remove default
    file_size = models.IntegerField(default=0)  # in bytes
    file_type = models.CharField(max_length=10, default='unknown')
    created_at = models.DateTimeField(auto_now_add=True)

    # Protection status fields
    access_control_enabled = models.BooleanField(default=False)
    watermark_enabled = models.BooleanField(default=False)
    hidden_watermark_enabled = models.BooleanField(default=False)
    metadata_enabled = models.BooleanField(default=False)
    ai_protection_enabled = models.BooleanField(default=False)

    metadata = models.JSONField(default=dict, blank=True)

    encryption_key = models.CharField(max_length=255, blank=True, null=True)
    encryption_params = models.JSONField(default=dict, blank=True)  # To store permutation and XOR streams

    def __str__(self):
        return f"{self.user.username}'s image - {self.image_name}"

    def save(self, *args, **kwargs):
        new_upload = not self.id  # Check if it's a new upload

        # For new uploads with an image
        if new_upload and self.image:
            # First save to get an ID and save the original image file
            super().save(*args, **kwargs)

            # Now we can access the image path
            image_path = self.image.path
            print('IMAGE NAME',self.image.name)

            # Extract metadata as before
            try:
                self.metadata = MetadataExtractor.extract_metadata(image_path)
                self.metadata_enabled = True
            except Exception as e:
                print(f"Metadata extraction failed: {str(e)}")
                self.metadata = {}
                self.metadata_enabled = False

            # Generate encryption key with improved randomness
            import hashlib
            import secrets
            import time
            import os
            import random

            salt = secrets.token_hex(8)
            current_time = str(time.time())
            random_num = str(random.randint(100000, 999999999))
            process_id = str(os.getpid())

            # Generate a secure key for AES encryption
            encryption_key = hashlib.sha256(
                f"{self.user.id}:{self.id}:{salt}:{current_time}:{random_num}:{process_id}".encode()
            ).digest()[:32]  # Use binary digest for AES, only need 32 bytes

            # Store hex string of key in database
            self.encryption_key = encryption_key.hex()

            # Encrypt the image using AES
            from .encryption import encrypt_aes_cbc

            # Read the original file
            with open(image_path, 'rb') as f:
                original_data = f.read()

            # Encrypt the data
            encrypted_data = encrypt_aes_cbc(original_data, encryption_key)

            # Save the encrypted file
            import tempfile
            from django.core.files.base import ContentFile
            from pathlib import Path

            file_name = f"{Path(self.image.name).stem}.enc"
            print('FILE NAME',file_name)

            # Replace the original file with the encrypted version
            self.image.save(file_name, ContentFile(encrypted_data), save=False)

            os.remove(image_path)

            # Update other fields
            self.image_name = Path(file_name).stem
            self.file_type = 'png'  # Custom file type for encrypted files
            self.file_size = self.image.size

            # No need to store permutation params for AES
            self.encryption_params = {
                'algorithm': 'AES-CBC',
                'key_length': len(encryption_key) * 8  # in bits
            }

            # Save the changes with update_fields
            super().save(update_fields=[
                'metadata', 'metadata_enabled', 'encryption_key', 'encryption_params',
                'image', 'image_name', 'file_type', 'file_size'
            ])
        else:
            # For updates or records without images, just save normally
            super().save(*args, **kwargs)
    def get_decrypted_image(self):
        """Return the decrypted image as a numpy array"""
        try:
            if not self.encryption_key or not self.encryption_params:
                # If not encrypted, just read the image directly
                import cv2
                print(f"Reading unencrypted image at {self.image.path}")
                img = cv2.imread(self.image.path)
                if img is None:
                    raise ValueError(f"Failed to read image at {self.image.path}")
                return img

            # Read the encrypted image file
            with open(self.image.path, 'rb') as f:
                encrypted_data = f.read()

            # Convert hex encryption key to bytes
            encryption_key = bytes.fromhex(self.encryption_key)

            # Decrypt the data using AES
            from .encryption import decrypt_aes_cbc
            decrypted_data = decrypt_aes_cbc(encrypted_data, encryption_key)

            # Convert decrypted bytes to numpy array for OpenCV
            import cv2
            import numpy as np

            # Create in-memory file-like object
            import io
            buffer = io.BytesIO(decrypted_data)

            # Decode image from memory buffer
            image_array = np.asarray(bytearray(buffer.read()), dtype=np.uint8)
            img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

            if img is None:
                raise ValueError("Failed to decode decrypted image data")

            return img

        except Exception as e:
            print(f"Error in get_decrypted_image: {type(e).__name__}: {str(e)}")
            import traceback
            print(traceback.format_exc())
            raise

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    social_links = models.JSONField(default=dict, blank=True)

    # Notification Preferences
    notify_on_access_request = models.BooleanField(default=True)
    notify_on_download = models.BooleanField(default=True)
    notify_on_successful_access = models.BooleanField(default=True)
    notify_on_failed_access = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

# Signal to create/update UserProfile when User is created/updated

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.profile.save()


class WatermarkSettings(models.Model):
    user_image = models.OneToOneField(
        UserImage,
        on_delete=models.CASCADE,
        related_name='watermark_settings'
    )
    enabled = models.BooleanField(default=False)
    settings = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def get_default_settings(cls, user_image=None):
        """
        Get default watermark settings.
        If user_image is provided, use its user's username in the watermark.
        """
        return {
            "text": f"© {user_image.user.username}" if user_image else "© Protected Image",
            "font": "Arial",
            "color": "#000000",
            "fontSize": 24,
            "opacity": 50,
            "rotation": 45,
            "pattern": "tiled",
            "spacing": 50,
            "horizontalOffset": 0,
            "verticalOffset": 0
        }

    def save(self, *args, **kwargs):
        if not self.settings:
            self.settings = self.get_default_settings(self.user_image)
        super().save(*args, **kwargs)

class InvisibleWatermarkSettings(models.Model):
    user_image = models.OneToOneField(
        UserImage,
        on_delete=models.CASCADE,
        related_name='invisible_watermark_settings'
    )
    enabled = models.BooleanField(default=False)
    embedded_image = models.ImageField(upload_to='uploads/stegnated', null=True, blank=True)
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

from django.contrib.auth.hashers import make_password, check_password as django_check_password

class ImageAccess(models.Model):

    access_name = models.CharField(max_length=255, default='')
    user_image = models.ForeignKey('UserImage', on_delete=models.CASCADE, related_name='access_rules')
    token = models.CharField(max_length=64, unique=True, db_index=True)
    allowed_emails = models.JSONField(default=list, blank=True)
    requires_password = models.BooleanField(default=False)
    password = models.CharField(max_length=128, null=True, blank=True)

    allow_download = models.BooleanField(default=False)
    max_views = models.IntegerField(default=0)
    current_views = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    protection_features = models.JSONField(default=dict, blank=True)
    protected_image = models.ImageField(upload_to='protected_images/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_urlsafe(32)

        if not self.protection_features:
            self.protection_features = {
                'watermark': False,
                'hidden_watermark': False,
                'metadata': False,
                'ai_protection': False
            }

        # Hash password if it's provided and changed
        if self.requires_password and self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)

        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        """Check if the provided password matches the stored hash"""
        if self.password:
            return django_check_password(raw_password, self.password)
        return False

    def is_valid(self):
        if self.max_views > 0 and self.current_views >= self.max_views:
            return False
        return True

from django.db import models
from django.utils import timezone
from datetime import timedelta

class OTPSecret(models.Model):
    image_access = models.ForeignKey('ImageAccess', on_delete=models.CASCADE)
    email = models.EmailField()
    secret = models.CharField(max_length=32)  # For storing pyotp secret
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        # Check if secret is not expired (5 minutes validity) and not used
        expiry_time = self.created_at + timedelta(minutes=5)
        return not self.is_used and timezone.now() <= expiry_time



class AccessLog(models.Model):
    image_access = models.ForeignKey(ImageAccess, on_delete=models.SET_NULL, null=True)

    # Fields to store information that would be lost on deletion
    image_id = models.IntegerField(null=True, blank=True)
    image_name = models.CharField(max_length=255, null=True, blank=True)
    access_rule_token = models.CharField(max_length=64, null=True, blank=True)
    access_rule_name = models.CharField(max_length=255, null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    username = models.CharField(max_length=150, null=True, blank=True)

    email = models.EmailField()
    ip_address = models.GenericIPAddressField(null=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    accessed_at = models.DateTimeField(auto_now_add=True)
    action_type = models.CharField(max_length=20, choices=[
        ('VIEW', 'Viewed'),
        ('DOWNLOAD', 'Downloaded'),
        ('ATTEMPT', 'Access Attempt')
    ])
    success = models.BooleanField(default=False)

    class Meta:
        ordering = ['-accessed_at']

    def __str__(self):
        return f"{self.email} - {self.action_type} - {self.accessed_at}"


class AccessRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied')
    ]

    image_access = models.ForeignKey('ImageAccess', on_delete=models.CASCADE, related_name='access_requests')
    email = models.EmailField()
    message = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('image_access', 'email')  # Prevent duplicate requests

    def __str__(self):
        return f"{self.email} - {self.status} - {self.image_access.token}"

# SIGNALS


from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

@receiver(post_save, sender=WatermarkSettings)
def update_user_image_watermark(sender, instance, **kwargs):
    """Sync UserImage when WatermarkSettings.enabled is changed"""
    user_image = instance.user_image
    if user_image.watermark_enabled != instance.enabled:
        user_image.watermark_enabled = instance.enabled
        user_image.save(update_fields=['watermark_enabled'])  # Prevent infinite loop

@receiver(post_save, sender=InvisibleWatermarkSettings)
def update_user_image_ai_protection(sender, instance, **kwargs):
    """Sync UserImage when InvisibleWatermarkSettings.enabled is changed"""
    user_image = instance.user_image
    if user_image.hidden_watermark_enabled != instance.enabled:
        user_image.hidden_watermark_enabled = instance.enabled
        user_image.save(update_fields=['hidden_watermark_enabled'])  # Prevent infinite loop


@receiver([post_save, post_delete], sender=ImageAccess)
def update_access_control_status(sender, instance, **kwargs):
    image = instance.user_image
    has_access_rules = ImageAccess.objects.filter(user_image=image).exists()  # Changed this line
    if image.access_control_enabled != has_access_rules:
        image.access_control_enabled = has_access_rules
        image.save(update_fields=['access_control_enabled'])

from django.db.models.signals import pre_delete
@receiver(pre_delete, sender=ImageAccess)
def store_access_rule_info_before_delete(sender, instance, **kwargs):
    """Preserve information from ImageAccess before it gets deleted"""
    try:
        # Get all related access logs
        access_logs = AccessLog.objects.filter(image_access=instance)

        # Store relevant info
        access_logs.update(
            access_rule_token=instance.token,
            access_rule_name=instance.access_name,
            image_id=instance.user_image.id if instance.user_image else None,
            image_name=instance.user_image.image_name if instance.user_image else None,
            user_id=instance.user_image.user.id if instance.user_image and instance.user_image.user else None,
            username=instance.user_image.user.username if instance.user_image and instance.user_image.user else None
        )
    except Exception as e:
        print(f"Error preserving access log data: {str(e)}")

class AIProtectionSettings(models.Model):
    user_image = models.OneToOneField(UserImage, on_delete=models.CASCADE, related_name='ai_protection')
    enabled = models.BooleanField(default=False)
    protected_image = models.ImageField(upload_to='ai_protected_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"AI Protection for {self.user_image.image_name}"
