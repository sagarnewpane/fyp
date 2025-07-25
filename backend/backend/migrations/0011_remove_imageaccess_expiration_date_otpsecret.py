# Generated by Django 5.1.5 on 2025-02-14 04:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0010_remove_imageaccess_allow_sharing_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imageaccess',
            name='expiration_date',
        ),
        migrations.CreateModel(
            name='OTPSecret',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('secret', models.CharField(max_length=32)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_used', models.BooleanField(default=False)),
                ('image_access', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.imageaccess')),
            ],
        ),
    ]
