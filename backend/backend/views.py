from django.contrib.auth.tokens import default_token_generator
from django.db.models.manager import QuerySet
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import RegisterUserSerializer, PasswordResetRequestSerializer, PasswordResetConfirmSerializer, SpecificImageSerializer, UserImageSerializer, UserImageListSerializer, PasswordChangeSerializer, OTPVerificationSerializer, AIProtectionSettingsSerializer, NotificationSettingsSerializer, AccountDeletionSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .models import UserImage, WatermarkSettings, InvisibleWatermarkSettings, AIProtectionSettings, UserProfile
from rest_framework.parsers import MultiPartParser, FormParser  #


from django.http import HttpResponse, Http404
import cv2
import os
import traceback
from PIL import Image
import io
import numpy as np
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def serve_decrypted_image(request, image_id):
    """
    View that decrypts and serves an image in real-time
    """
    try:
        # Get the image without filtering by user first
        user_image = UserImage.objects.get(id=image_id)

        # Decrypt the image
        decrypted_img = user_image.get_decrypted_image()

        # Convert to bytes for HTTP response
        success, buffer = cv2.imencode('.png', decrypted_img)
        if not success:
            return HttpResponse("Failed to encode image", status=500)

        # Create response
        response = HttpResponse(buffer.tobytes(), content_type="image/png")
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'

        return response

    except UserImage.DoesNotExist:
        print(f"Image not found in database: {image_id}")
        raise Http404("Image not found - does not exist")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return HttpResponse(f"Error: {str(e)}", status=500)


class RegisterView(generics.CreateAPIView):
    """
    View for user registration.
    Allows any user (authenticated or not) to access this view.
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterUserSerializer

class VerifyView(generics.RetrieveAPIView):
    """
    View for verifying and retrieving current user information.
    Only authenticated users can access this view.
    Returns username and email of the currently logged in user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            'username': user.username,
            'email': user.email
        }
        return Response(data, status=status.HTTP_200_OK)


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)  # We can safely get the user here because validation already checked

            # Generate token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Create reset link
            reset_link = f"http://localhost:5173/forget-password/{uid}/{token}"

            # Send email
            send_mail(
                'Password Reset Request - Authograph',
                f'''Dear {user.username},

We received a request to reset your password for your Authograph account. To proceed with the password reset, please click the following link:

{reset_link}

This link will expire in 24 hours for security reasons.

If you did not request this password reset, please ignore this email or contact our support team if you have concerns about your account security.

Best regards,
The Authograph Team''',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            return Response(
                {"message": "Password reset email has been sent."},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request):
        print("Received data:", request.data)  # Add this line
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            print("Serializer errors:", serializer.errors)
        if serializer.is_valid():
            try:
                uid = force_str(urlsafe_base64_decode(serializer.validated_data['uidb64']))
                user = User.objects.get(pk=uid)

                if default_token_generator.check_token(user, serializer.validated_data['token']):
                    user.set_password(serializer.validated_data['new_password'])
                    user.save()
                    return Response(
                        {"message": "Password has been reset successfully."},
                        status=status.HTTP_200_OK
                    )
                return Response(
                    {"error": "Invalid token."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                return Response(
                    {"error": "Invalid reset link."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # Add these parser classes

    def post(self, request):
        # Don't copy the request data - use it directly
        serializer = UserImageSerializer(data=request.data)

        if serializer.is_valid():
            # Save the image and associate it with the user
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# class ImageListView(generics.ListAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = UserImageListSerializer

#     def get_queryset(self):
#         queryset = UserImage.objects.filter(user=self.request.user)
#         params = self.request.query_params

#         # Search filter
#         search_query = params.get('search', '')
#         if search_query:
#             queryset = queryset.filter(image_name__icontains=search_query)

#         # Date range filter
#         date_from = params.get('date_from')
#         date_to = params.get('date_to')
#         if date_from:
#             queryset = queryset.filter(created_at__gte=date_from)
#         if date_to:
#             queryset = queryset.filter(created_at__lte=date_to)

#         # File type filter
#         file_types = params.getlist('file_type')
#         if file_types:
#             queryset = queryset.filter(file_type__in=file_types)

#         # Size range filter (in MB)
#         size_min = params.get('size_min')
#         size_max = params.get('size_max')
#         if size_min:
#             queryset = queryset.filter(file_size__gte=float(size_min)*1024*1024)
#         if size_max:
#             queryset = queryset.filter(file_size__lte=float(size_max)*1024*1024)

#         # Sorting
#         sort_by = params.get('sort', '-created_at')
#         return queryset.order_by(sort_by)
class ImageListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserImageListSerializer
    pagination_class = StandardResultsSetPagination

    def get_serializer_context(self):
        """Add request to serializer context"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        queryset = UserImage.objects.filter(user=self.request.user)
        params = self.request.query_params

        # Search filter
        search_query = params.get('search', '')
        if search_query:
            queryset = queryset.filter(image_name__icontains=search_query)

        # File type filter
        file_types = params.getlist('file_type')
        if file_types:
            queryset = queryset.filter(file_type__in=file_types)

        # Size filter (in MB)
        size_min = params.get('size_min')
        size_max = params.get('size_max')
        if size_min:
            queryset = queryset.filter(file_size__gte=float(size_min)*1024*1024)  # Convert MB to bytes
        if size_max:
            queryset = queryset.filter(file_size__lte=float(size_max)*1024*1024)  # Convert MB to bytes

        # Sorting
        sort_by = params.get('sort', '-created_at')
        valid_sort_fields = [
            'created_at', '-created_at',
            'image_name', '-image_name',
            'file_size', '-file_size'
        ]
        if sort_by in valid_sort_fields:
            queryset = queryset.order_by(sort_by)

        print(queryset)

        return queryset


class UserImageView(generics.RetrieveDestroyAPIView):  # Changed to RetrieveDestroyAPIView
    """
    View for retrieving and deleting a single user image.
    Handles permissions for public/private images.
    """
    serializer_class = SpecificImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserImage.objects.filter(user=self.request.user)

    def get_object(self):
        image = super().get_object()
        if image.user != self.request.user:
            raise PermissionDenied(
                "You do not have permission to access this image."
            )
        return image

    def delete(self, request, *args, **kwargs):
        """
        Delete a specific image
        """
        try:
            image = self.get_object()

            # Delete the actual image file from storage
            if image.image:
                image.image.delete(save=False)

            # Delete the database record
            image.delete()

            return Response({
                "message": "Image successfully deleted",
                "status": "success"
            }, status=status.HTTP_204_NO_CONTENT)

        except UserImage.DoesNotExist:
            return Response({
                "message": "Image not found",
                "status": "error"
            }, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied as e:
            return Response({
                "message": str(e),
                "status": "error"
            }, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({
                "message": "An error occurred while deleting the image",
                "status": "error",
                "detail": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from rest_framework.parsers import MultiPartParser, FormParser
from .models import UserProfile
from .serializers import UserProfileSerializer, UserProfileUpdateSerializer

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        profile, created = UserProfile.objects.get_or_create(user=user)

        data = {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'avatar_url': request.build_absolute_uri(profile.avatar.url) if profile.avatar else None,
            'social_links': profile.social_links
        }
        return Response(data)

    def patch(self, request):
        serializer = UserProfileUpdateSerializer(
            request.user,
            data=request.data,
            context={'request': request},
            partial=True
        )

        if serializer.is_valid():
            try:
                serializer.save()
                return Response({
                    'message': 'Profile updated successfully',
                    'data': serializer.data
                })
            except Exception as e:
                return Response({
                    'error': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AvatarUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        profile, created = UserProfile.objects.get_or_create(user=request.user)

        if 'avatar' not in request.FILES:
            return Response({'error': 'No avatar file provided'},
                          status=status.HTTP_400_BAD_REQUEST)

        profile.avatar = request.FILES['avatar']
        profile.save()

        return Response({
            'message': 'Avatar uploaded successfully',
            'avatar_url': request.build_absolute_uri(profile.avatar.url)
        })

class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PasswordChangeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({
                "message": "Password updated successfully."
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WatermarkSettingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, image_id):
        try:
            # First, get the image and verify ownership
            user_image = UserImage.objects.get(id=image_id, user=request.user)

            try:
                # Try to get existing settings
                watermark_settings = WatermarkSettings.objects.get(user_image=user_image)
                return Response({
                    'enabled': watermark_settings.enabled,
                    **watermark_settings.settings
                })
            except WatermarkSettings.DoesNotExist:
                # If settings don't exist, return default settings
                default_settings = WatermarkSettings.get_default_settings(user_image)
                return Response({
                    'enabled': False,
                    **default_settings
                })

        except UserImage.DoesNotExist:
            return Response(
                {'error': 'Image not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    def patch(self, request, image_id):
        try:
            user_image = UserImage.objects.get(id=image_id, user=request.user)
            watermark_settings, created = WatermarkSettings.objects.get_or_create(
                user_image=user_image,
                defaults={
                    'enabled': True,
                    'settings': WatermarkSettings.get_default_settings(user_image)
                }
            )

            # Update enabled status if provided
            if 'enabled' in request.data:
                watermark_settings.enabled = request.data['enabled']

            # Update settings
            new_settings = watermark_settings.settings.copy()
            for key, value in request.data.items():
                if key != 'enabled':
                    new_settings[key] = value
            watermark_settings.settings = new_settings

            watermark_settings.save()
            return Response({
                'enabled': watermark_settings.enabled,
                **watermark_settings.settings
            })

        except UserImage.DoesNotExist:
            return Response(
                {'error': 'Image not found'},
                status=status.HTTP_404_NOT_FOUND
            )


from django.core.files.base import ContentFile
import cv2
import numpy as np
from .scripts.steg import TextSteganography
import tempfile
import os

class InvisibleWatermarkView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, image_id):
        """Create a new invisible watermark"""
        try:
            user_image = UserImage.objects.get(id=image_id, user=request.user)
            message = request.data.get('text', '')

            if not message:
                return Response({'error': 'Message is required'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if watermark already exists
            if InvisibleWatermarkSettings.objects.filter(user_image=user_image).exists():
                return Response(
                    {'error': 'Watermark already exists. Use PATCH to update.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Get decrypted image
            decrypted_img = user_image.get_decrypted_image()

            # Create a temporary file with the decrypted image
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                temp_path = temp_file.name
                # Save the numpy array as an image
                cv2.imwrite(temp_path, decrypted_img)

            stego = TextSteganography()

            try:
                stego_image = stego.embed_message(temp_path, message)

                watermark = InvisibleWatermarkSettings.objects.create(
                    user_image=user_image,
                    enabled=True,
                    text=message
                )

                with tempfile.NamedTemporaryFile(suffix='.png') as stego_temp:
                    cv2.imwrite(stego_temp.name, stego_image)
                    with open(stego_temp.name, 'rb') as f:
                        watermark.embedded_image.save(
                            f'stego_{user_image.image_name}',
                            ContentFile(f.read()),
                            save=True
                        )
                # Update hidden_watermark_enabled flag
                user_image.hidden_watermark_enabled = True
                user_image.save(update_fields=['hidden_watermark_enabled'])

                return Response({'status': 'success'})

            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)

        except UserImage.DoesNotExist:
            return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, image_id):
        """Update existing watermark text"""
        try:
            user_image = UserImage.objects.get(id=image_id, user=request.user)
            message = request.data.get('text')

            if message is None:
                return Response({'error': 'Text is required'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                watermark = InvisibleWatermarkSettings.objects.get(user_image=user_image)
            except InvisibleWatermarkSettings.DoesNotExist:
                return Response(
                    {'error': 'No watermark exists. Use POST to create one.'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Get the decrypted image
            decrypted_img = user_image.get_decrypted_image()

            # Create a temporary file with the decrypted image
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                temp_path = temp_file.name
                # Save the numpy array as an image
                cv2.imwrite(temp_path, decrypted_img)

            stego = TextSteganography()

            try:
                stego_image = stego.embed_message(temp_path, message)

                # Delete old embedded image if it exists
                if watermark.embedded_image:
                    watermark.embedded_image.delete(save=False)

                with tempfile.NamedTemporaryFile(suffix='.png') as stego_temp:
                    cv2.imwrite(stego_temp.name, stego_image)
                    with open(stego_temp.name, 'rb') as f:
                        watermark.text = message
                        watermark.embedded_image.save(
                            f'stego_{user_image.image_name}',
                            ContentFile(f.read()),
                            save=True
                        )

                return Response({'status': 'success'})

            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)

        except UserImage.DoesNotExist:
            return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def clean_extracted_text(self, text):
        """Remove null characters and trailing whitespace from extracted text"""
        if text:
            # Split on first null character and take the first part
            cleaned_text = text.split('\x00')[0]
            # Remove any trailing whitespace
            return cleaned_text.strip()
        return text

    def get(self, request, image_id):
            try:
                watermark = InvisibleWatermarkSettings.objects.get(
                    user_image_id=image_id,
                    user_image__user=request.user
                )

                if watermark.embedded_image:
                    image_array = cv2.imdecode(
                        np.frombuffer(watermark.embedded_image.read(), np.uint8),
                        cv2.IMREAD_COLOR
                    )

                    stego = TextSteganography()
                    extracted_message = stego.extract_message(image_array)
                    # Clean the extracted message
                    cleaned_message = self.clean_extracted_text(extracted_message)

                    return Response({
                        'text': cleaned_message,
                        'embedded_image': request.build_absolute_uri(watermark.embedded_image.url)
                    })
                return Response({'text': None, 'embedded_image': None})

            except InvisibleWatermarkSettings.DoesNotExist:
                return Response({'text': None, 'embedded_image': None})
            except Exception as e:
                return Response(
                    {'error': f"Error extracting watermark: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

    def delete(self, request, image_id):
        """Delete the invisible watermark"""
        try:
            watermark = InvisibleWatermarkSettings.objects.get(
                user_image_id=image_id,
                user_image__user=request.user
            )
            watermark.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except InvisibleWatermarkSettings.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from .utils import OTPHandler
import secrets
from .models import ImageAccess,AccessLog
from .serializers import ImageAccessSerializer, AccessVerificationSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .utils import ProtectionChain
import json
import cv2

# Helper function to get user profile for notification checks
def get_user_profile_for_notifications(user_id):
    try:
        user = User.objects.get(id=user_id)
        profile, _ = UserProfile.objects.get_or_create(user=user)
        return profile
    except User.DoesNotExist:
        logger.error(f"User with id {user_id} not found for notification check.")
    except Exception as e:
        logger.error(f"Error fetching UserProfile for user {user_id}: {str(e)}")
    return None

class CreateAccessView(APIView):
    def get(self, request, image_id):
            """
            Get all access rules for an image
            """
            try:
                # Verify image ownership
                user_image = UserImage.objects.get(id=image_id, user=request.user)

                # Get all access rules for the image
                access_rules = ImageAccess.objects.filter(user_image=user_image)

                rules_data = [{
                    'access_name': rule.access_name,
                    'id': rule.id,
                    'token': rule.token,
                    'allowed_emails': rule.allowed_emails,
                    'requires_password': rule.requires_password,
                    'allow_download': rule.allow_download,
                    'max_views': rule.max_views,
                    'current_views': rule.current_views,
                    'created_at': rule.created_at,
                    'protection_features': rule.protection_features,
                    'is_valid': rule.is_valid()
                } for rule in access_rules]

                return Response({
                    'rules': rules_data,
                    'total_count': len(rules_data)
                })

            except UserImage.DoesNotExist:
                return Response({
                    'error': 'Image not found or unauthorized access'
                }, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({
                    'error': f'Failed to fetch access rules: {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, image_id):
        try:
            # Verify image ownership
            user_image = UserImage.objects.get(id=image_id, user=request.user)

            # Create data dictionary with all required fields
            access_data = {
                'user_image': user_image.id,
                'access_name': request.data['access_name'],
                'allowed_emails': request.data.get('allowed_emails', []),
                'requires_password': request.data.get('requires_password', False),
                'password': request.data.get('password'),
                'allow_download': request.data.get('allow_download', False),
                'max_views': request.data.get('max_views', 0),
                'protection_features': request.data.get('protection_features', {})
            }

            # Validate and save using serializer
            serializer = ImageAccessSerializer(data=access_data)
            if serializer.is_valid():
                access_rule = serializer.save()

                # Create protected version of the image if protection features are specified
                if access_data['protection_features']:
                    protected_image = ProtectionChain.create_protected_image(
                        user_image,
                        access_data['protection_features'],
                        access_rule
                    )
                    # if protected_image:
                    #     access_rule.protected_image = protected_image
                    #     access_rule.save()

                return Response({
                    'status': 'success',
                    'access_rule': {
                        'id': access_rule.id,
                        'token': access_rule.token,
                        'allowed_emails': access_rule.allowed_emails,
                        'requires_password': access_rule.requires_password,
                        'allow_download': access_rule.allow_download,
                        'max_views': access_rule.max_views,
                        'protection_features': access_rule.protection_features,
                        'created_at': access_rule.created_at
                    }
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'error': 'Invalid data',
                    'details': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

        except UserImage.DoesNotExist:
            return Response({
                'error': 'Image not found or unauthorized access'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _validate_protection_features(self, user_image, features):
        """Validate that requested protection features are available"""
        if features.get('watermark') and not user_image.watermark_enabled:
            return False
        if features.get('hidden_watermark') and not user_image.hidden_watermark_enabled:
            return False
        if features.get('ai_protection') and not user_image.ai_protection_enabled:
            return False
        if features.get('metadata') and not user_image.metadata_enabled:
            return False
        return True


    def delete(self, request, image_id, rule_id=None):
            """Delete an access rule"""
            try:
                # First verify image ownership
                user_image = UserImage.objects.get(id=image_id, user=request.user)

                if rule_id:
                    # Delete specific access rule
                    try:
                        access_rule = ImageAccess.objects.get(
                            id=rule_id,
                            user_image=user_image
                        )

                        # Delete the protected image file if it exists
                        if access_rule.protected_image:
                            access_rule.protected_image.delete()

                        # Delete the access rule
                        access_rule.delete()

                        return Response(status=status.HTTP_204_NO_CONTENT)

                    except ImageAccess.DoesNotExist:
                        return Response({
                            'error': 'Access rule not found'
                        }, status=status.HTTP_404_NOT_FOUND)
                else:
                    # Delete all access rules for the image
                    access_rules = ImageAccess.objects.filter(user_image=user_image)

                    # Delete protected images for all rules
                    for rule in access_rules:
                        if rule.protected_image:
                            rule.protected_image.delete()

                    # Delete all rules
                    access_rules.delete()

                    return Response(status=status.HTTP_204_NO_CONTENT)

            except UserImage.DoesNotExist:
                return Response({
                    'error': 'Image not found or unauthorized access'
                }, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({
                    'error': f'Failed to delete access rule: {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import ImageAccess, UserImage, OTPSecret
from .utils import OTPHandler
from .serializers import AccessVerificationSerializer, ImageAccessSerializer

# class InitiateAccessView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request, token):
#         try:
#             access = ImageAccess.objects.get(token=token)
#             email = request.data.get('email')
#             password = request.data.get('password', None)

#             # Validate email
#             if not email:
#                 return Response({
#                     'error': 'Email is required'
#                 }, status=status.HTTP_400_BAD_REQUEST)

#             # Debug info
#             print(f"Access check - Token: {token}, Email: {email}")
#             print(f"Allowed emails: {access.allowed_emails}")

#             # Only check email restrictions if allowed_emails is not empty
#             if access.allowed_emails:
#                 # Check if email is allowed
#                 email_lower = email.lower()
#                 allowed_emails_lower = [e.lower() for e in access.allowed_emails if e]
#                 print(f"Checking if {email_lower} is in {allowed_emails_lower}")
#                 is_allowed = email_lower in allowed_emails_lower

#                 # If email is not allowed
#                 if not is_allowed:
#                     print(f"Email {email} not authorized")
#                     # Check for existing access requests
#                     try:
#                         access_request = AccessRequest.objects.get(
#                             image_access=access,
#                             email=email_lower
#                         )

#                         print(f"Found existing access request with status: {access_request.status}")

#                         if access_request.status == 'approved':
#                             # If approved, add to allowed emails
#                             allowed_emails = access.allowed_emails or []
#                             allowed_emails.append(email_lower)
#                             access.allowed_emails = allowed_emails
#                             access.save()
#                             is_allowed = True
#                             print(f"Request was approved, added to allowed emails")
#                         elif access_request.status == 'pending':
#                             print(f"Request is pending approval")
#                             return Response({
#                                 'error': 'Your access request is pending approval',
#                                 'request_status': 'pending'
#                             }, status=status.HTTP_403_FORBIDDEN)
#                         else:  # denied
#                             print(f"Request was denied")
#                             return Response({
#                                 'error': 'Your access request was denied',
#                                 'request_status': 'denied',
#                                 'can_request_again': True
#                             }, status=status.HTTP_403_FORBIDDEN)
#                     except AccessRequest.DoesNotExist:
#                         print(f"No existing access request, can request access")
#                         # Allow user to request access
#                         return Response({
#                             'error': 'Email not authorized',
#                             'can_request_access': True
#                         }, status=status.HTTP_403_FORBIDDEN)
#                     except Exception as e:
#                         print(f"Error checking access request: {str(e)}")
#                         # Still allow requesting access on error
#                         return Response({
#                             'error': 'Email not authorized',
#                             'can_request_access': True
#                         }, status=status.HTTP_403_FORBIDDEN)
#             else:
#                 # If allowed_emails is empty, access is open to all
#                 print("No email restrictions, access open to all")
#                 is_allowed = True

#             # Check if password is required
#             if not password and access.requires_password:
#                 return Response({
#                     'requires_password': True,
#                     'message': 'Password required'
#                 }, status=status.HTTP_200_OK)

#             # Validate password if required
#             if access.requires_password:
#                 if not password:
#                     return Response({
#                         'error': 'Password is required'
#                     }, status=status.HTTP_400_BAD_REQUEST)

#                 if not access.check_password(password):
#                     return Response({
#                         'error': 'Invalid password'
#                     }, status=status.HTTP_400_BAD_REQUEST)

#             # Generate and send OTP
#             otp = OTPHandler.generate_and_store_otp(access, email)

#             try:
#                 send_mail(
#                     'Access Verification Code',
#                     f'Your verification code is: {otp}\nValid for 5 minutes.',
#                     settings.EMAIL_HOST_USER,
#                     [email],
#                     fail_silently=False,
#                 )

#                 return Response({
#                     'message': 'OTP sent successfully'
#                 }, status=status.HTTP_200_OK)
#             except Exception as e:
#                 print(f"Error sending OTP: {str(e)}")
#                 return Response({
#                     'error': 'Failed to send OTP'
#                 }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         except ImageAccess.DoesNotExist:
#             print(f"No access rule found for token: {token}")
#             return Response({
#                 'error': 'Invalid access token'
#             }, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             print(f"Unexpected error: {str(e)}")
#             return Response({
#                 'error': str(e)
#             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class InitiateAccessView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, token):
        try:
            access = ImageAccess.objects.get(token=token)

            # Check if access rule itself is valid (e.g., max_views, expiration)
            if not access.is_valid():
                # Log this attempt
                location_data = SimpleLocationCollector.get_location_data(request)
                AccessLog.objects.create(
                    image_access=access,
                    email=request.data.get('email', 'unknown@example.com'), # Try to get email
                    ip_address=location_data.get('ip_address'),
                    country=location_data.get('country'),
                    region=location_data.get('region'),
                    city=location_data.get('city'),
                    action_type='ATTEMPT',
                    success=False,
                    # Add a note about why it failed if possible, e.g., in a new field or a generic message
                    # For now, just logging the attempt before returning error
                )
                return Response({
                    'error': 'Access limit reached or this link is no longer valid.'
                }, status=status.HTTP_403_FORBIDDEN)

            email = request.data.get('email')
            password = request.data.get('password', None)

            # Validate email
            if not email:
                return Response({
                    'error': 'Email is required'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Debug info
            print(f"Access check - Token: {token}, Email: {email}")
            print(f"Allowed emails: {access.allowed_emails}")

            # Only check email restrictions if allowed_emails is not empty
            if access.allowed_emails:
                # Check if email is allowed
                email_lower = email.lower()
                allowed_emails_lower = [e.lower() for e in access.allowed_emails if e]
                print(f"Checking if {email_lower} is in {allowed_emails_lower}")
                is_allowed = email_lower in allowed_emails_lower

                # If email is not allowed
                if not is_allowed:
                    print(f"Email {email} not authorized")
                    # Check for existing access requests
                    try:
                        access_request = AccessRequest.objects.get(
                            image_access=access,
                            email=email_lower
                        )

                        print(f"Found existing access request with status: {access_request.status}")

                        if access_request.status == 'approved':
                            # If approved, add to allowed emails
                            allowed_emails = access.allowed_emails or []
                            allowed_emails.append(email_lower)
                            access.allowed_emails = allowed_emails
                            access.save()
                            is_allowed = True
                            print(f"Request was approved, added to allowed emails")
                        elif access_request.status == 'pending':
                            print(f"Request is pending approval")
                            return Response({
                                'error': 'Your access request is pending approval',
                                'request_status': 'pending'
                            }, status=status.HTTP_403_FORBIDDEN)
                        else:  # denied
                            print(f"Request was denied")
                            return Response({
                                'error': 'Your access request was denied',
                                'request_status': 'denied',
                                'can_request_again': True
                            }, status=status.HTTP_403_FORBIDDEN)
                    except AccessRequest.DoesNotExist:
                        print(f"No existing access request, can request access")
                        # Allow user to request access
                        return Response({
                            'error': 'Email not authorized',
                            'can_request_access': True
                        }, status=status.HTTP_403_FORBIDDEN)
                    except Exception as e:
                        print(f"Error checking access request: {str(e)}")
                        # Still allow requesting access on error
                        return Response({
                            'error': 'Email not authorized',
                            'can_request_access': True
                        }, status=status.HTTP_403_FORBIDDEN)
            else:
                # If allowed_emails is empty, access is open to all
                print("No email restrictions, access open to all")
                is_allowed = True

            # Check if password is required
            if not password and access.requires_password:
                return Response({
                    'requires_password': True,
                    'message': 'Password required'
                }, status=status.HTTP_200_OK)

            # Validate password if required
            if access.requires_password:
                if not password:
                    return Response({
                        'error': 'Password is required'
                    }, status=status.HTTP_400_BAD_REQUEST)

                if not access.check_password(password):
                    return Response({
                        'error': 'Invalid password'
                    }, status=status.HTTP_400_BAD_REQUEST)

            # Generate and send OTP
            otp = OTPHandler.generate_and_store_otp(access, email)

            try:
                send_mail(
                    'Access Verification Code - Authograph',
                    f'''Dear User,

Your verification code for accessing the protected image is: {otp}

This code is valid for 5 minutes. Please do not share this code with anyone.

If you did not request access to this image, please ignore this email.

Best regards,
The Authograph Team''',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )

                return Response({
                    'message': 'OTP sent successfully',
                    'requires_otp': True
                }, status=status.HTTP_200_OK)
            except Exception as e:
                print(f"Error sending OTP: {str(e)}")
                return Response({
                    'error': 'Failed to send OTP'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except ImageAccess.DoesNotExist:
            print(f"No access rule found for token: {token}")
            return Response({
                'error': 'Invalid access token'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from .utils import SimpleLocationCollector

class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def get_protected_image_url(self, access, request):
        """Get the appropriate image URL based on protection features"""
        user_image = access.user_image
        protection_features = access.protection_features

        # Check if we already have a protected image for this access rule
        if access.protected_image:
            return access.protected_image.url

        # If not, create one using the ProtectionChain
        from .utils import ProtectionChain
        protected_image = ProtectionChain.create_protected_image(user_image, protection_features, access)
        if protected_image:
            return protected_image.url

        # If no protection is applied or features aren't available, return original image
        return user_image.image.url

    def post(self, request, token):
            try:
                email = request.data.get('email')
                provided_otp = request.data.get('otp')

                if not email or not provided_otp:
                    return Response({'error': 'Email and OTP are required'}, status=400)

                try:
                    access = ImageAccess.objects.get(token=token)
                    image_owner_user = access.user_image.user # Get image owner
                except ImageAccess.DoesNotExist:
                    return Response({'error': 'Invalid token'}, status=404)

                location_data = SimpleLocationCollector.get_location_data(request)
                logger.info(f"Location data received: {location_data}")

                access_log_defaults = {
                    'email': email,
                    'ip_address': location_data.get('ip_address'),
                    'country': location_data.get('country'),
                    'region': location_data.get('region'),
                    'city': location_data.get('city'),
                }

                if not access.is_valid():
                    AccessLog.objects.create(
                        image_access=access, **access_log_defaults,
                        action_type='ATTEMPT', success=False
                    )
                    # Notify owner of failed attempt due to invalid access rule
                    owner_profile = get_user_profile_for_notifications(image_owner_user.id)
                    if owner_profile and owner_profile.notify_on_failed_access:
                        try:
                            send_mail(
                                'Security Alert: Failed Access Attempt - Authograph',
                                f'''Dear {image_owner_user.username},

We detected a failed attempt to access your protected image "{access.user_image.image_name}".

Details:
- Attempted by: {email}
- Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
- Reason: Invalid access rule or expired link

If you believe this was an unauthorized attempt, please review your security settings or contact our support team.

Best regards,
The Authograph Security Team''',
                                settings.EMAIL_HOST_USER, [image_owner_user.email], fail_silently=True
                            )
                            logger.info(f"Failed access (rule invalid) notification sent to {image_owner_user.email}")
                        except Exception as e_notify:
                            logger.error(f"Error sending failed access (rule invalid) notification: {str(e_notify)}")
                    return Response({'error': 'Access limit reached or this link is no longer valid.'}, status=status.HTTP_403_FORBIDDEN)

                if not OTPHandler.verify_otp(access, email, provided_otp):
                    AccessLog.objects.create(
                        image_access=access, **access_log_defaults,
                        action_type='ATTEMPT', success=False
                    )
                    # Notify owner of failed attempt due to invalid OTP
                    owner_profile = get_user_profile_for_notifications(image_owner_user.id)
                    if owner_profile and owner_profile.notify_on_failed_access:
                        try:
                            send_mail(
                                'Security Alert: Invalid OTP Attempt - Authograph',
                                f'''Dear {image_owner_user.username},

We detected an invalid OTP attempt for your protected image "{access.user_image.image_name}".

Details:
- Attempted by: {email}
- Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
- Action: Invalid OTP verification

If you believe this was an unauthorized attempt, please review your security settings or contact our support team.

Best regards,
The Authograph Security Team''',
                                settings.EMAIL_HOST_USER, [image_owner_user.email], fail_silently=True
                            )
                            logger.info(f"Failed access (invalid OTP) notification sent to {image_owner_user.email}")
                        except Exception as e_notify:
                            logger.error(f"Error sending failed access (invalid OTP) notification: {str(e_notify)}")
                    return Response({'error': 'Invalid or expired OTP'}, status=status.HTTP_400_BAD_REQUEST)

                # OTP is valid, proceed with access
                access.current_views += 1
                access.save(update_fields=['current_views'])

                AccessLog.objects.create(
                    image_access=access, **access_log_defaults,
                    action_type='VIEW', success=True
                )
                
                # Notify owner of successful view
                owner_profile = get_user_profile_for_notifications(image_owner_user.id)
                if owner_profile and owner_profile.notify_on_successful_access:
                    try:
                        send_mail(
                            'Image Access Notification - Authograph',
                            f'''Dear {image_owner_user.username},

Your protected image "{access.user_image.image_name}" was successfully accessed.

Details:
- Accessed by: {email}
- Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
- Action: Image view

You can view detailed access logs in your Authograph dashboard.

Best regards,
The Authograph Team''',
                            settings.EMAIL_HOST_USER, [image_owner_user.email], fail_silently=True
                        )
                        logger.info(f"Successful access notification sent to {image_owner_user.email}")
                    except Exception as e_notify:
                        logger.error(f"Error sending successful access notification: {str(e_notify)}")
                
                image_url = self.get_protected_image_url(access, request)
                return Response({
                    'message': 'Access granted',
                    'image_url': request.build_absolute_uri(image_url),
                    'allow_download': access.allow_download,
                    'protection_features': access.protection_features
                })

            except Exception as e:
                logger.error(f"Error in VerifyOTPView: {str(e)}", exc_info=True)
                return Response(
                    {'error': f'Verification failed: An unexpected error occurred.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import AccessLog, UserImage
from .serializers import AccessLogSerializer
from django.db.models import Q

class AccessLogView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get query parameters
        image_id = request.query_params.get('image_id')
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        action_type = request.query_params.get('action_type')
        search = request.query_params.get('search')

        # Base queryset - get logs for all images owned by the user
        queryset = AccessLog.objects.filter(
            image_access__user_image__user=request.user
        )

        # Apply filters
        if image_id:
            queryset = queryset.filter(image_access__user_image_id=image_id)

        if date_from:
            queryset = queryset.filter(accessed_at__gte=date_from)

        if date_to:
            queryset = queryset.filter(accessed_at__lte=date_to)

        if action_type:
            queryset = queryset.filter(action_type=action_type)

        if search:
            queryset = queryset.filter(
                Q(email__icontains=search) |
                Q(location__icontains=search) |
                Q(ip_address__icontains=search)
            )

        # Serialize and return data
        serializer = AccessLogSerializer(queryset, many=True)

        return Response({
            'count': queryset.count(),
            'results': serializer.data
        })

    def delete(self, request):
        # Allow users to clear their access logs
        image_id = request.query_params.get('image_id')

        if image_id:
            # Delete logs for specific image
            AccessLog.objects.filter(
                image_access__user_image_id=image_id,
                image_access__user_image__user=request.user
            ).delete()
        else:
            # Delete all logs for user's images
            AccessLog.objects.filter(
                image_access__user_image__user=request.user
            ).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class ImageAccessLogView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, image_id):
        # Base queryset - get logs for specific image owned by the user
        queryset = AccessLog.objects.filter(
            image_access__user_image__user=request.user,
            image_access__user_image_id=image_id
        )

        # Get query parameters
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        action_type = request.query_params.get('action_type')
        search = request.query_params.get('search')

        # Apply filters
        if date_from:
            queryset = queryset.filter(accessed_at__gte=date_from)

        if date_to:
            queryset = queryset.filter(accessed_at__lte=date_to)

        if action_type:
            queryset = queryset.filter(action_type=action_type)

        if search:
            queryset = queryset.filter(
                Q(email__icontains=search) |
                Q(location__icontains=search) |
                Q(ip_address__icontains=search)
            )

        # Serialize and return data
        serializer = AccessLogSerializer(queryset, many=True)

        return Response({
            'count': queryset.count(),
            'results': serializer.data
        })

    def delete(self, request, image_id):
        # Delete logs for specific image
        AccessLog.objects.filter(
            image_access__user_image_id=image_id,
            image_access__user_image__user=request.user
        ).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import UserImage
from .serializers import ImageMetadataSerializer
from .metadata_utils import MetadataExtractor
import tempfile
import os

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import UserImage

class ImageMetadataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, image_id):
        try:
            user_image = UserImage.objects.get(id=image_id, user=request.user)
            return Response({
                'metadata': user_image.metadata or {}
            }, status=status.HTTP_200_OK)
        except UserImage.DoesNotExist:
            return Response(
                {'error': 'Image not found or access denied'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Unexpected error: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, image_id):
        try:
            user_image = UserImage.objects.get(id=image_id, user=request.user)
            updates = request.data.get('updates', [])

            if not updates:
                return Response(
                    {'message': 'No updates provided'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Get current metadata or initialize if None
            current_metadata = user_image.metadata if user_image.metadata else {
                'XMP': {
                    'Basic Information': {},
                    'Protection & Copyright': {}
                },
                'EXIF': {
                    'Location Data': {},
                    'Protection & Copyright': {},
                    'Basic Image Information': {},
                    'Camera & Device Information': {}
                },
                'IPTC': {
                    'Location Data': {},
                    'Creator and Copyright Information': {}
                },
                'custom': {}
            }

            # Apply updates
            for update in updates:
                type_ = update.get('type')
                field_name = update.get('field_name')
                value = update.get('value')

                if not all([type_, field_name]):
                    continue

                # Handle custom metadata
                if type_ == 'custom':
                    if 'custom' not in current_metadata:
                        current_metadata['custom'] = {}
                    if field_name not in current_metadata['custom']:
                        current_metadata['custom'][field_name] = {}
                    current_metadata['custom'][field_name]['value'] = value
                    current_metadata['custom'][field_name]['type'] = 'string'
                    current_metadata['custom'][field_name]['label'] = field_name
                else:
                    # Handle regular metadata
                    type_upper = type_.upper()
                    if type_upper in current_metadata:
                        # Find the section containing the field
                        for section_name, section in current_metadata[type_upper].items():
                            for field, field_data in section.items():
                                if field == field_name:
                                    section[field_name]['value'] = value
                                    break

            # Save the updated metadata
            user_image.metadata = current_metadata
            user_image.save(update_fields=['metadata'])

            return Response({
                'message': 'Metadata updated successfully',
                'metadata': current_metadata
            })

        except UserImage.DoesNotExist:
            return Response(
                {'error': 'Image not found or access denied'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Failed to update metadata: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CustomMetadataView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, image_id):
        try:
            # Get the image
            image = UserImage.objects.get(id=image_id, user=request.user)

            # Get the data from request
            tag_name = request.data.get('tag_name')
            value = request.data.get('value')

            if not tag_name or value is None:
                return Response({
                    'error': 'Both tag_name and value are required'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Get current metadata
            metadata = image.metadata or {}

            # Ensure custom section exists
            if 'custom' not in metadata:
                metadata['custom'] = {}

            # Add new custom field
            metadata['custom'][tag_name] = {
                'value': value,
                'type': 'string',
                'label': tag_name
            }

            # Save updated metadata
            image.metadata = metadata
            image.save(update_fields=['metadata'])

            return Response({
                'tag_name': tag_name,
                'value': value
            })

        except UserImage.DoesNotExist:
            return Response({
                'error': 'Image not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from .models import AccessRequest

class RequestAccessView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, token):
        try:
            access = ImageAccess.objects.get(token=token)
            email = request.data.get('email')
            message = request.data.get('message', '')

            if not email:
                return Response({'error': 'Email is required'}, status=400)

            # Check existing request
            try:
                existing_request = AccessRequest.objects.get(
                    image_access=access,
                    email=email.lower()
                )

                if existing_request.status == 'pending':
                    return Response({
                        'message': 'Your access request is already pending',
                        'request_status': 'pending'
                    }, status=403)
                elif existing_request.status == 'denied':
                    # Update the existing request with new message
                    existing_request.message = message
                    existing_request.status = 'pending'
                    existing_request.save()

                    return Response({
                        'message': 'New access request submitted successfully',
                        'request_status': 'pending'
                    }, status=201)
                elif existing_request.status == 'approved':
                    return Response({
                        'message': 'Your access has already been approved',
                        'request_status': 'approved'
                    }, status=200)

            except AccessRequest.DoesNotExist:
                # Create new request
                AccessRequest.objects.create(
                    image_access=access,
                    email=email.lower(),
                    message=message,
                    status='pending'
                )

                # Send notification to owner IF PREFERENCE IS ENABLED
                try:
                    owner_user = access.user_image.user
                    owner_profile = get_user_profile_for_notifications(owner_user.id)
                    
                    if owner_profile and owner_profile.notify_on_access_request:
                        send_mail(
                            'New Access Request - Authograph',
                            f'''Dear {owner_user.username},

A new access request has been submitted for your protected image "{access.user_image.image_name}".

Request Details:
- Requested by: {email}
- Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
- Message: {message}

You can review and manage this request in your Authograph dashboard.

Best regards,
The Authograph Team''',
                            settings.EMAIL_HOST_USER,
                            [owner_user.email],
                            fail_silently=True,
                        )
                        logger.info(f"Access request notification sent to {owner_user.email} for image {access.user_image.id}")
                    elif owner_profile:
                        logger.info(f"Access request notification NOT sent to {owner_user.email} (preference disabled) for image {access.user_image.id}")
                    else:
                        logger.error(f"Could not retrieve profile for owner {owner_user.id} to check access request notification preference.")
                        
                except Exception as e:
                    logger.error(f"Failed to send access request notification: {str(e)}")

                return Response({
                    'message': 'Access request submitted successfully',
                    'request_status': 'pending'
                }, status=201)

        except ImageAccess.DoesNotExist:
            return Response({'error': 'Invalid access token'}, status=404)
        except Exception as e:
            logger.error(f"Error in RequestAccessView: {str(e)}", exc_info=True)
            return Response({'error': 'An unexpected error occurred.'}, status=500)

from .models import AccessRequest
from .serializers import AccessRequestSerializer

class ManageAccessRequestsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get all access requests for user's images"""
        try:
            # Get all requests for user's images
            queryset = AccessRequest.objects.filter(
                image_access__user_image__user=request.user,
                status='pending'
            ).order_by('-created_at')

            serializer = AccessRequestSerializer(queryset, many=True)

            return Response({
                'results': serializer.data,
                'count': queryset.count()
            })

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, request_id=None):
        """Handle approve/deny actions"""
        if not request_id:
            return Response(
                {'error': 'Request ID is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            access_request = AccessRequest.objects.get(
                id=request_id,
                image_access__user_image__user=request.user
            )

            action = request.data.get('action')
            if action not in ['approve', 'deny']:
                return Response(
                    {'error': 'Invalid action. Must be either "approve" or "deny"'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Update status based on action
            access_request.status = 'approved' if action == 'approve' else 'denied'
            access_request.save()

            # If approved, add email to allowed_emails
            if action == 'approve':
                image_access = access_request.image_access
                allowed_emails = image_access.allowed_emails or []
                if access_request.email.lower() not in [email.lower() for email in allowed_emails]:
                    allowed_emails.append(access_request.email)
                    image_access.allowed_emails = allowed_emails
                    image_access.save()

            # Send notification email
            try:
                status_text = 'approved' if action == 'approve' else 'denied'
                send_mail(
                    f'Access Request Update - Authograph',
                    f'''Dear User,

Your access request for the protected image has been {status_text}.

Details:
- Status: {status_text.capitalize()}
- Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

If your request was approved, you can now access the image using the original access link.

Best regards,
The Authograph Team''',
                    settings.EMAIL_HOST_USER,
                    [access_request.email],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Failed to send notification: {str(e)}")

            return Response({
                'message': f'Request successfully {action}ed',
                'status': access_request.status
            })

        except AccessRequest.DoesNotExist:
            return Response(
                {'error': 'Request not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class AIProtectionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, image_id):
        """Get AI protection settings for an image"""
        try:
            user_image = UserImage.objects.get(id=image_id, user=request.user)
            try:
                settings = AIProtectionSettings.objects.get(user_image=user_image)
                serializer = AIProtectionSettingsSerializer(settings, context={'request': request})
                return Response(serializer.data)
            except AIProtectionSettings.DoesNotExist:
                return Response({
                    'enabled': False,
                    'protected_image': None
                })
        except UserImage.DoesNotExist:
            return Response(
                {'error': 'Image not found or unauthorized access'},
                status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request, image_id):
        """Apply or update AI protection using external perturb API"""
        try:
            user_image = UserImage.objects.get(id=image_id, user=request.user)
            
            # Get decrypted image
            img = user_image.get_decrypted_image()
            
            # Convert image to bytes for API request
            success, buffer = cv2.imencode('.png', img)
            if not success:
                logger.error("Failed to encode image for perturb API")
                return Response(
                    {'error': 'Failed to encode image'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # Make request to perturb API
            import requests
            try:
                # Create a temporary file to store the image
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                    temp_file.write(buffer.tobytes())
                    temp_file.flush()
                    
                    # Make the API request with the file
                    with open(temp_file.name, 'rb') as f:
                        response = requests.post(
                            'http://20.168.8.203/perturb',
                            files={'file': ('image.png', f, 'image/png')},
                            timeout=30  # 30 second timeout
                        )
                
                # Clean up the temporary file
                os.unlink(temp_file.name)
                
                if response.status_code == 422:
                    logger.error(f"Perturb API validation error: {response.text}")
                    return Response(
                        {'error': 'Invalid image format or size'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                elif response.status_code != 200:
                    logger.error(f"Perturb API error: Status {response.status_code}, Response: {response.text}")
                    return Response(
                        {'error': f'Perturb API returned status code {response.status_code}'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                
                # Convert response content to image
                perturbed_img = cv2.imdecode(
                    np.frombuffer(response.content, np.uint8),
                    cv2.IMREAD_COLOR
                )
                
                if perturbed_img is None:
                    logger.error("Failed to decode perturbed image from API response")
                    return Response(
                        {'error': 'Failed to decode perturbed image from API response'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                
                # Save the protected image
                settings, created = AIProtectionSettings.objects.get_or_create(
                    user_image=user_image,
                    defaults={'enabled': True}
                )
                
                # Save the protected image to a temporary file
                success, buffer = cv2.imencode('.png', perturbed_img)
                if not success:
                    logger.error("Failed to encode protected image for storage")
                    return Response(
                        {'error': 'Failed to encode protected image'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                
                # Save the image to the model
                settings.protected_image.save(
                    f'ai_protected_{user_image.image_name}',
                    ContentFile(buffer.tobytes()),
                    save=True
                )
                
                settings.enabled = True
                settings.save()
                
                # Update the UserImage model
                user_image.ai_protection_enabled = True
                user_image.save(update_fields=['ai_protection_enabled'])
                
                serializer = AIProtectionSettingsSerializer(settings, context={'request': request})
                return Response(serializer.data)
                
            except requests.RequestException as e:
                logger.error(f"Request to perturb API failed: {str(e)}")
                return Response(
                    {'error': f'Failed to communicate with perturb API: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
        except UserImage.DoesNotExist:
            return Response(
                {'error': 'Image not found or unauthorized access'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Unexpected error in AIProtectionView.post: {str(e)}", exc_info=True)
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, image_id):
        """Remove AI protection"""
        try:
            user_image = UserImage.objects.get(id=image_id, user=request.user)
            try:
                settings = AIProtectionSettings.objects.get(user_image=user_image)
                if settings.protected_image:
                    settings.protected_image.delete()
                settings.delete()
                
                # Update the UserImage model
                user_image.ai_protection_enabled = False
                user_image.save(update_fields=['ai_protection_enabled'])
                
                return Response(status=status.HTTP_204_NO_CONTENT)
            except AIProtectionSettings.DoesNotExist:
                return Response(
                    {'error': 'AI protection not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        except UserImage.DoesNotExist:
            return Response(
                {'error': 'Image not found or unauthorized access'},
                status=status.HTTP_404_NOT_FOUND
            )

from django.http import FileResponse

class ServeProtectedImageDownloadView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token):
        try:
            image_access = ImageAccess.objects.get(token=token)
            image_owner_user = image_access.user_image.user # Get image owner

            if not image_access.protected_image or not image_access.protected_image.name:
                return Response(
                    {'error': 'Protected image not found for this access rule.'},
                    status=status.HTTP_404_NOT_FOUND
                )
            if not image_access.protected_image.storage.exists(image_access.protected_image.name):
                return Response(
                    {'error': 'Protected image file is missing from storage.'},
                    status=status.HTTP_404_NOT_FOUND
                )

            response = FileResponse(image_access.protected_image.open('rb'), as_attachment=True)
            
            try:
                # Get email from headers first
                log_email = request.headers.get('X-Access-Email')
                access_name = request.headers.get('X-Access-Name')
                
                logger.info(f"Download request - Token: {token}")
                logger.info(f"Headers - Email: {log_email}, Access Name: {access_name}")
                logger.info(f"Access Rule - Allowed Emails: {image_access.allowed_emails}")

                # Special case for owner download
                if log_email == 'owner@igaurdian.local':
                    log_email = image_owner_user.email
                    logger.info(f"Owner download detected, using owner email: {log_email}")
                # If no email in headers, try to get from access rule
                elif not log_email or log_email == 'unknown':
                    if image_access.allowed_emails:
                        log_email = image_access.allowed_emails[0]
                        logger.info(f"Using email from access rule: {log_email}")
                    elif request.user.is_authenticated:
                        log_email = request.user.email
                        logger.info(f"Using authenticated user email: {log_email}")
                    elif hasattr(request, 'session') and request.session.get('verified_email_for_token_' + token):
                        log_email = request.session['verified_email_for_token_' + token]
                        logger.info(f"Using email from session: {log_email}")
                    else:
                        # Use access name as identifier if available
                        log_email = f"{access_name}@access.local" if access_name and access_name != 'unknown' else 'unknown_downloader@example.com'
                        logger.info(f"Using fallback email: {log_email}")

                location_data = SimpleLocationCollector.get_location_data(request)
                logger.info(f"Location data: {location_data}")

                AccessLog.objects.create(
                    image_access=image_access,
                    email=log_email, 
                    ip_address=location_data.get('ip_address'),
                    country=location_data.get('country'),
                    region=location_data.get('region'),
                    city=location_data.get('city'),
                    action_type='DOWNLOAD',
                    success=True
                )
                
                # Notify owner of download IF PREFERENCE IS ENABLED
                owner_profile = get_user_profile_for_notifications(image_owner_user.id)
                if owner_profile and owner_profile.notify_on_download:
                    try:
                        send_mail(
                            'Image Download Alert - Authograph',
                            f'''Dear {image_owner_user.username},

Your protected image "{image_access.user_image.image_name}" was downloaded.

Details:
- Downloaded by: {log_email}
- Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
- Action: Image download

You can view detailed access logs in your Authograph dashboard.

Best regards,
The Authograph Team''',
                            settings.EMAIL_HOST_USER, [image_owner_user.email], fail_silently=True
                        )
                        logger.info(f"Image download notification sent to {image_owner_user.email}")
                    except Exception as e_notify:
                        logger.error(f"Error sending image download notification: {str(e_notify)}")
                elif owner_profile:
                    logger.info(f"Image download notification NOT sent to {image_owner_user.email} (preference disabled)")
                else:
                    logger.error(f"Could not retrieve profile for owner {image_owner_user.id} to check download notification preference.")

            except Exception as log_e:
                logger.error(f"Error creating download access log: {str(log_e)}")

            return response

        except ImageAccess.DoesNotExist:
            return Response({'error': 'Invalid access token.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error serving protected image for download: {str(e)}", exc_info=True)
            return Response({'error': 'An error occurred while processing your request.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class NotificationSettingsView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update notification settings for the authenticated user.
    """
    serializer_class = NotificationSettingsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Ensure UserProfile exists, create if not (should be handled by signal, but good practice)
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile

class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AccountDeletionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                # Delete all user's images and related data
                UserImage.objects.filter(user=request.user).delete()
                
                # Delete user profile
                UserProfile.objects.filter(user=request.user).delete()
                
                # Delete the user account
                request.user.delete()
                
                return Response(
                    {"message": "Account successfully deleted."},
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response(
                    {"error": "Failed to delete account. Please try again."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
