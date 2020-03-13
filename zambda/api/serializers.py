from rest_framework.serializers import ModelSerializer, Serializer
from forum.models import MessagesThread, Message
from rest_framework import fields



class SimpleThreadSerializer(Serializer):
    """A thread serializer that returns only the
    thread references for VUE"""
    reference = fields.CharField(read_only=True)
    created_on = fields.DateField(read_only=True)

class ThreadSerializer(ModelSerializer):
    """Serializer for the Thread model"""
    class Meta:
        model = MessagesThread
        fields = ['from_user', 'to_user', 'reference']

class MessageSerializer(ModelSerializer):
    """Serializer for the Message model"""
    thread_reference = ThreadSerializer()
    class Meta:
        model = Message
        fields = ['message', 'created_on', 'id', 'thread_reference']
