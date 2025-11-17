import uuid
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db import models

from .models import User,Friendships


from .forms import CriarUtilizador



# Create your views here.
# 
def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login feito com sucesso")
            return redirect('utilizadores:home')
        else:
            messages.error(request, "Erro ao fazer login")
            return render(request, 'auth/login.html', {'form': form})
    else:
        if request.user.is_authenticated:
            return redirect('utilizadores:home')
        form = AuthenticationForm()
        return render(request, 'auth/login.html', {'form': form})


def logout_user(request):
    logout(request)
    messages.success(request,("logout feito com sucesso"))
    return redirect('utilizadores:login_user')

def register_user(request):
    if request.method == "POST":
        form = CriarUtilizador(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Conta criada com sucesso")
            return redirect('utilizadores:login_user')
        else:
            messages.error(request, "erros no formulario")
    else:
        form = CriarUtilizador()
    return render(request, 'auth/register.html', {'form':form})

def home(request):
    if not request.user.is_authenticated:
        return redirect('utilizadores:login_user')
    return render(request,'home.html',{})

def perfil(request):
    return render(request,'perfil/perfil.html',{'user': request.user})

def editar_perfil(request):
    pass
    return render(request,'perfil/editar_perfil.html',{})

def ver_perfil(request, user_id):
    utilizador = User.objects.get(user_id=user_id)
    return render(request,'perfil/ver_perfil.html',{'profile_user': utilizador})

def pesquisar_users(request):
    query = request.GET.get('q', '')
    users = []
    if query:
        users = User.objects.filter(
            models.Q(username__icontains=query) |
            models.Q(first_name__icontains=query) |
            models.Q(last_name__icontains=query)
        )
    context = {
        'query': query,
        'users': users,
    }
    return render(request, 'amizades/pesquisar_users.html', context)

def enviar_pedido(request, user_id):
    if request.user.user_id == user_id:
        messages.error(request, "Não pode enviar um pedido de amizade a si próprio.")
        return redirect('utilizadores:pesquisar_users')
    if user_id is not None:
        user_adicionado = User.objects.get(user_id=user_id)
        jaexiste = Friendships.objects.filter(
            models.Q(user_id_1=request.user, user_id_2=user_adicionado) |
            models.Q(user_id_1=user_adicionado, user_id_2=request.user)
        ).exists()
        if jaexiste:
            messages.info(request, f"Já existe uma amizade ou pedido de amizade com {user_adicionado.first_name} {user_adicionado.last_name}.")
            return redirect('utilizadores:pesquisar_users')
        else:
            Friendships.objects.create(
                friendship_id=uuid.uuid4(),
                user_id_1=request.user,
                user_id_2=user_adicionado,
                status='pending',
                initiated_by=request.user,
            )
            messages.success(request, f"Pedido de amizade enviado para {user_adicionado.first_name} {user_adicionado.last_name}.")
    return redirect('utilizadores:pesquisar_users')

def remove_friend(request, friendship_id):
    pass
    return redirect('utilizadores:perfil')



