from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class User(AbstractUser):
    ROLE_CHOICES = [
        ("CITIZEN", "Citizen"),
        ("VOLUNTEER", "Volunteer"),
        ("AUTHORITY", "Authority"),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)


class DisasterReport(models.Model):
    DISASTER_TYPES = [
        ("FLOOD", "Flood"),
        ("LANDSLIDE", "Landslide"),
        ("HAZE", "Haze"),
        ("FIRE", "Fire"),
        ("EARTHQUAKE", "Earthquake"),
        ("OTHER", "Other"),
    ]
    SEVERITY_CHOICES = [
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
        ("CRITICAL", "Critical"),
    ]
    STATUS_CHOICES = [
        ("NEW", "New"),
        ("VERIFIED", "Verified"),
        ("IN_PROGRESS", "In Progress"),
        ("RESOLVED", "Resolved"),
    ]

    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    disaster_type = models.CharField(max_length=10, choices=DISASTER_TYPES)
    description = models.TextField(help_text="Detailed description of the disaster")
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
    )
    severity = models.CharField(max_length=8, choices=SEVERITY_CHOICES)
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default="NEW")
    timestamp = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.disaster_type} - {self.severity} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


class AidRequest(models.Model):
    AID_TYPES = [
        ("FOOD", "Food"),
        ("WATER", "Water"),
        ("SHELTER", "Shelter"),
        ("MEDICAL", "Medical"),
        ("RESCUE", "Rescue"),
        ("OTHER", "Other"),
    ]
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("IN_PROGRESS", "In Progress"),
        ("FULFILLED", "Fulfilled"),
        ("REJECTED", "Rejected"),
    ]
    PRIORITY_CHOICES = [
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
        ("URGENT", "Urgent"),
    ]

    requester = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="aid_requests"
    )
    disaster_report = models.ForeignKey(
        DisasterReport,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="aid_requests",
    )
    aid_type = models.CharField(max_length=7, choices=AID_TYPES)
    description = models.TextField(
        help_text="Detailed description of the aid needed", blank=True, default=""
    )
    quantity = models.PositiveIntegerField(
        null=True, blank=True, help_text="Number of items/people needing assistance"
    )
    priority = models.CharField(
        max_length=6, choices=PRIORITY_CHOICES, default="MEDIUM"
    )
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default="PENDING")
    location_details = models.TextField(
        help_text="Specific location details for aid delivery", blank=True, default=""
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_aid_requests",
    )
    notes = models.TextField(blank=True, help_text="Additional notes or updates")

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.aid_type} - {self.priority} Priority - {self.status}"


class Shelter(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    capacity = models.IntegerField(validators=[MinValueValidator(0)])
    availability = models.IntegerField(validators=[MinValueValidator(0)])
    contact_info = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.availability}/{self.capacity})"


class VolunteerProfile(models.Model):
    AVAILABILITY_CHOICES = [
        ("WEEKDAYS", "Weekdays"),
        ("WEEKENDS", "Weekends"),
        ("BOTH", "Both Weekdays and Weekends"),
        ("ON_CALL", "On Call"),
    ]

    SKILL_CHOICES = [
        ("MEDICAL", "Medical"),
        ("RESCUE", "Search and Rescue"),
        ("LOGISTICS", "Logistics"),
        ("TRANSPORTATION", "Transportation"),
        ("COUNSELING", "Counseling"),
        ("COOKING", "Cooking"),
        ("LANGUAGE", "Language/Translation"),
        ("TECH", "Technical/IT"),
        ("OTHER", "Other"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="volunteer_profile",
        limit_choices_to={"role": "VOLUNTEER"},
    )
    skills = models.JSONField(help_text="List of volunteer's skills", default=list)
    availability = models.CharField(
        max_length=10, choices=AVAILABILITY_CHOICES, default="ON_CALL"
    )
    preferred_locations = models.JSONField(
        help_text="List of preferred areas for volunteering", default=list
    )
    contact_number = models.CharField(max_length=20)
    emergency_contact = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    verification_status = models.BooleanField(default=False)
    verification_date = models.DateTimeField(null=True, blank=True)
    verified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verified_volunteers",
        limit_choices_to={"role": "AUTHORITY"},
    )

    class Meta:
        ordering = ["user__username"]

    def __str__(self):
        return f"{self.user.username} - {'Verified' if self.verification_status else 'Unverified'}"

    def add_skill(self, skill):
        if skill in dict(self.SKILL_CHOICES):
            if not self.skills:
                self.skills = []
            if skill not in self.skills:
                self.skills.append(skill)
                self.save()

    def remove_skill(self, skill):
        if skill in self.skills:
            self.skills.remove(skill)
            self.save()

    def add_preferred_location(self, location):
        if not self.preferred_locations:
            self.preferred_locations = []
        if location not in self.preferred_locations:
            self.preferred_locations.append(location)
            self.save()

    def remove_preferred_location(self, location):
        if location in self.preferred_locations:
            self.preferred_locations.remove(location)
            self.save()


class TaskAssignment(models.Model):
    STATUS_CHOICES = [
        ("ASSIGNED", "Assigned"),
        ("IN_PROGRESS", "In Progress"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    ]
    authority = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assigned_tasks",
        limit_choices_to={"role": "AUTHORITY"},
    )
    volunteer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="volunteer_tasks",
        limit_choices_to={"role": "VOLUNTEER"},
    )
    aid_request = models.ForeignKey(
        "AidRequest", on_delete=models.CASCADE, related_name="task_assignments"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ASSIGNED")
    notes = models.TextField(blank=True)
    assigned_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("volunteer", "aid_request")

    def __str__(self):
        return f"Task: {self.aid_request} -> {self.volunteer} (by {self.authority})"
