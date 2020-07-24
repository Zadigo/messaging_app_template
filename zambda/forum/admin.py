from django.contrib import admin
from forum import models


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['created_on']
    date_hierarchy = 'created_on'

@admin.register(models.Thread)
class MessageThreadAdmin(admin.ModelAdmin):
    list_display = ['reference', 'created_on', 'reported']
    search_fields = ['reference', 'sender', 'receiver']
    date_hierarchy = 'created_on'
    