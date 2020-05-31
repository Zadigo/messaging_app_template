from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Manager
from django.shortcuts import reverse

from forum.managers import MessagesManager
from forum.utilities import create_thread_reference

User = get_user_model()

class MessagesThread(models.Model):
    reference = models.CharField(max_length=100, blank=True, null=True)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='msg_sender')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='msg_receiver')
    
    reported    = models.BooleanField(default=False)
    created_on = models.DateField(auto_now_add=True)

    objects = Manager()

    def get_absolute_url(self):
        return reverse('thread', kwargs={'reference': self.reference})

    def __str__(self):
        return self.reference

    def clean(self):
        if not self.reference:
            self.reference = create_thread_reference()

class Message(models.Model):
    thread_reference    = models.ForeignKey(MessagesThread, blank=True, on_delete=models.CASCADE)
    message             = models.TextField(blank=True, null=True)
    created_on      = models.DateField(auto_now_add=True)

    objects = Manager()
    messages_manager = MessagesManager().as_manager()

    def __str__(self):
        return self.thread_reference.reference
