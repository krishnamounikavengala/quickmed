



from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Token endpoints (SimpleJWT)
    # POST /api/accounts/token/       -> { access, refresh }
    # POST /api/accounts/token/refresh/ -> { access }
    path('api/accounts/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/accounts/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Include accounts app URLs (registration, profile endpoints if implemented)
    path('api/accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),

    # Existing apps
    path('api/user/', include(('userapp.urls', 'userapp'), namespace='userapp')),
    path('api/delivery/', include(('deliveryapp.urls', 'deliveryapp'), namespace='deliveryapp')),

    # Vendor app endpoints (vendor profile, medicines, orders, prescriptions)
    path('api/vendor/', include(('vendorapp.urls', 'vendorapp'), namespace='vendorapp')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    