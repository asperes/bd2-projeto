from django.urls import path
from . import views

urlpatterns = [
    # Página inicial
    path('', views.index, name='index'),
    
    # URLs para Cliente
    path('clientes/', views.ClienteListView.as_view(), name='cliente_list'),
    path('clientes/novo/', views.cliente_create, name='cliente_create'),
    path('clientes/<int:pk>/', views.cliente_detail, name='cliente_detail'),
    
    # URLs para Local
    path('locais/', views.LocalListView.as_view(), name='local_list'),
    path('locais/novo/', views.local_create, name='local_create'),
    path('locais/<int:pk>/', views.local_detail, name='local_detail'),
    
    # APIs
    path('api/clientes/', views.api_clientes, name='api_clientes'),
    path('api/locais/', views.api_locais, name='api_locais'),
]