import json
import ast

from asgiref.sync import async_to_sync
from channels.generic import websocket

from forum import models, serializers



class ChatConsumer(websocket.JsonWebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        # Join the thread
        thread_reference = self.scope['url_route']['kwargs']['reference']
        self.thread_reference = thread_reference
        self.thread_name = f'thread_{thread_reference}'

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
        # transformed_dict = json.loads(json.dumps(text_data))
        transformed_dict = ast.literal_eval(text_data)

        authorized_methods = ['delete', 'new']

        method = transformed_dict['method']
        if method not in authorized_methods:
            self.send_json({'message': 'An error occured - MET-NO'})
        else:
            if method == 'new':
                serialized_message = self.create_in_database(transformed_dict['message'])

                # Send message to thread
                async_to_sync(self.channel_layer.group_send)(
                    self.thread_name,
                    {
                        'type': 'chat_message',
                        'message': serialized_message
                    }
                )

            if method == 'delete':
                # self.send_json({'method': 'deleted', 'message': {'id': '1'}})
                serialized_message = self.delete_from_database(transformed_dict['id'])
                self.send_json({
                    'method': 'deleted',
                    'message': serialized_message
                })
        
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'method': 'created',
            'message': message
        }))

    def create_in_database(self, message, thread=None):
        try:
            thread = models.Thread.objects.get(reference=self.thread_reference)
        except:
            self.close()
        else:
            message = thread.message_set.create(user=self.user, message=message)
            serialized_message = serializers.MessageSerializer(instance=message)
            return serialized_message.data
    
    def delete_from_database(self, pk):
        try:
            thread = models.Thread.objects.get(reference=self.thread_reference)
        except:
            self.close()
        else:
            message = thread.message_set.get(id__exact=pk)
            return serializers.MessageSerializer(instance=message.delete()).data


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
            'created_on': '2020-05-31',
            'id': 89,
            'message': text_data,
            'thread_reference': {
                'sender': 1,
                'reference': '388f12d950',
                'reported': 'False',
                'receiver': 2
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
