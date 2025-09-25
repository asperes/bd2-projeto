from django.contrib import admin

# Register your models here.
from .models import Artista
from .models import GeneroArtista

admin.site.register(GeneroArtista)
admin.site.register(Artista)
