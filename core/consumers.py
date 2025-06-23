import json
from channels.generic.websocket import AsyncWebsocketConsumer


class DRISRealtimeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join a group for all users (could be refined per role or page)
        await self.channel_layer.group_add("dris_updates", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("dris_updates", self.channel_name)

    async def receive(self, text_data):
        # Echo or handle incoming messages if needed (not required for broadcast-only)
        pass

    async def send_update(self, event):
        # Send data to WebSocket
        await self.send(text_data=json.dumps(event["data"]))
