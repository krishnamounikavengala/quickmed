from django.contrib import admin
from .models import DeliveryProfile

@admin.register(DeliveryProfile)
class DeliveryProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'vehicle_type', 'vehicle_number', 'joined_date')
    search_fields = ('user__email', 'user__username', 'phone', 'vehicle_number')
