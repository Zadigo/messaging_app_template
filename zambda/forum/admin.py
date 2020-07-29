from django.contrib import admin
from forum import models


@admin.register(models.Message)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ['created_on']
    date_hierarchy = 'created_on'

@admin.register(models.Thread)
class ThreadsAdmin(admin.ModelAdmin):
    list_display = ['name', 'reference', 'created_on', 'reported']
    search_fields = ['name', 'reference', 'sender', 'receiver']
    date_hierarchy = 'created_on'
    