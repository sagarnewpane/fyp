from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import UserImage, UserProfile, WatermarkSettings, AIProtectionSettings
from django.contrib.auth.hashers import make_password
from django.urls import reverse

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



from django.urls import reverse

class UserImageListSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = UserImage
        fields = ['id', 'image_url', 'image_name', 'file_size', 'file_type', 'created_at',
                 'watermark_enabled', 'hidden_watermark_enabled', 'metadata_enabled',
                 'ai_protection_enabled', 'access_control_enabled']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if request:
            if obj.encryption_key and obj.encryption_params:
                # Return URL to decryption view for encrypted images
                return request.build_absolute_uri(
                    reverse('serve_decrypted_image', args=[obj.id])
                )
            # If not encrypted, return direct URL
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url


class SpecificImageSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    file_size = serializers.SerializerMethodField()
    file_type = serializers.CharField()     # Add this
    security = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()


    class Meta:
        model = UserImage
        fields = ['id', 'image_url', 'image_name', 'created_at', 'file_size', 'file_type', 'security']  # Include new fields

    def get_created_at(self, obj):
        return obj.created_at.strftime("%B %d, %Y %I:%M %p")

    def get_security(self, obj):
        return {
            'access_control': obj.access_control_enabled,
            'watermark': obj.watermark_enabled,
            'hidden_watermark': obj.hidden_watermark_enabled,
            'metadata': obj.metadata_enabled,
            'ai_protection': obj.ai_protection_enabled
        }

    def get_image_url(self, obj):
        request = self.context.get('request')
        if request:
            if obj.encryption_key and obj.encryption_params:
                # Return URL to decryption view for encrypted images
                return request.build_absolute_uri(
                    reverse('serve_decrypted_image', args=[obj.id])
                )
            # If not encrypted, return direct URL
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url


    def get_file_size(self, obj):
        return self._format_file_size(obj.file_size)

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

class NotificationSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'notify_on_access_request',
            'notify_on_download',
            'notify_on_successful_access',
            'notify_on_failed_access'
        ]

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


from rest_framework import serializers
from .models import ImageAccess

class ImageAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageAccess
        fields = [
            'id',
            'access_name',
            'user_image',
            'token',
            'allowed_emails',
            'requires_password',
            'password',
            'allow_download',
            'max_views',
            'current_views',
            'protection_features',
            'created_at'
        ]
        read_only_fields = ['id', 'token', 'current_views', 'created_at']
        extra_kwargs = {
            'password': {'write_only': True},
            'access_name': {'required': False}
        }

    def create(self, validated_data):
        # Handle password hashing if password is provided
        password = validated_data.pop('password', None)
        instance = super().create(validated_data)
        if password:
            instance.password = make_password(password)
            instance.save()
        return instance

class AccessVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(required=False)

class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()




from rest_framework import serializers
from .models import AccessLog

class AccessLogSerializer(serializers.ModelSerializer):
    image_name = serializers.SerializerMethodField()
    image_id = serializers.SerializerMethodField()
    action_type = serializers.CharField()
    accessed_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    location = serializers.SerializerMethodField()
    protection_features = serializers.SerializerMethodField()
    access_rule_name = serializers.SerializerMethodField()

    class Meta:
        model = AccessLog
        fields = [
            'id',
            'email',
            'ip_address',
            'country',
            'region',
            'city',
            'accessed_at',
            'action_type',
            'success',
            'image_id',
            'image_name',
            'location',
            'protection_features',
            'access_rule_name'
        ]

    def get_image_name(self, obj):
        try:
            if obj.image_access and obj.image_access.user_image:
                return obj.image_access.user_image.image_name
            # Fall back to stored value if relation is broken
            return obj.image_name
        except AttributeError:
            return obj.image_name or None

    def get_image_id(self, obj):
        try:
            if obj.image_access and obj.image_access.user_image:
                return obj.image_access.user_image.id
            # Fall back to stored value
            return obj.image_id
        except AttributeError:
            return obj.image_id or None

    def get_location(self, obj):
        location_parts = []
        if obj.city:
            location_parts.append(obj.city)
        if obj.region:
            location_parts.append(obj.region)
        if obj.country:
            location_parts.append(obj.country)
        return ", ".join(filter(None, location_parts))

    def get_protection_features(self, obj):
        try:
            if obj.image_access:
                return obj.image_access.protection_features
            # Return empty dict for preserved logs
            return {}
        except AttributeError:
            return {}

    def get_access_rule_name(self, obj):
        try:
            if obj.image_access:
                return obj.image_access.access_name
            # Fall back to stored access rule name
            return obj.access_rule_name
        except AttributeError:
            return obj.access_rule_name or "Deleted Access Rule"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Format action type for display
        data['action_type'] = instance.action_type.replace('_', ' ').title()
        return data


class MetadataSerializer(serializers.Serializer):
    basic = serializers.DictField(required=False)
    exif = serializers.DictField(required=False)
    iptc = serializers.DictField(required=False)
    xmp = serializers.DictField(required=False)
    copyright = serializers.DictField(required=False)

class ImageMetadataSerializer(serializers.ModelSerializer):
    metadata = serializers.SerializerMethodField()
    raw_metadata = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%B %d, %Y %I:%M %p")

    class Meta:
        model = UserImage
        fields = ['id', 'image_name', 'created_at', 'file_size', 'file_type', 'metadata', 'raw_metadata']

    def get_metadata(self, obj):
        if obj.metadata:
            return obj.metadata.get('categorized', {})
        return {}

    def get_raw_metadata(self, obj):
        if obj.metadata:
            return obj.metadata.get('raw', {})
        return {}


from .models import AccessRequest

class AccessRequestSerializer(serializers.ModelSerializer):
    image_name = serializers.SerializerMethodField()
    image_id = serializers.SerializerMethodField()

    class Meta:
        model = AccessRequest
        fields = ['id', 'email', 'message', 'status', 'created_at', 'image_name', 'image_id']
        read_only_fields = ['id', 'status', 'created_at']

    def get_image_name(self, obj):
        return obj.image_access.user_image.image_name if obj.image_access.user_image else "Unknown"

    def get_image_id(self, obj):
        return obj.image_access.user_image.id if obj.image_access.user_image else None

class AIProtectionSettingsSerializer(serializers.ModelSerializer):
    protected_image = serializers.SerializerMethodField()

    class Meta:
        model = AIProtectionSettings
        fields = ['enabled', 'protected_image']
        read_only_fields = ['protected_image']

    def get_protected_image(self, obj):
        request = self.context.get('request')
        if obj.protected_image and request:
            return request.build_absolute_uri(obj.protected_image.url)
        return None if not obj.protected_image else obj.protected_image.url
