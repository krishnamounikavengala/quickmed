# doctorapp/admin.py
from django.contrib import admin
from .models import DoctorProfile

@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "full_name", "phone", "specialization")
