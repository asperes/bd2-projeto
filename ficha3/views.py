from django.http import HttpResponse
from django.template import loader

from .models import Artista
from .models import GeneroArtista

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the ficha3 index.")


def artistas(request):
    artistas = Artista.objects.all()
    template = loader.get_template('artistas/artistas.html')
    context = {
        'artistas': artistas
    }
    return HttpResponse(template.render(context, request))

def generos_artistas(request):
    generos = GeneroArtista.objects.all()
    template = loader.get_template('artistas/generos.html')
    context = {
        'generos': generos
    }  
    return HttpResponse(template.render(context, request))
