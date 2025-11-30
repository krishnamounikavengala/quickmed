# # accounts/models.py
# from django.contrib.auth.models import AbstractUser
# from django.db import models

# class User(AbstractUser):
#     USER_TYPES = (
#         ('user', 'User'),
#         ('vendor', 'Vendor'),
#         ('delivery', 'Delivery'),
#         ('doctor', 'Doctor'),
#     )

#     email = models.EmailField(unique=True)
#     phone = models.CharField(max_length=15, blank=True, null=True)
#     user_type = models.CharField(max_length=20, choices=USER_TYPES, default='user')

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']  # keep username to satisfy AbstractUser fields

#     def __str__(self):
#         return f'{self.email} ({self.user_type})'











# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPES = (
        ('user', 'User'),
        ('vendor', 'Vendor'),
        ('delivery', 'Delivery'),
        ('doctor', 'Doctor'),
        ('admin', 'Admin'),
    )

    full_name = models.CharField(max_length=120)   # NEW FIELD
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='user')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name']

    def __str__(self):
        return f"{self.full_name} ({self.email})"
