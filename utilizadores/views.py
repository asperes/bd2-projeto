from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

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