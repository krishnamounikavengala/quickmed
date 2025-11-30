



# # backend/vendorapp/admin.py
# from django.contrib import admin
# from django.apps import apps
# from django.utils.html import format_html

# # Safely get models (returns None if model not present)
# VendorProfile = apps.get_model('vendorapp', 'VendorProfile')
# VendorMedicine = apps.get_model('vendorapp', 'VendorMedicine')
# VendorOrder = apps.get_model('vendorapp', 'VendorOrder')
# VendorPrescription = apps.get_model('vendorapp', 'VendorPrescription')

# # Define a safe admin for VendorProfile if the model exists
# if VendorProfile is not None:

#     @admin.register(VendorProfile)
#     class VendorProfileAdmin(admin.ModelAdmin):
#         # Use fields that are likely present on the model.
#         # If you add/remove fields from the model, update this list accordingly.
#         list_display = ('id', 'user_email', 'phone', 'pharmacy_name', 'created_at', 'updated_at')
#         list_select_related = ('user',)
#         search_fields = ('user__email', 'pharmacy_name', 'phone')
#         readonly_fields = ('created_at', 'updated_at')

#         def user_email(self, obj):
#             return getattr(obj.user, 'email', '(no email)')
#         user_email.short_description = 'User Email'
#         user_email.admin_order_field = 'user__email'

# # Register VendorMedicine if exists
# if VendorMedicine is not None:
#     @admin.register(VendorMedicine)
#     class VendorMedicineAdmin(admin.ModelAdmin):
#         list_display = ('id', 'name', 'vendor_email', 'quantity', 'min_stock', 'price', 'expiry_date')
#         search_fields = ('name', 'vendor__user__email', 'batch_no')
#         list_filter = ('prescription_required', 'category')

#         def vendor_email(self, obj):
#             return getattr(obj.vendor.user, 'email', '(no email)')
#         vendor_email.short_description = 'Vendor Email'
#         vendor_email.admin_order_field = 'vendor__user__email'

# # Register VendorOrder if exists
# if VendorOrder is not None:
#     @admin.register(VendorOrder)
#     class VendorOrderAdmin(admin.ModelAdmin):
#         list_display = ('id', 'order_id', 'vendor_email', 'status', 'total', 'order_time')
#         search_fields = ('order_id', 'vendor__user__email', 'customer_name')
#         list_filter = ('status',)

#         def vendor_email(self, obj):
#             return getattr(obj.vendor.user, 'email', '(no email)')
#         vendor_email.short_description = 'Vendor Email'
#         vendor_email.admin_order_field = 'vendor__user__email'

# # Register VendorPrescription if exists
# if VendorPrescription is not None:
#     @admin.register(VendorPrescription)
#     class VendorPrescriptionAdmin(admin.ModelAdmin):
#         list_display = ('id', 'vendor_email', 'order', 'status', 'uploaded_time')
#         search_fields = ('vendor__user__email',)
#         list_filter = ('status',)

#         def vendor_email(self, obj):
#             return getattr(obj.vendor.user, 'email', '(no email)')
#         vendor_email.short_description = 'Vendor Email'
#         vendor_email.admin_order_field = 'vendor__user__email'



########################################################################################################################################







# vendorapp/admin.py
from django.contrib import admin, messages
from django.apps import apps
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

# Safely fetch models (returns None if not installed)
VendorProfile = apps.get_model('vendorapp', 'VendorProfile')
VendorMedicine = apps.get_model('vendorapp', 'VendorMedicine')
VendorOrder = apps.get_model('vendorapp', 'VendorOrder')
VendorPrescription = apps.get_model('vendorapp', 'VendorPrescription')


# -------------------
# Helper utilities
# -------------------
def _safe_email_from_user(user_obj):
    if not user_obj:
        return '(no user)'
    return getattr(user_obj, 'email', '(no email)')


def _admin_change_link(obj, related_obj, text=None):
    """Return link to admin change page for related_obj (if available)."""
    if not related_obj:
        return '-'
    try:
        app_label = related_obj._meta.app_label
        model_name = related_obj._meta.model_name
        url = reverse(f'admin:{app_label}_{model_name}_change', args=(related_obj.pk,))
        return format_html('<a href="{}">{}</a>', url, text or str(related_obj))
    except Exception:
        return str(related_obj)


# -------------------
# VendorMedicineInline (for VendorProfile admin)
# -------------------
if VendorMedicine is not None:
    class VendorMedicineInline(admin.TabularInline):
        model = VendorMedicine
        extra = 0
        fields = ('name', 'quantity', 'min_stock', 'price', 'expiry_date', 'prescription_required', 'batch_no')
        readonly_fields = ()
        show_change_link = True


# -------------------
# VendorProfile admin
# -------------------
if VendorProfile is not None:

    @admin.register(VendorProfile)
    class VendorProfileAdmin(admin.ModelAdmin):
        list_display = ('id', 'user_email', 'avatar_preview', 'pharmacy_name', 'phone', 'created_at', 'updated_at')
        list_select_related = ('user',)
        search_fields = ('user__email', 'pharmacy_name', 'phone', 'license_number')
        readonly_fields = ('created_at', 'updated_at', 'avatar_preview')
        list_filter = ('state',)
        ordering = ('-created_at',)
        fieldsets = (
            (None, {
                'fields': ('user', 'avatar_preview', 'phone', 'pharmacy_name', 'license_number')
            }),
            (_('Address'), {
                'fields': ('address', 'city', 'state', 'pincode')
            }),
            (_('Timestamps'), {
                'fields': ('created_at', 'updated_at')
            }),
        )

        # show medicines inline if model exists
        inlines = [VendorMedicineInline] if VendorMedicine is not None else []

        def user_email(self, obj):
            return _safe_email_from_user(getattr(obj, 'user', None))
        user_email.short_description = 'User Email'
        user_email.admin_order_field = 'user__email'

        def avatar_preview(self, obj):
            # show small image preview if available
            try:
                url = getattr(obj, 'profile_image').url
                if url:
                    return format_html('<img src="{}" style="width:48px;height:48px;border-radius:6px;object-fit:cover;border:1px solid #ddd" />', url)
            except Exception:
                pass
            return mark_safe('<span style="display:inline-block;width:48px;height:48px;border-radius:6px;background:#f0f0f0;color:#999;text-align:center;line-height:48px">No</span>')
        avatar_preview.short_description = 'Avatar'


# -------------------
# VendorMedicine admin
# -------------------
if VendorMedicine is not None:

    @admin.register(VendorMedicine)
    class VendorMedicineAdmin(admin.ModelAdmin):
        list_display = ('id', 'name', 'vendor_email', 'quantity', 'min_stock', 'price_display', 'expiry_date', 'prescription_required', 'batch_no')
        search_fields = ('name', 'vendor__user__email', 'supplier', 'batch_no')
        list_filter = ('prescription_required', 'category')
        ordering = ('-created_at',)

        def vendor_email(self, obj):
            try:
                return getattr(obj.vendor.user, 'email', '(no email)')
            except Exception:
                return '(no vendor)'
        vendor_email.short_description = 'Vendor Email'
        vendor_email.admin_order_field = 'vendor__user__email'

        def price_display(self, obj):
            try:
                # show price with 2 decimals
                return "{:.2f}".format(float(obj.price))
            except Exception:
                return obj.price
        price_display.short_description = 'Price'


# -------------------
# Admin actions for VendorOrder
# -------------------
def _bulk_status_update(modeladmin, request, queryset, status_value, success_msg):
    try:
        updated = queryset.update(status=status_value)
        modeladmin.message_user(request, _("{count} orders updated: {msg}").format(count=updated, msg=success_msg), level=messages.SUCCESS)
    except Exception as e:
        modeladmin.message_user(request, _("Failed to update orders: {}").format(str(e)), level=messages.ERROR)


# -------------------
# VendorOrder admin
# -------------------
if VendorOrder is not None:

    @admin.register(VendorOrder)
    class VendorOrderAdmin(admin.ModelAdmin):
        list_display = ('id', 'order_id', 'vendor_email', 'status', 'total', 'order_time', 'short_items_preview')
        search_fields = ('order_id', 'vendor__user__email', 'customer_name')
        list_filter = ('status',)
        readonly_fields = ('order_time',)
        ordering = ('-order_time',)
        actions = ('mark_ready', 'mark_picked', 'mark_cancelled')

        def vendor_email(self, obj):
            try:
                return getattr(obj.vendor.user, 'email', '(no email)')
            except Exception:
                return '(no vendor)'
        vendor_email.short_description = 'Vendor Email'
        vendor_email.admin_order_field = 'vendor__user__email'

        def short_items_preview(self, obj):
            try:
                items = getattr(obj, 'items', None)
                if not items:
                    return '-'
                # items may be list/dict - show concise preview
                if isinstance(items, (list, tuple)):
                    preview = ', '.join([str(i.get('name') or i.get('name', 'item')) for i in items[:3]])
                    if len(items) > 3:
                        preview += '…'
                    return preview
                return str(items)[:80]
            except Exception:
                return '-'
        short_items_preview.short_description = 'Items'

        @admin.action(description='Mark selected orders as Ready')
        def mark_ready(self, request, queryset):
            _bulk_status_update(self, request, queryset, 'ready', 'marked ready')

        @admin.action(description='Mark selected orders as Picked')
        def mark_picked(self, request, queryset):
            _bulk_status_update(self, request, queryset, 'picked', 'marked picked')

        @admin.action(description='Mark selected orders as Cancelled')
        def mark_cancelled(self, request, queryset):
            _bulk_status_update(self, request, queryset, 'cancelled', 'marked cancelled')


# -------------------
# Admin actions for VendorPrescription
# -------------------
def _prescription_bulk_status(modeladmin, request, queryset, new_status, success_msg):
    try:
        updated = queryset.update(status=new_status)
        modeladmin.message_user(request, _("{count} prescriptions updated: {msg}").format(count=updated, msg=success_msg), level=messages.SUCCESS)
    except Exception as e:
        modeladmin.message_user(request, _("Failed to update prescriptions: {}").format(str(e)), level=messages.ERROR)


# -------------------
# VendorPrescription admin
# -------------------
if VendorPrescription is not None:

    @admin.register(VendorPrescription)
    class VendorPrescriptionAdmin(admin.ModelAdmin):
        list_display = ('id', 'rx_vendor_email', 'order_link', 'status', 'uploaded_time', 'doctor_name', 'customer_name')
        search_fields = ('vendor__user__email', 'doctor_name', 'customer_name')
        list_filter = ('status',)
        readonly_fields = ('uploaded_time',)
        ordering = ('-uploaded_time',)
        actions = ('approve_selected', 'reject_selected')

        def rx_vendor_email(self, obj):
            try:
                return getattr(obj.vendor.user, 'email', '(no email)')
            except Exception:
                return '(no vendor)'
        rx_vendor_email.short_description = 'Vendor Email'
        rx_vendor_email.admin_order_field = 'vendor__user__email'

        def order_link(self, obj):
            if getattr(obj, 'order', None):
                return _admin_change_link(obj, obj.order, text=str(obj.order.order_id if getattr(obj.order, 'order_id', None) else obj.order.pk))
            return '-'
        order_link.short_description = 'Order'

        @admin.action(description='Approve selected prescriptions')
        def approve_selected(self, request, queryset):
            _prescription_bulk_status(self, request, queryset, 'approved', 'approved')

        @admin.action(description='Reject selected prescriptions')
        def reject_selected(self, request, queryset):
            _prescription_bulk_status(self, request, queryset, 'rejected', 'rejected')
