from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import reverse

from forum import managers
from forum import utilities

MYUSER = get_user_model()

class Thread(models.Model):
    reference = models.CharField(max_length=100, default=utilities.create_thread_reference(), blank=True, null=True)
    sender   = models.ForeignKey(MYUSER, on_delete=models.CASCADE, blank=True, null=True, related_name='msg_sender')
    receiver    = models.ForeignKey(MYUSER, on_delete=models.CASCADE, blank=True, null=True, related_name='msg_receiver')
    
    reported    = models.BooleanField(default=False)
    public      = models.BooleanField(default=False)
    
    modified_on = models.DateField(auto_now=True)
    created_on  = models.DateField(auto_now_add=True)

    objects = models.Manager()
    custom_manager = managers.ThreadsManager().as_manager()

    def get_absolute_url(self):
        return reverse('thread', kwargs={'reference': self.reference})

    def __str__(self):
        return self.reference

    def clean(self):
        if not self.reference:
            self.reference = utilities.create_thread_reference()


class AbstractMessage(models.Model):
    thread      = models.ForeignKey(Thread, blank=True, on_delete=models.CASCADE)
    user        = models.ForeignKey(MYUSER, on_delete=models.CASCADE)
    message       = models.TextField(blank=True, null=True)
    created_on      = models.DateField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        abstract = True


class PrivateMessage(AbstractMessage):
    thread = None

    def __str__(self):
        return self.created_on


class Message(AbstractMessage):
    message        = models.TextField(blank=True, null=True)
    created_on      = models.DateField(auto_now_add=True)

    objects = models.Manager()
    custom_manager = mangers.MessagesManager().as_manager()

    def __str__(self):
        return self.thread.reference
