# Generated by Django 5.0.6 on 2025-01-04 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_userimage_file_size_userimage_file_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userimage',
            name='image_name',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
