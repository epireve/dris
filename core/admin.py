from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import (
    DisasterReport,
    AidRequest,
    Shelter,
    VolunteerProfile,
    TaskAssignment,
)
from django.utils import timezone
from .models import (
    User,
    DisasterReport,
    AidRequest,
    Shelter,
    VolunteerProfile,
    TaskAssignment,
)


class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "role", "is_staff")
    list_filter = ("role", "is_staff", "is_superuser", "groups")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (_("Role"), {"fields": ("role",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "role", "password1", "password2"),
            },
        ),
    )


@admin.register(DisasterReport)
class DisasterReportAdmin(admin.ModelAdmin):
    list_display = ("disaster_type", "severity", "status", "reporter", "timestamp")
    list_filter = ("disaster_type", "severity", "status", "timestamp")
    search_fields = ("description", "reporter__username")
    date_hierarchy = "timestamp"


@admin.register(AidRequest)
class AidRequestAdmin(admin.ModelAdmin):
    list_display = ("aid_type", "priority", "status", "requester", "timestamp")
    list_filter = ("aid_type", "priority", "status", "timestamp")
    search_fields = ("description", "requester__username", "location_details")
    date_hierarchy = "timestamp"
    raw_id_fields = ("disaster_report", "assigned_to")


@admin.register(Shelter)
class ShelterAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "capacity", "availability", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "location")


@admin.register(VolunteerProfile)
class VolunteerProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "availability",
        "verification_status",
        "contact_number",
        "is_active",
    )
    list_filter = (
        "availability",
        "verification_status",
        "is_active",
        "verification_date",
    )
    search_fields = ("user__username", "user__email", "contact_number", "notes")
    raw_id_fields = ("user", "verified_by")
    readonly_fields = ("verification_date",)

    fieldsets = (
        (None, {"fields": ("user", "is_active", "notes")}),
        (
            "Skills & Availability",
            {"fields": ("skills", "availability", "preferred_locations")},
        ),
        ("Contact Information", {"fields": ("contact_number", "emergency_contact")}),
        (
            "Verification",
            {"fields": ("verification_status", "verification_date", "verified_by")},
        ),
    )

    def save_model(self, request, obj, form, change):
        if "verification_status" in form.changed_data:
            if obj.verification_status:
                obj.verified_by = request.user
                obj.verification_date = timezone.now()
            else:
                obj.verified_by = None
                obj.verification_date = None
        super().save_model(request, obj, form, change)


@admin.register(TaskAssignment)
class TaskAssignmentAdmin(admin.ModelAdmin):
    list_display = (
        "aid_request",
        "volunteer",
        "authority",
        "status",
        "assigned_at",
        "updated_at",
    )
    list_filter = ("status", "assigned_at", "updated_at")
    search_fields = (
        "aid_request__description",
        "volunteer__username",
        "authority__username",
        "notes",
    )
    raw_id_fields = ("aid_request", "volunteer", "authority")
    readonly_fields = ("assigned_at", "updated_at")


admin.site.register(User, CustomUserAdmin)
