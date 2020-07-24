from django.urls import path, re_path
from django.conf.urls import url
from forum import views

app_name = 'forum'

urlpatterns = [
    url(r'^thread/create$', views.create_thread, name='new_thread'),
    url(r'^thread/view$', views.change_thread, name='view_thread'),
    url(r'^thread/(?P<reference>[a-z0-9]+)/new-email$', views.new_email_message, name='new_email'),
    url(r'^thread/(?P<reference>[a-z0-9]+)/new-message$', views.new_message, name='new'),
    url(r'^thread/(?P<reference>[a-z0-9]+)/delete-message$', views.delete_message, name='delete'),
    url(r'^thread/(?P<reference>[a-z0-9]+)/report$', views.report_thread, name='report'),
    url(r'^users/(?P<username>\w+)/private$', views.PrivateMessageView.as_view(), name='private'),
    url(r'^users$', views.UsersView.as_view(), name='users'),
    url(r'^$', views.ForumView.as_view(), name='forum')
]
