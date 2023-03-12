"""
All Admin configuration related to drf_user

Author: Himanshu Shankar (https://himanshus.com)
"""
from django.contrib import admin
from django.contrib.auth.admin import Group
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.admin import UserAdmin
from django.utils.text import gettext_lazy as _
from .models import *


class DRFUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "profile_image", "email", "mobile", "address", "city", "zipcode", "country", "About_Me", "type")}),

        (_("Permissions"),{"fields": ("is_admin", "is_client", "is_active", "is_staff", "is_superuser","receive_notif", "groups", "user_permissions"  )},),

        (_("Important dates"), {"fields": ("last_login", "date_joined", "update_date")},),
        )
    add_fieldsets = (
        (None, { "classes": ("wide",), "fields": ("username", "email", "mobile", "password1", "password2", "type"), }, ),
        )
    list_display = ("username", "email", "first_name", "last_name", "mobile", "type", "is_staff", "receive_notif",)
    search_fields = ("username", "first_name", "last_name", "type", "email", "mobile")
    readonly_fields = ("date_joined", "last_login", "update_date")
    list_filter = ('is_staff', 'is_admin', 'is_active', 'groups')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)
    def has_add_permission(self, request, obj=None):
        return True
        
class OTPValidationAdmin(admin.ModelAdmin):
    list_display = ("destination", "porpose", "otp", "prop")

class AuthTransactionAdmin(admin.ModelAdmin):
    list_display = ("created_by", "ip_address", "create_date")
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return True
        


# UnRegister default Group & register proxy model Role
# This will also remove additional display of application in admin panel.
# Source: https://stackoverflow.com/a/32445368
admin.site.unregister(Group)
admin.site.register(Role, GroupAdmin)
admin.site.register(User, DRFUserAdmin)
admin.site.register(OTPValidation, OTPValidationAdmin)
admin.site.register(AuthTransaction, AuthTransactionAdmin)