from os import name
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('criar_evento', views.criar_evento, name="criar_evento"),
    path('eventos/', views.eventos, name='eventos'),
    path('ver_evento/<uuid:event_id>/',views.ver_evento, name='ver_evento'),
]
