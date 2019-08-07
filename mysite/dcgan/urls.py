from django.urls import re_path, path
from . import views

urlpatterns = [
    path('', views.index),
    path("generate", views.generate, name="generate"),
]