import json
import ast

from asgiref.sync import async_to_sync
from channels.generic import websocket

from forum import models, serializers, tasks



class ChatConsumer(websocket.JsonWebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.thread_reference = self.scope['url_route']['kwargs']['reference']
        self.thread_name = f'thread_{self.thread_reference}'
        # Join the thread in order to
        # start chatting with others
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
        transformed_dict = json.loads(text_data)

        method = transformed_dict['method']

        authorized_methods = ['delete', 'new']

        if method not in authorized_methods:
            self.send_json({'message': 'An error occured - MET-NO'})
        else:
            if method == 'new':
                message = transformed_dict['message']
                html = transformed_dict['html']
                contents = transformed_dict['contents']
                is_email = transformed_dict['email']

                serialized_message = self.create_in_database(
                    message, 
                    html, 
                    contents, 
                    email=is_email
                )
                # Send message to thread
                async_to_sync(self.channel_layer.group_send)(
                    self.thread_name,
                    {
                        'type': 'chat_message',
                        'message': serialized_message
                    }
                )

            if method == 'delete':
                message_id = transformed_dict['id']
                state = self.delete_from_database(message_id)
                self.send_json({
                    'method': 'deleted',
                    'state': state
                })
        
    def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'method': 'created',
            'message': message
        }))

    def create_in_database(self, message, html, contents, email=False):
        try:
            thread = models.Thread.objects.get(reference=self.thread_reference)
        except:
            self.close()
        else:
            message = thread.message_set.create(
                user=self.user,
                message=message,
                message_html=html,
                message_contents=contents
            )

            if email:
                message.email = True
                message.save()

                tasks.delayed_send_email.delay(
                    10,
                    thread.receiver.email,
                    message.text
                )

            serialized_message = serializers.MessageSerializer(instance=message)
            return serialized_message.data
    
    def delete_from_database(self, pk):
        try:
            thread = models.Thread.objects.get(reference=self.thread_reference)
        except:
            return False
        else:
            # Make sure that the only people
            # able to delete messages are the 
            # ones that created or sent them -;
            # in other words, I can only delete
            # a message I sent.
            if thread.sender.id != self.user.id:
                return False
            message = thread.message_set.get(id__exact=pk)
            message.delete()
            return True


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
