from django.shortcuts import render, redirect
from .models import *

# Create your views here.


def criar_evento(request):
    if request.method == 'POST':
        pass
    else:
        pass
    return render(request, 'eventos/criar_evento.html',{})

def eventos(request):
    eventos_publicos = VActiveEvents.objects.filter(is_public=True).order_by('start_datetime')
    eventos_convidados = EventInvitations.objects.filter(invitee_id=request.user.user_id).select_related('event')
    eventos_pessoais = Events.objects.filter(host=request.user.user_id)

    context = {
        'active_public_events': eventos_publicos,
        'invited_events': eventos_convidados,
        'hosted_events': eventos_pessoais
    }
    return render(request, 'eventos/eventos.html',context)

def ver_evento(request, event_id):
    evento = Events.objects.get(event_id=event_id)
    return render(request, 'eventos/ver_evento.html',{'event': evento})