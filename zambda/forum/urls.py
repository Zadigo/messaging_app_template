from django.urls import path, re_path
from django.conf.urls import url
from forum import views

urlpatterns = [
    url(r'^thread/(?P<reference>[a-z0-9]+)/new-message$', views.new_message, name='new_message'),
    url(r'^thread/(?P<reference>[a-z0-9]+)/delete-message$', views.delete_message, name='delete_message'),
    url(r'^thread/(?P<reference>[a-z0-9]+)/report$', views.report_thread, name='report_thread'),
    url(r'^$', views.ForumView.as_view(), name='forum')
]