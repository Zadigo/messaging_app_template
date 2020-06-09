import json

from asgiref.sync import async_to_sync
from channels.generic import websocket

from forum import models, serializers



class ChatConsumer(websocket.JsonWebsocketConsumer):
    def connect(self):
        # Join the thread
        thread_reference = self.scope['url_route']['kwargs']['reference']
        self.thread_name = f'thread_{thread_reference}'

        # self.user = self.scope['user']
        # if not self.user:
        #     self.close()

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
        serialized_message = self.create_in_database(text_data)

        # Send message to thread
        async_to_sync(self.channel_layer.group_send)(
            self.thread_name,
            {
                'type': 'chat_message',
                'message': serialized_message
            }
        )
        
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

    def create_in_database(self, message):
        reference = self.scope['url_route']['kwargs']['reference']
        try:
            thread = models.MessagesThread.objects.get(reference=reference)
        except:
            self.close()
        else:
            message = thread.message_set.create(message=message)
            return serializers.MessageSerializer(instance=message).data


class AsyncChatConsumer(websocket.AsyncJsonWebsocketConsumer):
    async def connect(self):
        # Join the thread
        thread_reference = self.scope['url_route']['kwargs']['reference']
        self.thread_name = f'thread_{thread_reference}'

        await self.channel_layer.group_add(
             self.thread_name,
             self.channel_name
        )

        self.accept()

    async def disconnect(self, code):
        # Leave thread
        await self.channel_layer.group_discard(
            self.thread_name,
            self.channel_name
        )

    async def receive(self, text_data):
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
        await self.channel_layer.group_send(
            self.thread_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
        
        # self.close(code=1000)

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({'message': message}))
