from django.contrib import admin
from forum.models import Message, MessagesThread


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['thread_reference', 'created_on']
    date_hierarchy = 'created_on'

@admin.register(MessagesThread)
class MessageThreadAdmin(admin.ModelAdmin):
    list_display = ['reference', 'to_user', 'from_user', 'created_on']
    search_fields = ['reference', 'to_user', 'from_user']
    date_hierarchy = 'created_on'
    