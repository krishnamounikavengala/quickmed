# # userapp/urls.py

# from django.urls import path
# from .views import (
#     ProfileRetrieveUpdateAPIView,
#     ProfilePhotoUploadAPIView,
#     ProfilePhotoRemoveAPIView,
# )

# app_name = "userapp"

# urlpatterns = [
#     path("me/", ProfileRetrieveUpdateAPIView.as_view(), name="profile-detail"),
#     path("me/photo/", ProfilePhotoUploadAPIView.as_view(), name="profile-photo-upload"),
#     path("me/photo/remove/", ProfilePhotoRemoveAPIView.as_view(), name="profile-photo-remove"),
# ]


# # userapp/urls.py
# from django.urls import path
# from .views import (
#     ProfileRetrieveUpdateAPIView,
#     ProfilePhotoUploadAPIView,
#     ProfilePhotoRemoveAPIView,
# )

# app_name = "userapp"

# urlpatterns = [
#     path("me/", ProfileRetrieveUpdateAPIView.as_view(), name="profile-detail"),
#     path("me/photo/", ProfilePhotoUploadAPIView.as_view(), name="profile-photo-upload"),
#     path("me/photo/remove/", ProfilePhotoRemoveAPIView.as_view(), name="profile-photo-remove"),
# ]




# userapp/urls.py
from django.urls import path
from .views import (
    ProfileRetrieveUpdateAPIView,
    ProfilePhotoUploadAPIView,
    ProfilePhotoRemoveAPIView,
)

app_name = "userapp"

urlpatterns = [
    path("me/", ProfileRetrieveUpdateAPIView.as_view(), name="profile-detail"),
    path("me/photo/", ProfilePhotoUploadAPIView.as_view(), name="profile-photo-upload"),
    path("me/photo/remove/", ProfilePhotoRemoveAPIView.as_view(), name="profile-photo-remove"),
]
