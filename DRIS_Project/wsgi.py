"""
WSGI config for DRIS_Project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DRIS_Project.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        # "websocket": URLRouter([...])  # To be added in next steps
    }
)
