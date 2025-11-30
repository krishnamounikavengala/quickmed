

######################################################################################################################################



# # vendorapp/serializers.py
# from rest_framework import serializers
# from .models import VendorProfile, VendorMedicine, VendorOrder, VendorPrescription


# class VendorUserSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     email = serializers.EmailField(allow_blank=True, required=False)
#     first_name = serializers.CharField(allow_blank=True, required=False)
#     last_name = serializers.CharField(allow_blank=True, required=False)
#     username = serializers.CharField(allow_blank=True, required=False)


# class VendorProfileSerializer(serializers.ModelSerializer):
#     user = VendorUserSerializer(read_only=True)
#     profile_image = serializers.ImageField(required=False, allow_null=True)

#     class Meta:
#         model = VendorProfile
#         fields = [
#             'id', 'user', 'phone', 'pharmacy_name', 'license_number',
#             'address', 'city', 'state', 'pincode', 'profile_image',
#         ]


# # Medicine serializers
# class VendorMedicineSerializer(serializers.ModelSerializer):
#     vendor = serializers.PrimaryKeyRelatedField(read_only=True)

#     class Meta:
#         model = VendorMedicine
#         fields = [
#             'id', 'vendor', 'name', 'category', 'quantity', 'min_stock',
#             'price', 'expiry_date', 'prescription_required', 'supplier',
#             'batch_no', 'created_at', 'updated_at'
#         ]
#         read_only_fields = ['id', 'vendor', 'created_at', 'updated_at']


# class VendorMedicineCreateSerializer(serializers.ModelSerializer):
#     """
#     Use this serializer for creating VendorMedicine objects.
#     The view should pass `context={'vendor': vendor, 'request': request}` but
#     this serializer will also try to resolve vendor from request.user as a fallback.
#     """
#     class Meta:
#         model = VendorMedicine
#         fields = [
#             'id', 'name', 'category', 'quantity', 'min_stock',
#             'price', 'expiry_date', 'prescription_required', 'supplier',
#             'batch_no'
#         ]

#     def validate_quantity(self, v):
#         if v is None:
#             return 0
#         return v

#     def create(self, validated_data):
#         # First try to get vendor from context (the view should pass it).
#         vendor = self.context.get('vendor')
#         # As a fallback, try to get via request.user (if request provided)
#         if not vendor:
#             request = self.context.get('request')
#             if request and getattr(request, 'user', None) and not request.user.is_anonymous:
#                 try:
#                     vendor = request.user.vendor_profile
#                 except VendorProfile.DoesNotExist:
#                     vendor = None

#         if not vendor:
#             # Raise ValidationError in a form DRF will present as 400 with helpful text
#             raise serializers.ValidationError(["Vendor profile not available."])

#         return VendorMedicine.objects.create(vendor=vendor, **validated_data)


# # Simple serializers for orders & prescriptions (can be extended)
# class VendorOrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = VendorOrder
#         fields = '__all__'


# class VendorPrescriptionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = VendorPrescription
#         fields = '__all__'



#################################################################################################
#to show in userdashboard

# vendorapp/serializers.py
from rest_framework import serializers
from .models import VendorProfile, VendorMedicine, VendorOrder, VendorPrescription

# ---------------- Vendor User Info ----------------
class VendorUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(allow_blank=True, required=False)
    first_name = serializers.CharField(allow_blank=True, required=False)
    last_name = serializers.CharField(allow_blank=True, required=False)
    username = serializers.CharField(allow_blank=True, required=False)


# ---------------- Vendor Profile ----------------
class VendorProfileSerializer(serializers.ModelSerializer):
    user = VendorUserSerializer(read_only=True)
    profile_image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = VendorProfile
        fields = [
            'id', 'user', 'phone', 'pharmacy_name', 'license_number',
            'address', 'city', 'state', 'pincode', 'profile_image',
        ]
        read_only_fields = ['id', 'user']


# ---------------- Medicines ----------------
class VendorMedicineSerializer(serializers.ModelSerializer):
    vendor = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = VendorMedicine
        fields = [
            'id', 'vendor', 'name', 'category', 'quantity', 'min_stock',
            'price', 'expiry_date', 'prescription_required', 'supplier',
            'batch_no', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'vendor', 'created_at', 'updated_at']


class VendorMedicineCreateSerializer(serializers.ModelSerializer):
    """
    Serializer used for creation. The view must pass context={'vendor': vendor}
    so create() can attach the proper VendorProfile.
    """
    # allow price as string or numeric input
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, default='0.00')
    quantity = serializers.IntegerField(required=False, default=0)
    min_stock = serializers.IntegerField(required=False, default=0)
    prescription_required = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = VendorMedicine
        fields = [
            'id', 'name', 'category', 'quantity', 'min_stock',
            'price', 'expiry_date', 'prescription_required', 'supplier',
            'batch_no'
        ]
        read_only_fields = ['id']

    def validate_quantity(self, value):
        if value is None:
            return 0
        if value < 0:
            raise serializers.ValidationError("Quantity cannot be negative.")
        return int(value)

    def validate_min_stock(self, value):
        if value is None:
            return 0
        if value < 0:
            raise serializers.ValidationError("Min stock cannot be negative.")
        return int(value)

    def validate_price(self, value):
        try:
            # DecimalField already ensures format but double-check
            if value is None:
                return '0.00'
            return value
        except Exception:
            raise serializers.ValidationError("Invalid price value.")

    def create(self, validated_data):
        """
        Create medicine attached to vendor from context.
        Raises ValidationError if vendor missing.
        """
        vendor = self.context.get('vendor')
        if not vendor:
            # Return as DRF validation error (frontend receives JSON)
            raise serializers.ValidationError({"detail": "Vendor profile not available."})
        # Ensure integer fields and defaults
        validated_data.setdefault('quantity', 0)
        validated_data.setdefault('min_stock', 0)
        validated_data.setdefault('price', '0.00')
        validated_data.setdefault('prescription_required', False)
        med = VendorMedicine.objects.create(vendor=vendor, **validated_data)
        return med


# -------- USER (Frontend) PUBLIC MEDICINE VIEW --------
# class PublicMedicineSerializer(serializers.ModelSerializer):
#     vendor_name = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         model = VendorMedicine
#         fields = [
#             'id', 'name', 'category', 'price', 'expiry_date',
#             'prescription_required', 'supplier', 'batch_no', 'vendor_name'
#         ]

#     def get_vendor_name(self, obj):
#         try:
#             return obj.vendor.pharmacy_name or getattr(obj.vendor.user, 'username', None) or getattr(obj.vendor.user, 'email', None)
#         except Exception:
#             return None


class PublicMedicineSerializer(serializers.ModelSerializer):
    vendor_name = serializers.SerializerMethodField(read_only=True)
    vendor_id = serializers.SerializerMethodField(read_only=True)
    # if your VendorMedicine has an image field, uncomment:
    # image = serializers.ImageField(source='image', required=False, allow_null=True)

    class Meta:
        model = VendorMedicine
        fields = [
            'id', 'name', 'category', 'price', 'expiry_date',
            'prescription_required', 'supplier', 'batch_no',
            'vendor_name', 'vendor_id', # 'image'
        ]

    def get_vendor_name(self, obj):
        try:
            return obj.vendor.pharmacy_name or getattr(obj.vendor.user, 'username', None) or getattr(obj.vendor.user, 'email', None)
        except Exception:
            return None

    def get_vendor_id(self, obj):
        try:
            return obj.vendor.id
        except Exception:
            return None


# ---------------- Orders ----------------
class VendorOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorOrder
        fields = '__all__'


# ---------------- Prescriptions ----------------
class VendorPrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorPrescription
        fields = '__all__'
