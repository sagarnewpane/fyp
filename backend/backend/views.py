from django.contrib.auth.tokens import default_token_generator
from django.db.models.manager import QuerySet
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import RegisterUserSerializer, PasswordResetRequestSerializer, PasswordResetConfirmSerializer, SpecificImageSerializer, UserImageSerializer, UserImageListSerializer, PasswordChangeSerializer, OTPVerificationSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .models import UserImage, WatermarkSettings, InvisibleWatermarkSettings
from rest_framework.parsers import MultiPartParser, FormParser  #


from django.http import HttpResponse, Http404
import cv2
import os
import traceback

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
                'Password Reset Request',
                f'Please click the following link to reset your password: {reset_link}',
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

class InitiateAccessView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, token):
        try:
            access = ImageAccess.objects.get(token=token)
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
                    'Access Verification Code',
                    f'Your verification code is: {otp}\nValid for 5 minutes.',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )

                return Response({
                    'message': 'OTP sent successfully'
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
import logging

logger = logging.getLogger(__name__)

class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def get_protected_image_url(self, access, request):
        """Get the appropriate image URL based on protection features"""
        user_image = access.user_image
        protection_features = access.protection_features

        if protection_features.get('watermark') and user_image.watermark_enabled:
            try:
                watermark_settings = WatermarkSettings.objects.get(user_image=user_image)
                if watermark_settings.enabled and watermark_settings.watermarked_image:
                    return watermark_settings.watermarked_image.url
            except WatermarkSettings.DoesNotExist:
                pass

        if protection_features.get('hidden_watermark') and user_image.hidden_watermark_enabled:
            try:
                invisible_watermark = InvisibleWatermarkSettings.objects.get(user_image=user_image)
                if invisible_watermark.enabled and invisible_watermark.embedded_image:
                    return invisible_watermark.embedded_image.url
            except InvisibleWatermarkSettings.DoesNotExist:
                pass

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
                except ImageAccess.DoesNotExist:
                    return Response({'error': 'Invalid token'}, status=404)

                # Get location data with logging
                location_data = SimpleLocationCollector.get_location_data(request)
                logger.info(f"Location data received: {location_data}")

                # Create access log with location data
                access_log = AccessLog.objects.create(
                    image_access=access,
                    email=email,
                    ip_address=location_data.get('ip_address'),
                    country=location_data.get('country'),
                    region=location_data.get('region'),
                    city=location_data.get('city'),
                    action_type='ATTEMPT',
                    success=False
                )
                logger.info(f"Access log created: {access_log.id}")

                # Verify OTP
                if not OTPHandler.verify_otp(access, email, provided_otp):
                    return Response({'error': 'Invalid or expired OTP'}, status=400)

                # Update access log to successful
                access_log.action_type = 'VIEW'
                access_log.success = True
                access_log.save()

                # Use the pre-generated protected image if available
                image_url = access.protected_image.url if access.protected_image else access.user_image.image.url

                # Construct full URL
                protocol = 'https://' if request.is_secure() else 'http://'
                domain = request.get_host()
                full_image_url = f"{protocol}{domain}{image_url}"

                # Return success response
                return Response({
                    'message': 'Access granted',
                    'image_url': full_image_url,
                    'allow_download': access.allow_download,
                    'protection_features': access.protection_features
                })

            except Exception as e:
                logger.error(f"Error in VerifyOTPView: {str(e)}", exc_info=True)
                return Response(
                    {'error': f'Verification failed: {str(e)}'},
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

                # Send notification to owner
                try:
                    owner_email = access.user_image.user.email
                    send_mail(
                        'New Access Request',
                        f'{email} has requested access to your protected image.\n\nMessage: {message}',
                        settings.EMAIL_HOST_USER,
                        [owner_email],
                        fail_silently=True,
                    )
                except Exception as e:
                    print(f"Failed to send notification: {str(e)}")

                return Response({
                    'message': 'Access request submitted successfully',
                    'request_status': 'pending'
                }, status=201)

        except ImageAccess.DoesNotExist:
            return Response({'error': 'Invalid access token'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

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
                    f'Access Request {status_text.capitalize()}',
                    f'Your request to access the protected image has been {status_text}.',
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
