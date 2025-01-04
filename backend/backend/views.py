from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import RegisterUserSerializer, PasswordResetRequestSerializer, PasswordResetConfirmSerializer, UserImageSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


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

    def post(self, request):
        # Add the user to the data
        data = request.data.copy()

        # Create serializer with the data
        serializer = UserImageSerializer(data=data)

        if serializer.is_valid():
            # Save the image and associate it with the user
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import UserImageListSerializer
from .models import UserImage
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ImageListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserImageListSerializer

    def get_queryset(self):
        queryset = UserImage.objects.filter(user=self.request.user)
        params = self.request.query_params

        # Search filter
        search_query = params.get('search', '')
        if search_query:
            queryset = queryset.filter(image_name__icontains=search_query)

        # Date range filter
        date_from = params.get('date_from')
        date_to = params.get('date_to')
        if date_from:
            queryset = queryset.filter(created_at__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__lte=date_to)

        # File type filter
        file_types = params.getlist('file_type')
        if file_types:
            queryset = queryset.filter(file_type__in=file_types)

        # Size range filter (in MB)
        size_min = params.get('size_min')
        size_max = params.get('size_max')
        if size_min:
            queryset = queryset.filter(file_size__gte=float(size_min)*1024*1024)
        if size_max:
            queryset = queryset.filter(file_size__lte=float(size_max)*1024*1024)

        # Sorting
        sort_by = params.get('sort', '-created_at')
        return queryset.order_by(sort_by)
