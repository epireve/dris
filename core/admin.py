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


@admin.register(DisasterReport)
class DisasterReportAdmin(admin.ModelAdmin):
    list_display = (
        "disaster_type",
        "severity",
        "status",
        "reporter",
        "location_display",
        "timestamp",
    )
    list_filter = ("disaster_type", "severity", "status", "timestamp")
    search_fields = ("description", "reporter__username")
    readonly_fields = ("timestamp", "last_updated")
    date_hierarchy = "timestamp"

    def location_display(self, obj):
        return f"({obj.latitude}, {obj.longitude})"

    location_display.short_description = "Location"


@admin.register(AidRequest)
class AidRequestAdmin(admin.ModelAdmin):
    list_display = ("aid_type", "requester", "status", "disaster_report", "timestamp")
    list_filter = ("aid_type", "status", "timestamp")
    search_fields = ("requester__username",)
    raw_id_fields = ("disaster_report",)


@admin.register(Shelter)
class ShelterAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "capacity", "availability", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "location")
    list_editable = ("availability", "is_active")


# Register the custom User admin
admin.site.register(User, CustomUserAdmin)
