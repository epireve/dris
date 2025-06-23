from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import DisasterReport, Shelter
from django.core import serializers


def broadcast_update(model_name, instance):
    channel_layer = get_channel_layer()
    data = serializers.serialize("json", [instance])
    async_to_sync(channel_layer.group_send)(
        "dris_updates",
        {
            "type": "send_update",
            "data": {
                "model": model_name,
                "payload": data,
            },
        },
    )


@receiver(post_save, sender=DisasterReport)
def disaster_report_updated(sender, instance, **kwargs):
    broadcast_update("disaster_report", instance)


@receiver(post_save, sender=Shelter)
def shelter_updated(sender, instance, **kwargs):
    broadcast_update("shelter", instance)
