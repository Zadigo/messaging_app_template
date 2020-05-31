from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api import serializers
from forum.models import Message, MessagesThread
from django.shortcuts import get_list_or_404, get_object_or_404

from django.db.models import F
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin


class IsAuthorized(IsAuthenticated):
    """Checks whether the user is active, authenticated
    and actually logged in"""
    def has_permission(self, request, view):
        return all([request.user, request.user.is_active, \
                        request.user.is_authenticated])

class BaseView(APIView):
    @classmethod
    def get_extra_actions(cls):
        return []

class ThreadAPI(BaseView):
    """Create a new message"""
    permission_classes = []
    authentication_classes = []

    def get(self, request, **kwargs):
        messages = Message.objects.filter(thread_reference__reference=kwargs['reference'])
        serialized_message = serializers.MessageSerializer(messages, many=True)
        return Response(data=serialized_message.data)

# class ThreadsAPI(ListAPIView):
#     """Returns all the messages from a given user"""
#     def list(self, request, **kwargs):
#         user_threads = get_list_or_404(MessagesThread, from_user__exact=1)
#         serialized_threads = serializers.SimpleThreadSerializer(user_threads, many=True)
#         return Response(data=serialized_threads.data)

class ThreadViewset(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    permission_classes = []
    authentication_classes = []
    queryset = MessagesThread.objects.all()
    serializer_class = serializers.ThreadSerializer

class NewMessageAPI(BaseView):
    """Create a new message"""
    permission_classes = []
    authentication_classes = []

    def post(self, request, **kwargs):
        current_thread = MessagesThread.objects.get(reference=kwargs['reference'])
        data = {
            'message': request.data['message'],
            'thread_reference': current_thread
        }
        message = Message.objects.create(**data)
        serialized_message = serializers.MessageSerializer(message)
        return Response(data=serialized_message.data, status=201)

class DeleteMessageAPI(BaseView):
    """Delete a message from a thread"""
    permission_classes = []
    authentication_classes = []

    def post(self, request, **kwargs):
        if kwargs and 'reference' in kwargs:
            messages = Message.objects.filter(thread_reference__reference=kwargs['reference'])
            message = messages.get(id=request.data['id'])
            message.delete()
            return Response(data={'message': message.id}, status=200)
        else:
            return Response(data={'error': 'An error occured'}, status=400)

class ReportThreadAPI(BaseView):
    permission_classes = []
    authentication_classes = []

    def post(self, request, **kwargs):
        selected_thread = MessagesThread.objects.get(reference=kwargs['reference'])
        selected_thread.reported = True
        selected_thread.save()
        serialized_thread = serializers.ThreadSerializer(selected_thread)
        return Response(data=serialized_thread.data)