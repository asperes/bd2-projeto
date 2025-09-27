from django.http import HttpResponse
from django.template import loader


from .models import Artista
from .models import GeneroArtista

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
