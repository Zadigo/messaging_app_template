from django.urls import path, re_path
from django.conf.urls import url
from forum import views

urlpatterns = [
    url(r'^$', views.ForumView.as_view(), name='forum')
]