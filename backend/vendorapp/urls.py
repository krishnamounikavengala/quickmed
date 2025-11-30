

# # vendorapp/urls.py
# from django.urls import path
# from .views import VendorProfileView

# urlpatterns = [
#     path('profile/', VendorProfileView.as_view(), name='vendor-profile'),
# ]


#################################################################################################################################
# # vendorapp/urls.py
# from django.urls import path
# from .views import (
#     VendorProfileView,
#     VendorMedicineListCreateView, VendorMedicineDetailView,
#     VendorOrderListView, VendorOrderDetailView,
#     VendorPrescriptionListView, ApprovePrescriptionView, RejectPrescriptionView
# )

# urlpatterns = [
#     # profile
#     path('profile/', VendorProfileView.as_view(), name='vendor-profile'),

#     # medicines
#     path('medicines/', VendorMedicineListCreateView.as_view(), name='vendor-medicines'),
#     path('medicines/<int:pk>/', VendorMedicineDetailView.as_view(), name='vendor-medicine-detail'),

#     # orders
#     path('orders/', VendorOrderListView.as_view(), name='vendor-orders'),
#     path('orders/<int:order_pk>/', VendorOrderDetailView.as_view(), name='vendor-order-detail'),

#     # prescriptions
#     path('prescriptions/', VendorPrescriptionListView.as_view(), name='vendor-prescriptions'),
#     path('prescriptions/<int:pk>/approve/', ApprovePrescriptionView.as_view(), name='vendor-prescription-approve'),
#     path('prescriptions/<int:pk>/reject/', RejectPrescriptionView.as_view(), name='vendor-prescription-reject'),
# ]

# # vendorapp/urls.py
# from django.urls import path
# from .views import (
#     VendorProfileView,
#     VendorMedicineListCreateView, VendorMedicineDetailView,
#     VendorOrderListView, VendorOrderDetailView,
#     VendorPrescriptionListView, ApprovePrescriptionView, RejectPrescriptionView
# )

# urlpatterns = [
#     # profile
#     path('profile/', VendorProfileView.as_view(), name='vendor-profile'),

#     # medicines
#     path('medicines/', VendorMedicineListCreateView.as_view(), name='vendor-medicines'),
#     path('medicines/<int:pk>/', VendorMedicineDetailView.as_view(), name='vendor-medicine-detail'),

#     # orders
#     path('orders/', VendorOrderListView.as_view(), name='vendor-orders'),
#     path('orders/<int:order_pk>/', VendorOrderDetailView.as_view(), name='vendor-order-detail'),

#     # prescriptions
#     path('prescriptions/', VendorPrescriptionListView.as_view(), name='vendor-prescriptions'),
#     path('prescriptions/<int:pk>/approve/', ApprovePrescriptionView.as_view(), name='vendor-prescription-approve'),
#     path('prescriptions/<int:pk>/reject/', RejectPrescriptionView.as_view(), name='vendor-prescription-reject'),
# ]

####################################################################################################
#to dispaly the medicine in userdashboard
from django.urls import path
from .views import (
    VendorProfileView,
    VendorMedicineListCreateView, VendorMedicineDetailView,
    VendorOrderListView, VendorOrderDetailView,
    VendorPrescriptionListView, ApprovePrescriptionView, RejectPrescriptionView,
    PublicMedicineListView
)

urlpatterns = [
    path('profile/', VendorProfileView.as_view()),

    path('medicines/', VendorMedicineListCreateView.as_view()),
    path('medicines/<int:pk>/', VendorMedicineDetailView.as_view()),

    path('orders/', VendorOrderListView.as_view()),
    path('orders/<int:order_pk>/', VendorOrderDetailView.as_view()),

    path('prescriptions/', VendorPrescriptionListView.as_view()),
    path('prescriptions/<int:pk>/approve/', ApprovePrescriptionView.as_view()),
    path('prescriptions/<int:pk>/reject/', RejectPrescriptionView.as_view()),

    # ⭐ USER DASHBOARD MEDICINE API
    path('public/medicines/', PublicMedicineListView.as_view()),
]
