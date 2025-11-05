from django.contrib import admin
from .models import (
    Organizador, Local, CategoriaEvento, Evento, GeneroArtista, 
    Artista, Sessao, Cliente, Fatura, Bilhete, Performance, Avaliacao
)


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'email', 'telefone', 'data_registo']
    list_filter = ['data_registo']
    search_fields = ['nome', 'email', 'telefone']
    ordering = ['-data_registo']
    readonly_fields = ['data_registo']


@admin.register(Local)
class LocalAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'capacidade', 'contacto']
    list_filter = ['capacidade']
    search_fields = ['nome', 'morada', 'contacto']
    ordering = ['nome']


@admin.register(Organizador)
class OrganizadorAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'telefone']
    search_fields = ['nome', 'email']


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'organizador', 'categoria', 'data_inicio', 'ativo']
    list_filter = ['ativo', 'categoria', 'data_inicio']
    search_fields = ['titulo', 'descricao']
    date_hierarchy = 'data_inicio'


@admin.register(Sessao)
class SessaoAdmin(admin.ModelAdmin):
    list_display = ['evento', 'local', 'inicio', 'fim', 'preco']
    list_filter = ['local', 'inicio']
    search_fields = ['evento__titulo', 'local__nome']


@admin.register(Bilhete)
class BilheteAdmin(admin.ModelAdmin):
    list_display = ['codigo_unico', 'cliente', 'sessao', 'tipo', 'preco_final', 'usado']
    list_filter = ['tipo', 'usado', 'comprado_em']
    search_fields = ['codigo_unico', 'cliente__nome', 'sessao__evento__titulo']
    readonly_fields = ['comprado_em']


# Registrar os outros modelos de forma simples
admin.site.register(CategoriaEvento)
admin.site.register(GeneroArtista)
admin.site.register(Artista)
admin.site.register(Fatura)
admin.site.register(Performance)
admin.site.register(Avaliacao)
