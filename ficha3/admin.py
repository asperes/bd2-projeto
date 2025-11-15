from django.contrib import admin

# Register your models here.
from .models import Artista
from .models import GeneroArtista
from .models import Sessao
from .models import Performance
from .models import Evento
from .models import CategoriaEvento
from .models import Local
from .models import Organizador

admin.site.register(GeneroArtista)
admin.site.register(Artista)
admin.site.register(Sessao)
admin.site.register(Performance)
admin.site.register(Evento)
admin.site.register(CategoriaEvento)
admin.site.register(Local)
admin.site.register(Organizador)
