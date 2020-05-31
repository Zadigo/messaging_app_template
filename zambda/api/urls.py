from django.urls.conf import path, re_path
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register('threads', views.ThreadViewset, basename='threads')

urlpatterns = router.urls

urlpatterns.append(re_path(r'^thread/(?P<reference>[a-z0-9]+)/report$', views.ReportThreadAPI().as_view(), name='report_thread_api'))
urlpatterns.append(re_path(r'^thread/(?P<reference>[a-z0-9]+)/delete-message$', views.DeleteMessageAPI().as_view(), name='delete_message_api'))
urlpatterns.append(re_path(r'^thread/(?P<reference>[a-z0-9]+)/new-message$', views.NewMessageAPI().as_view(), name='new_message_api'))
urlpatterns.append(re_path(r'^thread/(?P<reference>[a-z0-9]+)$', views.ThreadAPI.as_view(), name='my_thread_api'))
# urlpatterns.append(re_path(r'^threads$', views.Thre().as_view(), name='my_threads_api'))
