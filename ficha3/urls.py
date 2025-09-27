from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("eventos/", views.eventos_list, name="Eventos"),
    path("avaliacao/", views.avaliacao_list, name="Avaliacao"),
    path("organizador/", views.organizador_list, name="Organizador"),
]