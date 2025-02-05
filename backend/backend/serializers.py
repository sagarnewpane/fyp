from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import UserImage, UserProfile, WatermarkSettings

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'email': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            User.objects.get(email=value)
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("No user found with this email address.")

class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    uidb64 = serializers.CharField()
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

class UserImageSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = UserImage
        fields = ['id', 'image', 'created_at', 'access_control_enabled',
                 'watermark_enabled', 'metadata_enabled', 'ai_protection_enabled']
        read_only_fields = ['created_at']

    def get_created_at(self, obj):
        # Format: "January 3, 2025 5:44 PM"
        return obj.created_at.strftime("%B %d, %Y %I:%M %p")



class UserImageListSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    file_size = serializers.IntegerField()  # Add this
    file_type = serializers.CharField()     # Add this

    class Meta:
        model = UserImage
        fields = ['id', 'image_url', 'image_name', 'created_at', 'file_size', 'file_type']  # Include new fields

    def get_image_url(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None

    def get_created_at(self, obj):
        return obj.created_at.strftime("%B %d, %Y %I:%M %p")


class SpecificImageSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    file_size = serializers.IntegerField()  # Add this
    file_type = serializers.CharField()     # Add this
    security = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    # dimensions = serializers.SerializerMethodField()


    class Meta:
        model = UserImage
        fields = ['id', 'image_url', 'image_name', 'created_at', 'file_size', 'file_type', 'security']  # Include new fields

    def get_created_at(self, obj):
        return obj.created_at.strftime("%B %d, %Y %I:%M %p")

    def get_security(self, obj):
        return {
            'access_control': obj.access_control_enabled,
            'watermark': obj.watermark_enabled,
            'metadata': obj.metadata_enabled,
            'ai_protection': obj.ai_protection_enabled
        }
        # def get_dimensions(self, obj):
        #     try:
        #         metadata = obj.metadata
        #         return {
        #             'width': metadata.width,
        #             'height': metadata.height
        #         }
        #     except ImageMetadata.DoesNotExist:
        #         return None

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

    def _format_file_size(self, size_in_bytes):
        # Convert bytes to human readable format
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_in_bytes < 1024:
                return f"{size_in_bytes:.2f} {unit}"
            size_in_bytes /= 1024
        return f"{size_in_bytes:.2f} TB"


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'website', 'twitter', 'instagram']

class UserProfileUpdateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    first_name = serializers.CharField(max_length=150, required=False, allow_blank=True)  # Made optional
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)   # Made optional
    email = serializers.EmailField()
    social_links = serializers.JSONField(required=False, default=dict)

    def validate_username(self, value):
        """
        Check that the username is unique (except for current user)
        """
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def validate_email(self, value):
        """
        Check that the email is unique (except for current user)
        """
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def update(self, instance, validated_data):
        # Update User model fields
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        # Update or create UserProfile
        profile, created = UserProfile.objects.get_or_create(user=instance)
        if 'social_links' in validated_data:
            profile.social_links = validated_data['social_links']
            profile.save()

        return instance

# Passwod Updatation
class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    confirm_password = serializers.CharField(required=True)

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")
        return value

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Password fields didn't match."})
        return data

class WatermarkSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatermarkSettings
        fields = ['enabled', 'settings']

    def validate_settings(self, value):
        # Add any validation if needed
        return value


from rest_framework import serializers
from .models import InvisibleWatermarkSettings

class InvisibleWatermarkSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvisibleWatermarkSettings
        fields = ['enabled', 'text', 'embedded_image']
        read_only_fields = ['embedded_image']
