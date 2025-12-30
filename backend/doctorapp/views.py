



# doctorapp/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser

from .models import DoctorProfile
from .serializers import DoctorProfileSerializer


class DoctorMeView(APIView):
    """
    GET  /api/doctors/me/   -> logged-in doctor's profile ni return cheyyi
    PATCH /api/doctors/me/  -> same profile ni update cheyyi (JSON or FormData)
    """
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def _get_or_create_profile(self, request):
        """
        Logged-in user kosam profile create / fetch chestundi.
        Email & basic name auto-fill chestundi first time.
        """
        user = request.user
        profile, created = DoctorProfile.objects.get_or_create(
            user=user,
            defaults={
                "email": user.email or "",
                "full_name": (
                    (user.first_name or "") + " " + (user.last_name or "")
                ).strip()
                or (user.username or user.email or ""),
            },
        )
        return profile

    def get(self, request, *args, **kwargs):
        profile = self._get_or_create_profile(request)
        serializer = DoctorProfileSerializer(profile, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        """
        Frontend nundi FormData (image unda appudu) or JSON (no file) rendu accept chestundi.
        DoctorModals defaultHandleProfileUpdate → patchMyProfileJson / patchMyProfileFormData
        direct ga ee view ki vastayi.
        """
        profile = self._get_or_create_profile(request)
        serializer = DoctorProfileSerializer(
            profile,
            data=request.data,
            partial=True,   # important: konni fields matrame update chestham
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
