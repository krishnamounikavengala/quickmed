




# userapp/views.py
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from .models import UserProfile
from .serializers import UserProfileSerializer, UserProfileReadSerializer

class ProfileRetrieveUpdateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)

        serializer = UserProfileReadSerializer(profile, context={"request": request})
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            read = UserProfileReadSerializer(profile, context={"request": request})
            return Response(read.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfilePhotoUploadAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        file = request.FILES.get('profile_photo')
        if not file:
            return Response({"detail": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        profile.profile_photo = file
        profile.save()
        read = UserProfileReadSerializer(profile, context={"request": request})
        return Response(read.data)

class ProfilePhotoRemoveAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        profile.profile_photo.delete(save=False)  # delete file from storage if exists
        profile.profile_photo = None
        profile.save()
        read = UserProfileReadSerializer(profile, context={"request": request})
        return Response(read.data)
