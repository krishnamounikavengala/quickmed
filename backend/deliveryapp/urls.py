from django.urls import path
from .views import DeliveryProfileView

urlpatterns = [
    path('profile/', DeliveryProfileView.as_view(), name='delivery-profile'),
]
