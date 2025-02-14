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

    def __str__(self):
        return f"{self.user.username}'s image - {self.image_name}"

    def save(self, *args, **kwargs):
        if self.image and not self.id:  # Only convert on new uploads
            # Open the image
            img = Image.open(self.image)
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')

            # Save as PNG
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            file_name = f"{Path(self.image.name).stem}.png"

            # Save the converted image
            self.image.save(file_name, ContentFile(buffer.getvalue()), save=False)
            self.image_name = file_name
            self.file_type = 'png'
            self.file_size = self.image.size

        super().save(*args, **kwargs)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    social_links = models.JSONField(default=dict, blank=True)

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
    user_image = models.ForeignKey('UserImage', on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True, db_index=True)
    allowed_emails = models.JSONField(default=list, blank=True)
    requires_password = models.BooleanField(default=False)
    password = models.CharField(max_length=128, null=True, blank=True)

    allow_download = models.BooleanField(default=False)
    max_views = models.IntegerField(default=0)
    current_views = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_urlsafe(32)

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

class AccessLog(models.Model):
    image_access = models.ForeignKey(ImageAccess, on_delete=models.CASCADE)
    email = models.EmailField()
    ip_address = models.GenericIPAddressField()
    accessed_at = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=True)


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

# SIGNALS


from django.db.models.signals import post_save
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
