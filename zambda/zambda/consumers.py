import json

from asgiref.sync import async_to_sync
from channels.generic import websocket
import json


class ChatConsumer(websocket.JsonWebsocketConsumer):
    def connect(self):
        # Join the thread
        # thread_reference = self.scope['url_root']['kwargs']['reference']
        # self.thread_name = f'thread_{thread_reference}'

        # async_to_sync(self.channel_layer.group_add)(
        #     self.thread_name,
        #     self.channel_name
        # )

        self.accept()

    def disconnect(self, code):
        # Leave thread
        # async_to_sync(self.channel_layer.group_discard)(
        #     self.thread_name,
        #     self.channel_name
        # )
        pass

    def receive(self, text_data):
        # message = 'My message'
        # Send message to thread
        # async_to_sync(self.channel_layer.group_send)(
        #     self.thread_name,
        #     {
        #         'type': 'chat_message',
        #         'message': message
        #     }
        # )

        # self.send(text_data="We are a connected")
        self.close(code=1000)

    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))