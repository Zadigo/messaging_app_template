from django.db import models
from django.db.models import Manager
from django.shortcuts import reverse

from forum.managers import MessagesManager
from forum.utilities import create_thread_reference


class MessagesThread(models.Model):
    """Represents a thread containing various messages"""
    reference = models.CharField(max_length=100, blank=True, null=True)
    from_user = models.PositiveIntegerField()
    to_user = models.PositiveIntegerField()
    
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
    """Messages sent from a user to another in a discussion thread"""
    thread_reference    = models.ForeignKey(MessagesThread, blank=True, on_delete=models.CASCADE)
    message             = models.TextField(blank=True, null=True)
    created_on      = models.DateField(auto_now_add=True)

    objects = Manager()
    messages_manager = MessagesManager().as_manager()

    # def get_absolute_url(self):
    #     return reverse('thread_message', args=[1, self.pk])

    def __str__(self):
        return self.thread_reference.reference
