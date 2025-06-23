from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, VolunteerProfile


@receiver(post_save, sender=User)
def create_volunteer_profile(sender, instance, created, **kwargs):
    """Create a VolunteerProfile for new Volunteer users"""
    if created and instance.role == "VOLUNTEER":
        VolunteerProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_volunteer_profile(sender, instance, **kwargs):
    """Save the VolunteerProfile when the User is saved"""
    if instance.role == "VOLUNTEER":
        if hasattr(instance, "volunteer_profile"):
            instance.volunteer_profile.save()
        else:
            VolunteerProfile.objects.create(user=instance)
