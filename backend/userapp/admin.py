# # from django.contrib import admin
# # from .models import UserProfile

# # @admin.register(UserProfile)
# # class UserProfileAdmin(admin.ModelAdmin):
# #     list_display = ('user', 'phone', 'city', 'pincode', 'last_updated')
# #     search_fields = ('user__username', 'user__email', 'phone', 'city')






# # userapp/admin.py
# from django.contrib import admin
# from .models import UserProfile

# @admin.register(UserProfile)
# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'phone', 'city', 'pincode', 'last_updated')
#     search_fields = ('user__username', 'user__email', 'phone', 'city')

# @admin.register(EmailChangeRequest)
# class EmailChangeRequestAdmin(admin.ModelAdmin):
#     list_display = ('user', 'new_email', 'token', 'created_at', 'expires_at', 'used')
#     search_fields = ('user__username', 'user__email', 'new_email')



from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "phone", "city", "gender"]
