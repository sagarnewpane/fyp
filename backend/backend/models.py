from django.db import models
from django.contrib.auth.models import User
from pathlib import Path
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    if user_image.ai_protection_enabled != instance.enabled:
        user_image.ai_protection_enabled = instance.enabled
        user_image.save(update_fields=['ai_protection_enabled'])  # Prevent infinite loop
