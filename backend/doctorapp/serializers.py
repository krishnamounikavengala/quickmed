# # doctorapp/serializers.py
# from rest_framework import serializers
# from .models import DoctorProfile


# class DoctorProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DoctorProfile
#         fields = [
#             "id",
#             "full_name",
#             "email",
#             "phone",
#             "specialization",
#             "license_number",
#             "experience",
#             "hospital",
#             "address",
#             "city",
#             "state",
#             "pincode",
#             "profile_image",
#         ]

#     def validate_phone(self, value):
#         if value and len(value) < 10:
#             raise serializers.ValidationError("Enter a valid phone number.")
#         return value

#     def validate_pincode(self, value):
#         if value and value.isdigit() and len(value) != 6:
#             raise serializers.ValidationError("Pincode must be 6 digits.")
#         return value




# doctorapp/serializers.py
from rest_framework import serializers
from .models import DoctorProfile


class DoctorProfileSerializer(serializers.ModelSerializer):
    """
    Simple serializer: anni fields optional, partial update easy ga jarugutundi.
    """
    email = serializers.EmailField(required=False, allow_blank=True)

    class Meta:
        model = DoctorProfile
        fields = [
            "id",
            "full_name",
            "phone",
            "specialization",
            "license_number",
            "experience",
            "hospital",
            "address",
            "city",
            "state",
            "pincode",
            "created_at",
            "updated_at",
            "email",
            "profile_image",
        ]
        extra_kwargs = {
            "full_name": {"required": False, "allow_blank": True},
            "phone": {"required": False, "allow_blank": True},
            "specialization": {"required": False, "allow_blank": True},
            "license_number": {"required": False, "allow_blank": True},
            "experience": {"required": False, "allow_blank": True},
            "hospital": {"required": False, "allow_blank": True},
            "address": {"required": False, "allow_blank": True},
            "city": {"required": False, "allow_blank": True},
            "state": {"required": False, "allow_blank": True},
            "pincode": {"required": False, "allow_blank": True},
            "profile_image": {"required": False, "allow_null": True},
        }
