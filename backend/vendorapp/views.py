
# # vendorapp/views.py
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
# from rest_framework import status
# from .models import VendorProfile
# from .serializers import VendorProfileSerializer

# class VendorProfileView(APIView):
#     permission_classes = [IsAuthenticated]
#     parser_classes = (MultiPartParser, FormParser, JSONParser)

#     def get_object(self, user):
#         profile, _ = VendorProfile.objects.get_or_create(user=user)
#         return profile

#     def get(self, request, format=None):
#         profile = self.get_object(request.user)
#         serializer = VendorProfileSerializer(profile, context={'request': request})
#         return Response(serializer.data)

#     def patch(self, request, format=None):
#         profile = self.get_object(request.user)

#         # If file present, assign it to the instance first (helps some serializers)
#         if 'profile_image' in request.FILES:
#             profile.profile_image = request.FILES['profile_image']
#             profile.save()

#         serializer = VendorProfileSerializer(profile, data=request.data, partial=True, context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             out = VendorProfileSerializer(profile, context={'request': request})
#             return Response(out.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


######################################################################################################################################



# # vendorapp/views.py
# from rest_framework import generics, permissions, status
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
# from django.shortcuts import get_object_or_404

# from .models import VendorProfile, VendorMedicine, VendorOrder, VendorPrescription
# from .serializers import (
#     VendorProfileSerializer,
#     VendorMedicineSerializer, VendorMedicineCreateSerializer,
#     VendorOrderSerializer, VendorPrescriptionSerializer
# )

# class VendorProfileView(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     parser_classes = (MultiPartParser, FormParser, JSONParser)

#     def get_object(self, user):
#         profile, _ = VendorProfile.objects.get_or_create(user=user)
#         return profile

#     def get(self, request, format=None):
#         profile = self.get_object(request.user)
#         serializer = VendorProfileSerializer(profile, context={'request': request})
#         return Response(serializer.data)

#     def patch(self, request, format=None):
#         profile = self.get_object(request.user)

#         # If file present, assign it to the instance first (helps some serializers)
#         if 'profile_image' in request.FILES:
#             profile.profile_image = request.FILES['profile_image']
#             profile.save()

#         serializer = VendorProfileSerializer(profile, data=request.data, partial=True, context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             out = VendorProfileSerializer(profile, context={'request': request})
#             return Response(out.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # ---------- Medicines ----------
# class VendorMedicineListCreateView(generics.ListCreateAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     parser_classes = (JSONParser,)

#     def get_serializer_class(self):
#         if self.request.method == 'POST':
#             return VendorMedicineCreateSerializer
#         return VendorMedicineSerializer

#     def get_queryset(self):
#         # ensure vendor only sees their medicines
#         profile, _ = VendorProfile.objects.get_or_create(user=self.request.user)
#         return VendorMedicine.objects.filter(vendor=profile).order_by('-created_at')

#     def perform_create(self, serializer):
#         profile, _ = VendorProfile.objects.get_or_create(user=self.request.user)
#         serializer.save(vendor=profile)


# class VendorMedicineDetailView(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = VendorMedicineSerializer
#     lookup_url_kwarg = 'pk'

#     def get_object(self):
#         profile, _ = VendorProfile.objects.get_or_create(user=self.request.user)
#         obj = get_object_or_404(VendorMedicine, pk=self.kwargs.get('pk'), vendor=profile)
#         return obj


# # ---------- Orders (basic list + update) ----------
# class VendorOrderListView(generics.ListAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = VendorOrderSerializer

#     def get_queryset(self):
#         profile, _ = VendorProfile.objects.get_or_create(user=self.request.user)
#         return VendorOrder.objects.filter(vendor=profile).order_by('-order_time')


# class VendorOrderDetailView(generics.RetrieveUpdateAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = VendorOrderSerializer
#     lookup_url_kwarg = 'order_pk'

#     def get_object(self):
#         profile, _ = VendorProfile.objects.get_or_create(user=self.request.user)
#         obj = get_object_or_404(VendorOrder, pk=self.kwargs.get('order_pk'), vendor=profile)
#         return obj


# # ---------- Prescriptions ----------
# class VendorPrescriptionListView(generics.ListAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = VendorPrescriptionSerializer

#     def get_queryset(self):
#         profile, _ = VendorProfile.objects.get_or_create(user=self.request.user)
#         return VendorPrescription.objects.filter(vendor=profile).order_by('-uploaded_time')

# class ApprovePrescriptionView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request, pk, format=None):
#         profile, _ = VendorProfile.objects.get_or_create(user=request.user)
#         rx = get_object_or_404(VendorPrescription, pk=pk, vendor=profile)
#         rx.status = 'approved'
#         rx.save()
#         return Response({'status': 'approved'})

# class RejectPrescriptionView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request, pk, format=None):
#         profile, _ = VendorProfile.objects.get_or_create(user=request.user)
#         rx = get_object_or_404(VendorPrescription, pk=pk, vendor=profile)
#         rx.status = 'rejected'
#         rx.save()
#         return Response({'status': 'rejected'})






# vendorapp/views.py
# vendorapp/views.py
# from rest_framework import generics, permissions, status
# from rest_framework.response import Response
# from rest_framework.exceptions import ValidationError, NotFound
# from rest_framework.parsers import MultiPartParser, FormParser
# from django.shortcuts import get_object_or_404

# from .models import VendorProfile, VendorMedicine, VendorOrder, VendorPrescription
# from .serializers import (
#     VendorProfileSerializer,
#     VendorMedicineSerializer,
#     VendorMedicineCreateSerializer,
#     VendorOrderSerializer,
#     VendorPrescriptionSerializer
# )


# class VendorProfileView(generics.RetrieveUpdateAPIView):
#     """
#     GET /api/vendor/profile/  -> returns VendorProfile for request.user
#     PATCH -> update fields (supports multipart/form-data for image uploads)
#     """
#     permission_classes = [permissions.IsAuthenticated]
#     parser_classes = [MultiPartParser, FormParser]
#     serializer_class = VendorProfileSerializer

#     def get_object(self):
#         try:
#             return self.request.user.vendor_profile
#         except VendorProfile.DoesNotExist:
#             raise NotFound(detail="Vendor profile not available.")

#     def patch(self, request, *args, **kwargs):
#         instance = self.get_object()
#         partial = True
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)


# class VendorMedicineListCreateView(generics.ListCreateAPIView):
#     """
#     GET /api/vendor/medicines/  -> list medicines for current vendor
#     POST /api/vendor/medicines/ -> create medicine for current vendor
#     """
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = VendorMedicineSerializer  # used for list & detail output

#     def get_vendor_profile(self):
#         """Return VendorProfile instance for request.user or None if not present."""
#         try:
#             return self.request.user.vendor_profile
#         except VendorProfile.DoesNotExist:
#             return None

#     def get_queryset(self):
#         vendor = self.get_vendor_profile()
#         if not vendor:
#             return VendorMedicine.objects.none()
#         return VendorMedicine.objects.filter(vendor=vendor).order_by('-created_at')

#     def get(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serializer = VendorMedicineSerializer(queryset, many=True, context={'request': request})
#         return Response(serializer.data)

#     def post(self, request, *args, **kwargs):
#         vendor = self.get_vendor_profile()
#         if not vendor:
#             # Keep the same message shape your frontend expects
#             raise ValidationError("Vendor profile not available.")

#         # Build create-serializer and pass vendor + request in context
#         create_serializer = VendorMedicineCreateSerializer(data=request.data, context={'vendor': vendor, 'request': request})
#         create_serializer.is_valid(raise_exception=True)

#         # serializer.save() will call VendorMedicineCreateSerializer.create and create object with vendor
#         med = create_serializer.save()

#         # Use read serializer for response
#         out = VendorMedicineSerializer(med, context={'request': request})
#         return Response(out.data, status=status.HTTP_201_CREATED)


# class VendorMedicineDetailView(generics.RetrieveUpdateDestroyAPIView):
#     """
#     GET /api/vendor/medicines/<pk>/
#     PATCH /api/vendor/medicines/<pk>/
#     DELETE /api/vendor/medicines/<pk>/
#     """
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = VendorMedicineSerializer
#     lookup_url_kwarg = 'pk'

#     def get_vendor_profile(self):
#         try:
#             return self.request.user.vendor_profile
#         except VendorProfile.DoesNotExist:
#             return None

#     def get_object(self):
#         vendor = self.get_vendor_profile()
#         if not vendor:
#             raise NotFound(detail="Vendor profile not available.")
#         obj = get_object_or_404(VendorMedicine, pk=self.kwargs.get(self.lookup_url_kwarg), vendor=vendor)
#         return obj

#     def patch(self, request, *args, **kwargs):
#         inst = self.get_object()
#         serializer = self.get_serializer(inst, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     def delete(self, request, *args, **kwargs):
#         inst = self.get_object()
#         inst.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class VendorOrderListView(generics.ListAPIView):
#     """
#     GET /api/vendor/orders/ -> list orders for vendor
#     """
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = VendorOrderSerializer

#     def get_vendor_profile(self):
#         try:
#             return self.request.user.vendor_profile
#         except VendorProfile.DoesNotExist:
#             return None

#     def get_queryset(self):
#         vendor = self.get_vendor_profile()
#         if not vendor:
#             return VendorOrder.objects.none()
#         return VendorOrder.objects.filter(vendor=vendor).order_by('-order_time')

#     def get(self, request, *args, **kwargs):
#         qs = self.get_queryset()
#         serializer = self.get_serializer(qs, many=True)
#         return Response(serializer.data)


# class VendorOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
#     """
#     GET /api/vendor/orders/<order_pk>/
#     PATCH -> update (e.g. status)
#     DELETE -> delete order
#     """
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = VendorOrderSerializer
#     lookup_url_kwarg = 'order_pk'

#     def get_vendor_profile(self):
#         try:
#             return self.request.user.vendor_profile
#         except VendorProfile.DoesNotExist:
#             return None

#     def get_object(self):
#         vendor = self.get_vendor_profile()
#         if not vendor:
#             raise ValidationError("Vendor profile not available.")
#         pk = self.kwargs.get(self.lookup_url_kwarg)
#         obj = get_object_or_404(VendorOrder, pk=pk, vendor=vendor)
#         return obj

#     def patch(self, request, *args, **kwargs):
#         inst = self.get_object()
#         serializer = self.get_serializer(inst, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     def delete(self, request, *args, **kwargs):
#         inst = self.get_object()
#         inst.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class VendorPrescriptionListView(generics.ListAPIView):
#     """
#     GET /api/vendor/prescriptions/ -> list prescriptions for vendor
#     """
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = VendorPrescriptionSerializer

#     def get_vendor_profile(self):
#         try:
#             return self.request.user.vendor_profile
#         except VendorProfile.DoesNotExist:
#             return None

#     def get_queryset(self):
#         vendor = self.get_vendor_profile()
#         if not vendor:
#             return VendorPrescription.objects.none()
#         return VendorPrescription.objects.filter(vendor=vendor).order_by('-uploaded_time')

#     def get(self, request, *args, **kwargs):
#         qs = self.get_queryset()
#         serializer = self.get_serializer(qs, many=True)
#         return Response(serializer.data)


# class ApprovePrescriptionView(generics.GenericAPIView):
#     """
#     POST /api/vendor/prescriptions/<pk>/approve/
#     """
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = VendorPrescriptionSerializer
#     lookup_url_kwarg = 'pk'

#     def get_vendor_profile(self):
#         try:
#             return self.request.user.vendor_profile
#         except VendorProfile.DoesNotExist:
#             return None

#     def post(self, request, *args, **kwargs):
#         vendor = self.get_vendor_profile()
#         if not vendor:
#             raise ValidationError("Vendor profile not available.")
#         pk = kwargs.get(self.lookup_url_kwarg)
#         presc = get_object_or_404(VendorPrescription, pk=pk, vendor=vendor)
#         presc.status = 'approved'
#         presc.save()
#         if presc.order:
#             presc.order.status = 'ready'
#             presc.order.save()
#         return Response(self.get_serializer(presc).data)


# class RejectPrescriptionView(generics.GenericAPIView):
#     """
#     POST /api/vendor/prescriptions/<pk>/reject/
#     """
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = VendorPrescriptionSerializer
#     lookup_url_kwarg = 'pk'

#     def get_vendor_profile(self):
#         try:
#             return self.request.user.vendor_profile
#         except VendorProfile.DoesNotExist:
#             return None

#     def post(self, request, *args, **kwargs):
#         vendor = self.get_vendor_profile()
#         if not vendor:
#             raise ValidationError("Vendor profile not available.")
#         pk = kwargs.get(self.lookup_url_kwarg)
#         presc = get_object_or_404(VendorPrescription, pk=pk, vendor=vendor)
#         presc.status = 'rejected'
#         presc.save()
#         if presc.order:
#             presc.order.status = 'cancelled'
#             presc.order.save()
#         return Response(self.get_serializer(presc).data)





###############################################################################################
# vendorapp/views.py
import logging

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404

from .models import VendorProfile, VendorMedicine, VendorOrder, VendorPrescription
from .serializers import (
    VendorProfileSerializer,
    VendorMedicineSerializer,
    VendorMedicineCreateSerializer,
    VendorOrderSerializer,
    VendorPrescriptionSerializer,
    # PublicMedicineSerializer is defined in serializers.py
    PublicMedicineSerializer
)

logger = logging.getLogger(__name__)


class VendorProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = VendorProfileSerializer

    def get_object(self):
        try:
            return self.request.user.vendor_profile
        except VendorProfile.DoesNotExist:
            raise NotFound(detail="Vendor profile not available.")

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        partial = True
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class VendorMedicineListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = VendorMedicineSerializer

    def get_vendor_profile(self):
        user = getattr(self.request, 'user', None)
        if not user or user.is_anonymous:
            return None
        vendor = getattr(user, 'vendor_profile', None)
        if vendor:
            return vendor
        try:
            return VendorProfile.objects.filter(user=user).first()
        except Exception:
            return None

    def get_queryset(self):
        vendor = self.get_vendor_profile()
        if not vendor:
            return VendorMedicine.objects.none()
        return VendorMedicine.objects.filter(vendor=vendor).order_by('-created_at')

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = VendorMedicineSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        logger.debug("Vendor medicines POST called by user: %s (id=%s)",
                     getattr(request.user, 'username', None), getattr(request.user, 'id', None))
        vendor = self.get_vendor_profile()
        if not vendor:
            raise ValidationError({"detail": "Vendor profile not available."})

        serializer = VendorMedicineCreateSerializer(data=request.data, context={'vendor': vendor})
        serializer.is_valid(raise_exception=True)
        med = serializer.save()
        out = VendorMedicineSerializer(med)
        return Response(out.data, status=status.HTTP_201_CREATED)


class VendorMedicineDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = VendorMedicineSerializer
    lookup_url_kwarg = 'pk'

    def get_vendor_profile(self):
        try:
            return self.request.user.vendor_profile
        except VendorProfile.DoesNotExist:
            return None

    def get_object(self):
        vendor = self.get_vendor_profile()
        if not vendor:
            raise NotFound(detail="Vendor profile not available.")
        obj = get_object_or_404(VendorMedicine, pk=self.kwargs.get(self.lookup_url_kwarg), vendor=vendor)
        return obj

    def patch(self, request, *args, **kwargs):
        inst = self.get_object()
        serializer = self.get_serializer(inst, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        inst = self.get_object()
        inst.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VendorOrderListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = VendorOrderSerializer

    def get_vendor_profile(self):
        try:
            return self.request.user.vendor_profile
        except VendorProfile.DoesNotExist:
            return None

    def get_queryset(self):
        vendor = self.get_vendor_profile()
        if not vendor:
            return VendorOrder.objects.none()
        return VendorOrder.objects.filter(vendor=vendor).order_by('-order_time')

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


class VendorOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = VendorOrderSerializer
    lookup_url_kwarg = 'order_pk'

    def get_vendor_profile(self):
        try:
            return self.request.user.vendor_profile
        except VendorProfile.DoesNotExist:
            return None

    def get_object(self):
        vendor = self.get_vendor_profile()
        if not vendor:
            raise ValidationError({"detail": "Vendor profile not available."})
        pk = self.kwargs.get(self.lookup_url_kwarg)
        obj = get_object_or_404(VendorOrder, pk=pk, vendor=vendor)
        return obj

    def patch(self, request, *args, **kwargs):
        inst = self.get_object()
        serializer = self.get_serializer(inst, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        inst = self.get_object()
        inst.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VendorPrescriptionListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = VendorPrescriptionSerializer

    def get_vendor_profile(self):
        try:
            return self.request.user.vendor_profile
        except VendorProfile.DoesNotExist:
            return None

    def get_queryset(self):
        vendor = self.get_vendor_profile()
        if not vendor:
            return VendorPrescription.objects.none()
        return VendorPrescription.objects.filter(vendor=vendor).order_by('-uploaded_time')

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


class ApprovePrescriptionView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = VendorPrescriptionSerializer
    lookup_url_kwarg = 'pk'

    def get_vendor_profile(self):
        try:
            return self.request.user.vendor_profile
        except VendorProfile.DoesNotExist:
            return None

    def post(self, request, *args, **kwargs):
        vendor = self.get_vendor_profile()
        if not vendor:
            raise ValidationError({"detail": "Vendor profile not available."})
        pk = kwargs.get(self.lookup_url_kwarg)
        presc = get_object_or_404(VendorPrescription, pk=pk, vendor=vendor)
        presc.status = 'approved'
        presc.save()
        if presc.order:
            presc.order.status = 'ready'
            presc.order.save()
        return Response(self.get_serializer(presc).data)


class RejectPrescriptionView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = VendorPrescriptionSerializer
    lookup_url_kwarg = 'pk'

    def get_vendor_profile(self):
        try:
            return self.request.user.vendor_profile
        except VendorProfile.DoesNotExist:
            return None

    def post(self, request, *args, **kwargs):
        vendor = self.get_vendor_profile()
        if not vendor:
            raise ValidationError({"detail": "Vendor profile not available."})
        pk = kwargs.get(self.lookup_url_kwarg)
        presc = get_object_or_404(VendorPrescription, pk=pk, vendor=vendor)
        presc.status = 'rejected'
        presc.save()
        if presc.order:
            presc.order.status = 'cancelled'
            presc.order.save()
        return Response(self.get_serializer(presc).data)


# -------------------------
# Public (user-facing) APIs
# GET /api/vendor/public/medicines/
# -------------------------
class PublicMedicineListView(generics.ListAPIView):
    """
    Public endpoint — user side (no login required)
    Returns list of ALL vendor medicines
    """
    queryset = VendorMedicine.objects.all().order_by('-created_at')
    serializer_class = PublicMedicineSerializer
    permission_classes = []  # allow any (no auth)
