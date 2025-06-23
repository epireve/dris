from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


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
    requester = models.ForeignKey(User, on_delete=models.CASCADE)
    disaster_report = models.ForeignKey(
        DisasterReport, on_delete=models.SET_NULL, null=True
    )
    aid_type = models.CharField(
        max_length=7,
        choices=[
            ("FOOD", "Food"),
            ("SHELTER", "Shelter"),
            ("RESCUE", "Rescue"),
            ("MEDICAL", "Medical"),
        ],
    )
    status = models.CharField(
        max_length=9,
        choices=[
            ("PENDING", "Pending"),
            ("APPROVED", "Approved"),
            ("FULFILLED", "Fulfilled"),
            ("REJECTED", "Rejected"),
        ],
        default="PENDING",
    )
    timestamp = models.DateTimeField(auto_now_add=True)


class Shelter(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    capacity = models.IntegerField(validators=[MinValueValidator(0)])
    availability = models.IntegerField(validators=[MinValueValidator(0)])
    contact_info = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.availability}/{self.capacity})"
