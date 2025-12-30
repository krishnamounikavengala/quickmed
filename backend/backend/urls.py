# backend/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT Auth
    path('api/accounts/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/accounts/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Other apps
    path('api/accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('api/user/', include(('userapp.urls', 'userapp'), namespace='userapp')),
    path('api/delivery/', include(('deliveryapp.urls', 'deliveryapp'), namespace='deliveryapp')),
    path('api/vendor/', include(('vendorapp.urls', 'vendorapp'), namespace='vendorapp')),

    # ✅ DOCTOR APP mounted here
    # Final URL = /api/doctors/ + (doctorapp.urls lo pattern)
    path('api/doctors/', include(('doctorapp.urls', 'doctorapp'), namespace='doctorapp')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
