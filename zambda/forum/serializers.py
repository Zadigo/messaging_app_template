from rest_framework.serializers import ModelSerializer, Serializer
from forum import models
from django.contrib.auth import get_user_model
from rest_framework import fields

MYUSER = get_user_model()

class MyUserSerializer(Serializer):
    username = fields.CharField()

class SimpleThreadSerializer(Serializer):
    reference = fields.CharField(read_only=True)
    name = fields.CharField()
    reported = fields.BooleanField(read_only=True)
    created_on = fields.DateField(read_only=True)


class ThreadSerializer(ModelSerializer):
    class Meta:
        model = models.Thread
        fields = ['sender', 'name', 'receiver', 'reference', 'reported', 'public']


class MessageSerializer(ModelSerializer):
    user = MyUserSerializer()
    class Meta:
        model = models.Message
        fields = ['id', 'user', 'message', 'message_html', 'created_on']
