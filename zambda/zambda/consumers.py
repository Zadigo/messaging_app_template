import json

from asgiref.sync import async_to_sync
from channels.generic import websocket
import json


class ChatConsumer(websocket.JsonWebsocketConsumer):
    def connect(self):
        # Join the thread
        thread_reference = self.scope['url_route']['kwargs']['reference']
        self.thread_name = f'thread_{thread_reference}'

        async_to_sync(self.channel_layer.group_add)(
             self.thread_name,
             self.channel_name
        )

        self.accept()

    def disconnect(self, code):
        # Leave thread
        async_to_sync(self.channel_layer.group_discard)(
            self.thread_name,
            self.channel_name
        )

    def receive(self, text_data):
        print(text_data)
        message = {
            "created_on": "2020-05-31",
            "id": 89,
            "message": text_data,
            "thread_reference": {
                "from_user": 1,
                "reference": "388f12d950",
                "reported": "False",
                "to_user": 2
            }
        }
        
        # Send message to thread
        async_to_sync(self.channel_layer.group_send)(
            self.thread_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
        
        # self.close(code=1000)

    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
