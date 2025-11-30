




import os
from django.db import models
from django.conf import settings
from django.utils import timezone

def vendor_image_path(instance, filename):
    """
    Migration-safe upload path helper required by older migrations.
    Produces: vendor_profiles/<user_id>/<timestamp>_<safe_filename>.<ext>
    """
    base, ext = os.path.splitext(filename)
    timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
    user_id = getattr(instance.user, 'id', 'unknown')
    safe_base = "".join(c for c in base if c.isalnum() or c in (' ', '-', '_')).rstrip()
    return f"vendor_profiles/{user_id}/{timestamp}_{safe_base}{ext}"


class VendorProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='vendor_profile'
    )
    phone = models.CharField(max_length=20, blank=True, null=True)
    pharmacy_name = models.CharField(max_length=255, blank=True, null=True)
    license_number = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    profile_image = models.ImageField(upload_to=vendor_image_path, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return getattr(self.user, 'email', str(self.user))


class VendorMedicine(models.Model):
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, related_name='medicines')
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=120, blank=True, null=True)
    quantity = models.IntegerField(default=0)
    min_stock = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    expiry_date = models.DateField(blank=True, null=True)
    prescription_required = models.BooleanField(default=False)
    supplier = models.CharField(max_length=255, blank=True, null=True)
    batch_no = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        vendor_email = getattr(self.vendor.user, 'email', 'unknown')
        return f"{self.name} ({vendor_email})"


class VendorOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('ready', 'Ready'),
        ('picked', 'Picked'),
        ('cancelled', 'Cancelled'),
    ]

    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, related_name='orders')
    order_id = models.CharField(max_length=100, unique=True)
    customer_name = models.CharField(max_length=255, blank=True, null=True)
    customer_phone = models.CharField(max_length=20, blank=True, null=True)
    items = models.JSONField(default=list)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    order_time = models.DateTimeField(default=timezone.now)
    delivery_type = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    prescription_required = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        vendor_email = getattr(self.vendor.user, 'email', 'unknown')
        return f"{self.order_id} - {vendor_email}"


class VendorPrescription(models.Model):
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, related_name='prescriptions')
    order = models.ForeignKey(VendorOrder, on_delete=models.SET_NULL, null=True, blank=True, related_name='prescriptions')
    image = models.ImageField(upload_to='vendor_prescriptions/', blank=True, null=True)
    uploaded_time = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, default='pending')
    doctor_name = models.CharField(max_length=255, blank=True, null=True)
    customer_name = models.CharField(max_length=255, blank=True, null=True)
    medicines = models.JSONField(default=list, blank=True)

    def __str__(self):
        vendor_email = getattr(self.vendor.user, 'email', 'unknown')
        return f"RX {self.id} - {vendor_email}"


###########################################################################################################################################