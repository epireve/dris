from django.urls import path
from .consumers import DRISRealtimeConsumer

websocket_urlpatterns = [
    path("ws/updates/", DRISRealtimeConsumer.as_asgi()),
]
