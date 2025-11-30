

# userapp/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    # Accept flat payload; allow partial updates
    full_name = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    profile_photo = serializers.SerializerMethodField(read_only=True)  # return URL

    class Meta:
        model = UserProfile
        fields = [
            "full_name",
            "email",
            "phone",
            "address",
            "city",
            "pincode",
            "date_of_birth",
            "age",
            "gender",
            "profile_photo",
        ]
        read_only_fields = ["profile_photo"]

    def get_profile_photo(self, obj):
        request = self.context.get("request")
        if obj.profile_photo:
            # return absolute URL if request available
            try:
                url = obj.profile_photo.url
            except Exception:
                url = None
            if request and url:
                return request.build_absolute_uri(url)
            return url
        return None

    def update(self, instance, validated_data):
        # update profile fields
        profile_fields = [
            "full_name",
            "email",
            "phone",
            "address",
            "city",
            "pincode",
            "date_of_birth",
            "age",
            "gender",
        ]
        for f in profile_fields:
            if f in validated_data:
                setattr(instance, f, validated_data.get(f))
        instance.save()

        # also update linked User fields where applicable
        user = instance.user
        user_changed = False
        # We keep primary email on User in sync if frontend changes email
        if "email" in validated_data and validated_data.get("email"):
            user.email = validated_data.get("email")
            user_changed = True
        # if your User model has first_name/last_name or full_name, you can map accordingly
        if "full_name" in validated_data and validated_data.get("full_name"):
            # If your user model stores full_name, set it; otherwise may set first_name
            if hasattr(user, "full_name"):
                user.full_name = validated_data.get("full_name")
                user_changed = True
            else:
                # try splitting into first/last
                full = validated_data.get("full_name").strip()
                parts = full.split(" ", 1)
                user.first_name = parts[0]
                user.last_name = parts[1] if len(parts) > 1 else ""
                user_changed = True

        if user_changed:
            user.save()

        return instance


class UserProfileReadSerializer(serializers.ModelSerializer):
    # separate read serializer that includes profile_photo url
    profile_photo = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            "full_name",
            "email",
            "phone",
            "address",
            "city",
            "pincode",
            "date_of_birth",
            "age",
            "gender",
            "profile_photo",
        ]

    def get_profile_photo(self, obj):
        request = self.context.get("request")
        if obj.profile_photo:
            try:
                url = obj.profile_photo.url
            except Exception:
                url = None
            if request and url:
                return request.build_absolute_uri(url)
            return url
        return None
