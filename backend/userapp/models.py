



# userapp/models.py
from django.db import models
from django.conf import settings

# Use AUTH_USER_MODEL string to avoid circular import issues
User = settings.AUTH_USER_MODEL

def profile_photo_upload_path(instance, filename):
    # store uploaded files under MEDIA_ROOT/profile_photos/<user_id>/<filename>
    return f"profile_photos/user_{instance.user.id}/{filename}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')

    full_name = models.CharField(max_length=150, default="", blank=True)
    email = models.EmailField(max_length=254, default="", blank=True)
    phone = models.CharField(max_length=20, default="", blank=True)
    address = models.CharField(max_length=255, default="", blank=True)
    city = models.CharField(max_length=100, default="", blank=True)
    pincode = models.CharField(max_length=10, default="", blank=True)

    date_of_birth = models.DateField(null=True, blank=True, default=None)
    age = models.IntegerField(default=0)

    gender = models.CharField(max_length=20, default="", blank=True)

    # Use ImageField/FileField so uploaded files are handled by Django
    profile_photo = models.ImageField(upload_to=profile_photo_upload_path, null=True, blank=True)

    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        email = getattr(self.user, "email", None) or self.email or str(self.user)
        return f"{email} Profile"
