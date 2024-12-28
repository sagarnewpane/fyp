from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import RegisterUserSerializer
from rest_framework.permissions import AllowAny

class RegisterView(generics.CreateAPIView):
    """
    View for user registration.
    Allows any user (authenticated or not) to access this view.
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterUserSerializer
