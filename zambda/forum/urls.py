from django.urls import path, re_path, include
from django.conf.urls import url
from forum import views

app_name = 'forum'

threadpatterns = [
    url(r'^create$', views.create_thread, name='new'),
    url(r'^view$', views.change_thread, name='view'),
    url(r'^add-user$', views.add_user_to_thread, name='add_user'),
    url(r'^(?P<reference>[a-z0-9]+)/delete-message$', views.delete_message, name='delete'),
    url(r'^(?P<reference>[a-z0-9]+)/report$', views.report_thread, name='report'),
]

urlpatterns = [
    # url(r'^test', views.test_tasks_view, name='testing'),
    path('thread/', include((threadpatterns, app_name), namespace='thread')),

    url(r'^users/(?P<username>\w+)/private$', views.PrivateMessageView.as_view(), name='private'),
    url(r'^users$', views.UsersView.as_view(), name='users'),
    url(r'^$', views.ForumView.as_view(), name='forum')
]
