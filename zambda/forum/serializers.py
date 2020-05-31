from rest_framework.serializers import ModelSerializer, Serializer
from forum.models import MessagesThread, Message
from rest_framework import fields



class SimpleThreadSerializer(Serializer):
    reference = fields.CharField(read_only=True)
    reported = fields.BooleanField(read_only=True)
    created_on = fields.DateField(read_only=True)

class ThreadSerializer(ModelSerializer):
    class Meta:
        model = MessagesThread
        fields = ['from_user', 'to_user', 'reference', 'reported']

class MessageSerializer(ModelSerializer):
    thread_reference = ThreadSerializer()
    class Meta:
        model = Message
        fields = ['message', 'created_on', 'id', 'thread_reference']
