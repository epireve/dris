from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, DisasterReport, AidRequest, Shelter


class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "role", "is_staff")
    list_filter = ("role", "is_staff", "is_superuser")
    fieldsets = UserAdmin.fieldsets + (("Role Information", {"fields": ("role",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Role Information", {"fields": ("role",)}),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(DisasterReport)
admin.site.register(AidRequest)
admin.site.register(Shelter)
