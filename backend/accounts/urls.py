# # from django.urls import path
# # from .views import RegisterView, ProfileView
# # from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# # urlpatterns = [
# #     path('register/', RegisterView.as_view(), name='register'),
# #     path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # login
# #     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
# #     path('profile/', ProfileView.as_view(), name='profile'),
# # ]



# # accounts/urls.py
# from django.urls import path
# from .views import RegisterView, ProfileView
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# urlpatterns = [
#     path('register/', RegisterView.as_view(), name='register'),
#     path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#     path('profile/', ProfileView.as_view(), name='profile'),
# ]
# accounts/urls.py
from django.urls import path
from .views import RegisterAPIView, ProfileAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='account-register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),
]
