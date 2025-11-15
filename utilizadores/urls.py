from os import name
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('login_user', views.login_user, name="login_user"),
    path('register/', views.register_user, name='register'),
    path('logout_user',views.logout_user, name='logout_user'),
    path('',views.home,name='home')
]
