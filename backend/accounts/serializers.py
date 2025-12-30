







# # accounts/serializers.py
# from rest_framework import serializers
# from django.utils.text import slugify
# from django.contrib.auth import get_user_model
# from rest_framework_simplejwt.tokens import RefreshToken

# User = get_user_model()

# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'email', 'username', 'first_name', 'last_name', 'phone', 'user_type')

# class RegisterSerializer(serializers.ModelSerializer):
#     confirm_password = serializers.CharField(write_only=True, required=True)
#     username = serializers.CharField(required=False, allow_blank=True)

#     class Meta:
#         model = User
#         fields = ('id', 'email', 'username', 'first_name', 'last_name', 'phone', 'user_type', 'password', 'confirm_password')
#         extra_kwargs = {
#             'password': {'write_only': True, 'min_length': 8},
#             'first_name': {'required': False, 'allow_blank': True},
#             'last_name': {'required': False, 'allow_blank': True},
#             'phone': {'required': False, 'allow_blank': True},
#             'user_type': {'required': False, 'allow_blank': True},
#         }

#     def validate(self, attrs):
#         if attrs.get('password') != attrs.get('confirm_password'):
#             raise serializers.ValidationError({'confirm_password': 'Passwords do not match.'})
#         return attrs

#     def _generate_username(self, email=None, first_name=None):
#         base = ''
#         if email and '@' in email:
#             base = email.split('@')[0]
#         elif first_name:
#             base = first_name
#         else:
#             base = 'user'
#         candidate = slugify(base)[:30] or 'user'
#         # ensure unique
#         suffix = 0
#         unique = candidate
#         while User.objects.filter(username=unique).exists():
#             suffix += 1
#             unique = f"{candidate}{suffix}"
#         return unique

#     def create(self, validated_data):
#         validated_data.pop('confirm_password', None)
#         username = validated_data.pop('username', None)
#         if not username:
#             username = self._generate_username(email=validated_data.get('email'), first_name=validated_data.get('first_name'))
#         else:
#             username = slugify(username)[:30] or self._generate_username(validated_data.get('email'), validated_data.get('first_name'))
#             # ensure unique
#             base = username
#             suffix = 0
#             unique = base
#             while User.objects.filter(username=unique).exists():
#                 suffix += 1
#                 unique = f"{base}{suffix}"
#             username = unique

#         password = validated_data.pop('password')

#         user = User.objects.create_user(
#             username=username,
#             email=validated_data.get('email'),
#             password=password,
#             first_name=validated_data.get('first_name', ''),
#             last_name=validated_data.get('last_name', '')
#         )

#         # save optional fields
#         phone = validated_data.get('phone', None)
#         user_type = validated_data.get('user_type', None)
#         if phone:
#             user.phone = phone
#         if user_type:
#             user.user_type = user_type
#         user.save()

#         return user

#     def to_representation(self, instance):
#         # When returning the created object, include tokens + user data
#         data = ProfileSerializer(instance).data
#         refresh = RefreshToken.for_user(instance)
#         return {
#             'user': data,
#             'access': str(refresh.access_token),
#             'refresh': str(refresh),
#         }







# accounts/serializers.py
from rest_framework import serializers
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'phone',
            'user_type',
        )


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'phone',
            'user_type',
            'password',
            'confirm_password',
        )
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8},
            'first_name': {'required': False, 'allow_blank': True},
            'last_name': {'required': False, 'allow_blank': True},
            'phone': {'required': False, 'allow_blank': True},
            'user_type': {'required': False, 'allow_blank': True},
        }

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError(
                {'confirm_password': 'Passwords do not match.'}
            )
        return attrs

    def _generate_username(self, email=None, first_name=None):
        base = ''
        if email and '@' in email:
            base = email.split('@')[0]
        elif first_name:
            base = first_name
        else:
            base = 'user'

        candidate = slugify(base)[:30] or 'user'
        # ensure unique
        suffix = 0
        unique = candidate
        while User.objects.filter(username=unique).exists():
            suffix += 1
            unique = f"{candidate}{suffix}"
        return unique

    def create(self, validated_data):
        # confirm_password remove
        validated_data.pop('confirm_password', None)

        # username prepare
        username = validated_data.pop('username', None)
        if not username:
            username = self._generate_username(
                email=validated_data.get('email'),
                first_name=validated_data.get('first_name'),
            )
        else:
            username = slugify(username)[:30] or self._generate_username(
                validated_data.get('email'),
                validated_data.get('first_name'),
            )
            # ensure unique
            base = username
            suffix = 0
            unique = base
            while User.objects.filter(username=unique).exists():
                suffix += 1
                unique = f"{base}{suffix}"
            username = unique

        password = validated_data.pop('password')

        # main user create
        user = User.objects.create_user(
            username=username,
            email=validated_data.get('email'),
            password=password,
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )

        # 🔴 IMPORTANT FIX: make user active
        user.is_active = True

        # optional fields
        phone = validated_data.get('phone', None)
        user_type = validated_data.get('user_type', None)
        if phone:
            user.phone = phone
        if user_type:
            user.user_type = user_type

        user.save()
        return user

    def to_representation(self, instance):
        # Return tokens + user data after registration
        data = ProfileSerializer(instance).data
        refresh = RefreshToken.for_user(instance)
        return {
            'user': data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

