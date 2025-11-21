from django.shortcuts import render, redirect
from .models import *
from .forms import CriarEvento
import uuid
from django.contrib import messages
from django.db.models import Q
from utilizadores.models import User
# Create your views here.


def criar_evento(request):
    if request.method == 'POST':
        form = CriarEvento(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.event_id = uuid.uuid4()
            evento.host_id = request.user.user_id
            evento.status = 'published'
            evento.save()
            messages.success(request, "Evento criado com sucesso")
            return redirect('eventos:eventos')
    else:
        form = CriarEvento()
    return render(request, 'eventos/criar_evento.html',{'form': form})

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
    is_host = evento.host.user_id == request.user.user_id
    attendees = EventInvitations.objects.filter(event=evento, status='accepted')
    
    # Verificar se o utilizador já está a participar ou foi convidado
    user_invitation = EventInvitations.objects.filter(event=evento, invitee=request.user).first()
    is_participating = user_invitation and user_invitation.status == 'accepted'
    has_pending_invitation = user_invitation and user_invitation.status == 'pending'
    
    context = {
        'event': evento,
        'is_host': is_host,
        'attendees': attendees,
        'is_participating': is_participating,
        'has_pending_invitation': has_pending_invitation,
    }
    return render(request, 'eventos/ver_evento.html', context)

def participar_evento(request, event_id):
    evento = Events.objects.get(event_id=event_id)
    
    # Verificar se já está a participar ou tem convite
    existing_invitation = EventInvitations.objects.filter(event=evento, invitee=request.user).first()
    
    if existing_invitation:
        if existing_invitation.status == 'accepted':
            messages.info(request, "Você já está a participar deste evento.")
        elif existing_invitation.status == 'pending':
            # Aceitar convite pendente (funciona para eventos públicos e privados)
            existing_invitation.status = 'accepted'
            existing_invitation.save()
            messages.success(request, "Você agora está a participar do evento!")
    else:
        # Apenas para eventos públicos: criar nova participação
        if not evento.is_public:
            messages.error(request, "Este evento não é público.")
            return redirect('eventos:ver_evento', event_id=event_id)
        
        EventInvitations.objects.create(
            invitation_id=uuid.uuid4(),
            event=evento,
            inviter=evento.host,
            invitee=request.user,
            status='accepted',
            role='attendee',
            notification_sent=False
        )
        messages.success(request, "Você agora está a participar do evento!")
    
    return redirect('eventos:ver_evento', event_id=event_id)

def convidar_pessoas(request, event_id):
    evento = Events.objects.get(event_id=event_id)
    
    # Verificar se o utilizador é o host
    if evento.host.user_id != request.user.user_id:
        messages.error(request, "Apenas o host pode convidar pessoas.")
        return redirect('eventos:ver_evento', event_id=event_id)
    
    # Obter participantes já convidados
    convidados_ids = EventInvitations.objects.filter(event=evento).values_list('invitee_id', flat=True)
    
    # Obter utilizadors disponíveis para convidar (excluindo host e já convidados)
    utilizadores_disponiveis = User.objects.exclude(
        Q(user_id=evento.host.user_id) | Q(user_id__in=convidados_ids)
    )
    
    if request.method == 'POST':
        invitee_ids = request.POST.getlist('invitees')
        role = request.POST.get('role', 'attendee')
        
        if invitee_ids:
            for invitee_id in invitee_ids:
                EventInvitations.objects.create(
                    invitation_id=uuid.uuid4(),
                    event=evento,
                    inviter=request.user,
                    invitee_id=invitee_id,
                    status='pending',
                    role=role,
                    notification_sent=True
                )
            messages.success(request, f"{len(invitee_ids)} pessoa(s) convidada(s) com sucesso!")
            return redirect('eventos:ver_evento', event_id=event_id)
        else:
            messages.warning(request, "Selecione pelo menos uma pessoa para convidar.")
    
    context = {
        'event': evento,
        'utilizadores_disponiveis': utilizadores_disponiveis
    }
    return render(request, 'eventos/convidar_pessoas.html', context)