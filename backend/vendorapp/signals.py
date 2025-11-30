# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth.models import User
# from .models import VendorProfile

# @receiver(post_save, sender=User)
# def create_vendor_profile(sender, instance, created, **kwargs):
#     if created:
#         VendorProfile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_vendor_profile(sender, instance, **kwargs):
#     if hasattr(instance, 'vendor_profile'):
#         instance.vendor_profile.save()


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import VendorProfile

User = get_user_model()

@receiver(post_save, sender=User)
def create_vendor_profile(sender, instance, created, **kwargs):
    """
    Auto-create VendorProfile when a user is created.
    If you don't want every user to have a vendor_profile (only vendors),
    either guard this with a flag on the user (e.g. is_vendor) or remove it.
    """
    if created:
        VendorProfile.objects.create(user=instance)          #5

@receiver(post_save, sender=User)
def save_vendor_profile(sender, instance, **kwargs):
    if hasattr(instance, 'vendor_profile'):
        instance.vendor_profile.save()


########################################################################################################################################