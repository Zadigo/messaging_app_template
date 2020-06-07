from django.conf.urls import re_path
from zambda import consumers

websocket_urlpatterns = [
    re_path(r'ws/forum/(?P<reference>[a-z0-9]+)/$', consumers.ChatConsumer)
]
