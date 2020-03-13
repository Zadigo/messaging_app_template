from django.shortcuts import render
from django.views.generic import View

from forum.models import Message


class ForumView(View):
    """Access the forum section of the website"""
    def get(self, request, *args, **kwargs):
        return render(request, 'pages/messages.html')
