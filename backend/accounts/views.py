# accounts/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .serializers import RegisterSerializer, ProfileSerializer

User = get_user_model()

class RegisterAPIView(generics.CreateAPIView):
    """
    POST /api/accounts/register/
    The RegisterSerializer.to_representation already returns:
      { "user": {..}, "access": "<access>", "refresh": "<refresh>" }
    We call serializer.save() and then return serializer.data (which triggers to_representation).
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # serializer.save() returns the created model instance (per your RegisterSerializer.create)
        instance = serializer.save()

        # serializer.data will call to_representation which (in your serializer) returns tokens + user
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Profile endpoint: GET /api/accounts/profile/
from rest_framework.views import APIView

class ProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)
