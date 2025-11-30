from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import DeliveryProfile

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_delivery_profile(sender, instance, created, **kwargs):
    if created:
        DeliveryProfile.objects.create(user=instance)
    else:
        # ensure profile exists for existing user (useful when migrating)
        DeliveryProfile.objects.get_or_create(user=instance)
