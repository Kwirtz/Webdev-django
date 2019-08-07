# chat/urls.py
from django.urls import re_path
from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),
]