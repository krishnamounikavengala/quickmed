# # doctorapp/urls.py
# from django.urls import path
# from .views import MyDoctorProfileView

# urlpatterns = [
#     # GET + PATCH:
#     # /api/doctors/  (root from backend.urls)
#     # + "me/"        (ikkada pattern)
#     # = /api/doctors/me/
#     path("me/", MyDoctorProfileView.as_view(), name="my-doctor-profile"),
# ]


# doctorapp/urls.py
from django.urls import path
from .views import DoctorMeView

urlpatterns = [
    path("me/", DoctorMeView.as_view(), name="doctor-me"),
]
