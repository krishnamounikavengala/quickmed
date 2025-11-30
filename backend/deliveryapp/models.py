from django.db import models
from django.conf import settings

VEHICLE_CHOICES = [
    ('Motorcycle', 'Motorcycle'),
    ('Scooter', 'Scooter'),
    ('Bicycle', 'Bicycle'),
    ('Car', 'Car'),
]

class DeliveryProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='delivery_profile')
    phone = models.CharField(max_length=20, blank=True, null=True)
    current_location = models.CharField(max_length=200, blank=True, null=True)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_CHOICES, default='Motorcycle')
    vehicle_number = models.CharField(max_length=50, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)

    # performance stats (update from backend logic)
    joined_date = models.DateTimeField(auto_now_add=True)
    total_deliveries = models.PositiveIntegerField(default=0)
    rating = models.FloatField(default=0.0)
    completion_rate = models.CharField(max_length=20, default='0%')
    response_time = models.CharField(max_length=50, blank=True, default='—')
    average_rating = models.FloatField(default=0.0)

    def __str__(self):
        return f"DeliveryProfile: {self.user} ({self.vehicle_type})"
