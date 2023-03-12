import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync


class Login_user(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'login'
        self.accept()