from django.urls import path
from . import views

urlpatterns = [
    path('faturas/select-cliente/', views.fatura_select_cliente, name='fatura_select_cliente'),
    path('faturas/add/', views.fatura_add, name='fatura_add'),
    path('faturas/', views.fatura_list, name='fatura_list'),
    path('bilhetes/', views.bilhete_list, name='bilhete_list'),
    path('bilhetes/add/', views.bilhete_add, name='bilhete_add'),
]