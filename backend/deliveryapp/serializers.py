# # import base64
# # import imghdr
# # import uuid
# # from django.core.files.base import ContentFile
# # from rest_framework import serializers
# # from django.contrib.auth import get_user_model
# # from .models import DeliveryProfile

# # User = get_user_model()

# # class Base64ImageField(serializers.ImageField):
# #     """
# #     Accepts base64-encoded images or normal UploadedFile objects.
# #     """
# #     def to_internal_value(self, data):
# #         # If it's already an uploaded file, let parent handle it
# #         if hasattr(data, 'read'):
# #             return super().to_internal_value(data)

# #         # if string and like data:image/...;base64,...
# #         if isinstance(data, str) and data.startswith('data:'):
# #             # format: data:<mime>;base64,<data>
# #             header, base64_data = data.split(',', 1)
# #             try:
# #                 decoded_file = base64.b64decode(base64_data)
# #             except TypeError:
# #                 raise serializers.ValidationError("Invalid image")

# #             # get file ext
# #             file_ext = imghdr.what(None, decoded_file) or 'jpg'
# #             file_name = f"{uuid.uuid4()}.{file_ext}"
# #             data = ContentFile(decoded_file, name=file_name)
# #             return super().to_internal_value(data)

# #         # if empty string or None -> allow clearing
# #         if data in (None, ''):
# #             return None

# #         return super().to_internal_value(data)

# # class UserMiniSerializer(serializers.ModelSerializer):
# #     fullName = serializers.SerializerMethodField()
# #     email = serializers.EmailField(source='email', read_only=True)
# #     id = serializers.IntegerField(source='id', read_only=True)

# #     class Meta:
# #         model = User
# #         fields = ('id', 'email', 'fullName')

# #     def get_fullName(self, obj):
# #         # adapt to your user model fields
# #         first = getattr(obj, 'first_name', '') or ''
# #         last = getattr(obj, 'last_name', '') or ''
# #         if first or last:
# #             return f"{first} {last}".strip()
# #         # fallback to username or email
# #         return getattr(obj, 'full_name', None) or getattr(obj, 'username', obj.email)

# # class DeliveryProfileSerializer(serializers.ModelSerializer):
# #     user = UserMiniSerializer(read_only=True)
# #     profile_image = Base64ImageField(required=False, allow_null=True)

# #     class Meta:
# #         model = DeliveryProfile
# #         fields = [
# #             'user',
# #             'phone',
# #             'current_location',
# #             'vehicle_type',
# #             'vehicle_number',
# #             'profile_image',
# #             'joined_date',
# #             'total_deliveries',
# #             'rating',
# #             'completion_rate',
# #             'response_time',
# #             'average_rating',
# #         ]
# #         read_only_fields = ['joined_date', 'total_deliveries', 'rating', 'average_rating']










# # backend/deliveryapp/serializers.py
# from rest_framework import serializers
# from django.conf import settings
# from .models import DeliveryProfile
# from PIL import Image, UnidentifiedImageError
# from io import BytesIO

# MAX_IMAGE_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB
# ALLOWED_IMAGE_FORMATS = ("JPEG", "PNG", "WEBP")  # uppercase format names returned by PIL

# class DeliveryProfileSerializer(serializers.ModelSerializer):
#     # if your model field name differs, adjust accordingly
#     profile_image = serializers.ImageField(required=False, allow_null=True, use_url=True)

#     class Meta:
#         model = DeliveryProfile
#         # choose fields you need to expose/update; adjust if your model has different names
#         fields = [
#             "id",
#             "user",
#             "phone",
#             "current_location",
#             "vehicle_type",
#             "vehicle_number",
#             "profile_image",
#             "joined_date",
#             "total_deliveries",
#             "rating",
#             "completion_rate",
#             "response_time",
#             "average_rating",
#         ]
#         read_only_fields = ("id", "user", "joined_date", "total_deliveries", "rating", "completion_rate", "response_time", "average_rating")

#     def validate_profile_image(self, value):
#         """
#         Validate uploaded image using Pillow:
#         - ensure file size <= MAX_IMAGE_SIZE_BYTES
#         - ensure format is one of allowed formats
#         """
#         if not value:
#             return value

#         # size check
#         try:
#             size = value.size
#         except Exception:
#             size = None

#         if size and size > MAX_IMAGE_SIZE_BYTES:
#             raise serializers.ValidationError("Image file size must be less than 5MB.")

#         # Try to open image with Pillow to verify format
#         try:
#             # value might be an InMemoryUploadedFile; ensure we don't break file pointer
#             value.seek(0)
#             img = Image.open(value)
#             img_format = img.format  # e.g., 'JPEG', 'PNG'
#             # Pillow may lazy-load; force load to catch errors
#             img.verify()
#         except UnidentifiedImageError:
#             raise serializers.ValidationError("Uploaded file is not a valid image.")
#         except Exception as e:
#             # For safety, allow other exceptions to bubble as validation error
#             raise serializers.ValidationError("Could not process the uploaded image.") from e
#         finally:
#             # Reset pointer so Django can save the file later
#             try:
#                 value.seek(0)
#             except Exception:
#                 pass

#         if img_format not in ALLOWED_IMAGE_FORMATS:
#             raise serializers.ValidationError(
#                 f"Unsupported image format ({img_format}). Allowed formats: JPG, PNG, WebP."
#             )

#         return value

#     def update(self, instance, validated_data):
#         """
#         Custom update - if profile_image is present, it will be handled by the ImageField.
#         """
#         # handle simple fields
#         for attr in ("phone", "current_location", "vehicle_type", "vehicle_number"):
#             if attr in validated_data:
#                 setattr(instance, attr, validated_data[attr])

#         # profile_image may be in validated_data (ImageField)
#         if "profile_image" in validated_data:
#             instance.profile_image = validated_data.get("profile_image")

#         instance.save()
#         return instance



# backend/deliveryapp/serializers.py
from rest_framework import serializers
from .models import DeliveryProfile
from PIL import Image, UnidentifiedImageError

MAX_IMAGE_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB
ALLOWED_IMAGE_FORMATS = ("JPEG", "PNG", "WEBP")  # Pillow format names

class DeliveryProfileSerializer(serializers.ModelSerializer):
    # keep use_url=True so DRF produces absolute URLs when request is provided in context
    profile_image = serializers.ImageField(required=False, allow_null=True, use_url=True)

    class Meta:
        model = DeliveryProfile
        fields = [
            "id",
            "user",
            "phone",
            "current_location",
            "vehicle_type",
            "vehicle_number",
            "profile_image",
            "joined_date",
            "total_deliveries",
            "rating",
            "completion_rate",
            "response_time",
            "average_rating",
        ]
        read_only_fields = ("id", "user", "joined_date", "total_deliveries", "rating", "completion_rate", "response_time", "average_rating")

    def validate_profile_image(self, value):
        """
        Validate uploaded image using Pillow:
        - ensure file size <= MAX_IMAGE_SIZE_BYTES
        - ensure format is one of allowed formats
        """
        if not value:
            return value

        # size check
        try:
            size = value.size
        except Exception:
            size = None

        if size and size > MAX_IMAGE_SIZE_BYTES:
            raise serializers.ValidationError("Image file size must be less than 5MB.")

        # Try to open image with Pillow to verify format
        try:
            value.seek(0)
            img = Image.open(value)
            img_format = img.format  # e.g., 'JPEG', 'PNG'
            img.verify()  # ensure not corrupted
        except UnidentifiedImageError:
            raise serializers.ValidationError("Uploaded file is not a valid image.")
        except Exception:
            raise serializers.ValidationError("Could not process the uploaded image.")
        finally:
            try:
                value.seek(0)
            except Exception:
                pass

        if img_format not in ALLOWED_IMAGE_FORMATS:
            raise serializers.ValidationError(
                f"Unsupported image format ({img_format}). Allowed formats: JPG, PNG, WebP."
            )

        return value

    def update(self, instance, validated_data):
        """
        Custom update - if profile_image is present, it will be handled by the ImageField.
        """
        # simple update of fields
        for attr in ("phone", "current_location", "vehicle_type", "vehicle_number"):
            if attr in validated_data:
                setattr(instance, attr, validated_data[attr])

        # handle image if present
        if "profile_image" in validated_data:
            instance.profile_image = validated_data.get("profile_image")

        instance.save()
        return instance
