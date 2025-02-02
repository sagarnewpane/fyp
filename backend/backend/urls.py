from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import (
    RegisterView,
    VerifyView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    ImageUploadView,
    ImageListView,
    UserImageView,
    UserProfileView,
    AvatarUploadView,
    PasswordChangeView,
    WatermarkSettingsView

)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name='auth_register'),
    path('verify/', VerifyView.as_view(), name='verify'),
    path('api/password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('api/password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('upload/', ImageUploadView.as_view(), name='image-upload'),
    path('images/', ImageListView.as_view(), name='image-list'),
    path('image/<int:pk>/', UserImageView.as_view(), name='view-image'),
    path('api/profile/', UserProfileView.as_view(), name='user-profile'),
    path('api/profile/avatar/', AvatarUploadView.as_view(), name='avatar-upload'),
    path('api/password/change/', PasswordChangeView.as_view(), name='password-change'),
    path('api/image/<int:image_id>/watermark-settings/',WatermarkSettingsView.as_view(),name='watermark-settings'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
