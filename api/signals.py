from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
import websocket
from datetime import datetime, timedelta

@receiver(user_logged_in)
def my_callback(sender, **kwargs):
    print("user login")
    # ws = websocket.WebSocket()
    # ws.connect("ws://localhost:8000/ws/socket-server/")
    # import inspect
    # for frame_record in inspect.stack():
    #     if frame_record[3]=='get_response':
    #         request = frame_record[0].f_locals['request']
    #         print(request)
    #         break
    # else:
    #     print(None)
    #     request = None
