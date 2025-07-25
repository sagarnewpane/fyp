# Generated by Django 5.1.7 on 2025-04-06 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0020_remove_userimage_encryption_perms_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userimage',
            name='encryption_key',
        ),
        migrations.RemoveField(
            model_name='userimage',
            name='perms',
        ),
        migrations.RemoveField(
            model_name='userimage',
            name='xor_streams',
        ),
        migrations.AddField(
            model_name='userimage',
            name='encryption_perms',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name='userimage',
            name='encryption_xor_streams',
            field=models.JSONField(blank=True, default=list),
        ),
    ]
