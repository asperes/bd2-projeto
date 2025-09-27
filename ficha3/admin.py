from django.contrib import admin
from .models import *

# Register your models here.

models = [Sessao, Organizador, Local, CategoriaEvento, Evento, Artista, Cliente, Fatura, Bilhete, Performance, Avaliacao]

admin.site.register(models)