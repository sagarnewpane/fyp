from django.db import models
from django.contrib.auth.models import User
from pathlib import Path

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
        if self.image:
            # Set the image name from the uploaded file
            self.image_name = Path(self.image.name).name
            # Set the file size
            self.file_size = self.image.size
            # Set the file type
            self.file_type = Path(self.image.name).suffix[1:].lower()  # Remove the dot from extension
        super().save(*args, **kwargs)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    website = models.URLField(max_length=200, blank=True)
    twitter = models.CharField(max_length=100, blank=True)
    instagram = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
