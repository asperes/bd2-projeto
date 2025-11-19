from os import name
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('login_user', views.login_user, name="login_user"),
    path('register/', views.register_user, name='register'),
    path('logout_user',views.logout_user, name='logout_user'),
    path('',views.home,name='home'),
    path('perfil/', views.perfil, name='perfil'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path('ver_perfil/<uuid:user_id>/', views.ver_perfil, name='ver_perfil'),
    path('pesquisar_users/', views.pesquisar_users, name='pesquisar_users'),
    path('enviar_pedido/<uuid:user_id>/', views.enviar_pedido, name='enviar_pedido'),
    path('remove_friend/<uuid:friendship_id>/', views.remove_friend, name='remove_friend'),
    path('ver_amizades/', views.ver_amizades, name='ver_amizades'),
    path('ver_pedidos/', views.ver_pedidos, name='ver_pedidos'),
    path('aceitar_pedido/<uuid:friendship_id>/', views.aceitar_pedido, name='aceitar_pedido'),
    path('recusar_pedido/<uuid:friendship_id>/', views.recusar_pedido, name='recusar_pedido'),
    
]
