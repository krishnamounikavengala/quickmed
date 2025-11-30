


# # backend/deliveryapp/views.py
# from rest_framework import generics, permissions, status
# from rest_framework.response import Response
# from rest_framework.parsers import MultiPartParser, FormParser
# from .models import DeliveryProfile
# from .serializers import DeliveryProfileSerializer
# from rest_framework_simplejwt.authentication import JWTAuthentication

# class DeliveryProfileView(generics.RetrieveUpdateAPIView):
#     """
#     GET -> returns the delivery profile for the authenticated user.
#     PATCH -> partial update for editable fields, including profile_image (file upload).
#     """
#     serializer_class = DeliveryProfileSerializer
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [permissions.IsAuthenticated]

#     # <<< THIS LINE is the important fix (Step B) to accept multipart/form-data uploads
#     parser_classes = (MultiPartParser, FormParser)

#     def get_object(self):
#         # get or create profile to guarantee return object
#         profile, _ = DeliveryProfile.objects.get_or_create(user=self.request.user)
#         return profile

#     def get_serializer_context(self):
#         # ensure serializer can build absolute URLs for file fields
#         return {'request': self.request}

#     def patch(self, request, *args, **kwargs):
#         partial = True
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)




# backend/deliveryapp/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import DeliveryProfile
from .serializers import DeliveryProfileSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

class DeliveryProfileView(generics.RetrieveUpdateAPIView):
    """
    GET -> returns the delivery profile for the authenticated user.
    PATCH -> partial update for editable fields, including profile_image (file upload).
    """
    serializer_class = DeliveryProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    # Accept multipart/form-data so file uploads work
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        # get or create profile to guarantee return object
        profile, _ = DeliveryProfile.objects.get_or_create(user=self.request.user)
        return profile

    def get_serializer_context(self):
        # ensure serializer can build absolute URLs for file fields
        return {'request': self.request}

    def patch(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
