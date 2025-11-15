from django.http import HttpResponse
from django.template import loader


from .models import Artista
from .models import GeneroArtista
from .models import Sessao
from .models import Performance
from .models import Evento
from .models import Local

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the ficha3 index.")


def artistas(request):
    artistas = Artista.objects.all()
    generos = GeneroArtista.objects.all()
    template = loader.get_template('artistas/artistas.html')
    context = {
        'artistas': artistas,
        'generos': generos
    }
    return HttpResponse(template.render(context, request))


def artistas_add(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        bio = request.POST.get('bio')
        genero_id = request.POST.get('genero')
        if nome and genero_id:
            genero = GeneroArtista.objects.get(id=genero_id)
            Artista.objects.create(nome=nome, bio=bio, genero=genero)
    return artistas(request)


def generos_artistas(request):
    generos = GeneroArtista.objects.all()
    template = loader.get_template('artistas/generos.html')
    context = {
        'generos': generos
    }  
    return HttpResponse(template.render(context, request))

def generos_artistas_add(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        if nome:
            GeneroArtista.objects.create(nome=nome)
    return generos_artistas(request)


def sessoes(request):
    sessoes = Sessao.objects.all()
    locais = Local.objects.all()
    eventos = Evento.objects.all()
    template = loader.get_template('sessoes/sessoes.html')
    context = {
        'sessoes': sessoes,
        'locais': locais,
        'eventos': eventos
    }
    return HttpResponse(template.render(context, request))

def sessoes_add(request):
    if request.method == 'POST':
        inicio = request.POST.get('inicio')
        fim = request.POST.get('fim')
        local = request.POST.get('local')
        evento = request.POST.get('evento')
        preco = request.POST.get('preco')
        if inicio and fim and local and evento and preco:
            Sessao.objects.create(inicio=inicio, fim=fim, local_id=local, evento_id=evento, preco=preco)
    return sessoes(request)


def performance(request):
    performances = Performance.objects.all()
    artistas = Artista.objects.all()
    sessoes = Sessao.objects.all()
    template = loader.get_template('sessoes/performance.html')
    context = {
        'performances': performances,
        'artistas': artistas,
        'sessoes': sessoes
    }
    return HttpResponse(template.render(context, request))

def performance_add(request):
    if request.method == 'POST':
        artista_id = request.POST.get('artista')
        sessao_id = request.POST.get('sessao')
        duracao_estim = request.POST.get('duracao')
        if artista_id and sessao_id and duracao_estim:
            Performance.objects.create(artista_id=artista_id, sessao_id=sessao_id, duracao_estim=duracao_estim)
    return performance(request)
