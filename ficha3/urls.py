"""
URL configuration for bilheteira project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from . import views

urlpatterns = [
    path('artistas/', views.artistas, name='artistas'),
    path('artistas/add/', views.artistas_add, name='artistas_add'),

    path('generos_artistas/', views.generos_artistas, name='generos_artistas'),
    path('generos_artistas/add/', views.generos_artistas_add, name='generos_artistas_add'),

    path('sessoes/', views.sessoes, name='sessoes'),
    path('sessoes/add/', views.sessoes_add, name='sessoes_add'),
    path('performance/', views.performance, name='performance'),
    path('performance/add/', views.performance_add, name='performance_add'),
    

]
