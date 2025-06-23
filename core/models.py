from django.db import models
from django.contrib.auth.models import AbstractUser


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
        ("OTHER", "Other"),
    ]
    SEVERITY_CHOICES = [
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
    ]
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    disaster_type = models.CharField(max_length=10, choices=DISASTER_TYPES)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    severity = models.CharField(max_length=6, choices=SEVERITY_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)


class AidRequest(models.Model):
    AID_TYPES = [
        ("FOOD", "Food"),
        ("SHELTER", "Shelter"),
        ("RESCUE", "Rescue"),
    ]
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("FULFILLED", "Fulfilled"),
    ]
    requester = models.ForeignKey(User, on_delete=models.CASCADE)
    disaster_report = models.ForeignKey(
        DisasterReport, on_delete=models.SET_NULL, null=True
    )
    aid_type = models.CharField(max_length=7, choices=AID_TYPES)
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default="PENDING")


class Shelter(models.Model):
    location = models.CharField(max_length=255)
    capacity = models.IntegerField()
    availability = models.IntegerField()
