# Generated by Django 5.1.5 on 2025-02-16 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0012_imageaccess_protection_features'),
    ]

    operations = [
        migrations.AddField(
            model_name='imageaccess',
            name='protected_image',
            field=models.ImageField(blank=True, null=True, upload_to='protected_images/'),
        ),
    ]
