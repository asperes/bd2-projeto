from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.db import connection
from django.views.generic import ListView
from .models import Cliente, Local
from .forms import ClienteForm, LocalForm


def index(request):
    """Página inicial com resumo dos dados"""
    context = {
        'total_clientes': Cliente.objects.count(),
        'total_locais': Local.objects.count(),
    }
    return render(request, 'ficha3/index.html', context)


# ============================================================================
# VIEWS PARA CLIENTE
# ============================================================================

class ClienteListView(ListView):
    """Lista todos os clientes usando a vista SQL"""
    model = Cliente
    template_name = 'ficha3/cliente_list.html'
    context_object_name = 'clientes'
    paginate_by = 10
    
    def get_queryset(self):
        # Usar a vista SQL criada
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM vista_clientes")
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]


def cliente_create(request):
    """Criar novo cliente usando o procedimento SQL"""
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT inserir_cliente(%s, %s, %s, %s)",
                        [
                            form.cleaned_data['nome'],
                            form.cleaned_data['email'],
                            form.cleaned_data['telefone'],
                            form.cleaned_data['morada']
                        ]
                    )
                    cliente_id = cursor.fetchone()[0]
                
                messages.success(request, f'Cliente criado com sucesso! ID: {cliente_id}')
                return redirect('cliente_list')
            except Exception as e:
                messages.error(request, f'Erro ao criar cliente: {str(e)}')
    else:
        form = ClienteForm()
    
    return render(request, 'ficha3/cliente_form.html', {'form': form, 'title': 'Novo Cliente'})


def cliente_detail(request, pk):
    """Detalhes de um cliente específico"""
    cliente = get_object_or_404(Cliente, pk=pk)
    
    # Buscar bilhetes do cliente
    bilhetes = cliente.bilhetes.select_related('sessao__evento', 'sessao__local').all()
    
    context = {
        'cliente': cliente,
        'bilhetes': bilhetes,
    }
    return render(request, 'ficha3/cliente_detail.html', context)


# ============================================================================
# VIEWS PARA LOCAL
# ============================================================================

class LocalListView(ListView):
    """Lista todos os locais usando a vista SQL"""
    model = Local
    template_name = 'ficha3/local_list.html'
    context_object_name = 'locais'
    paginate_by = 10
    
    def get_queryset(self):
        # Usar a vista SQL criada
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM vista_locais")
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]


def local_create(request):
    """Criar novo local usando o procedimento SQL"""
    if request.method == 'POST':
        form = LocalForm(request.POST)
        if form.is_valid():
            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT inserir_local(%s, %s, %s, %s)",
                        [
                            form.cleaned_data['nome'],
                            form.cleaned_data['morada'],
                            form.cleaned_data['capacidade'],
                            form.cleaned_data['contacto']
                        ]
                    )
                    local_id = cursor.fetchone()[0]
                
                messages.success(request, f'Local criado com sucesso! ID: {local_id}')
                return redirect('local_list')
            except Exception as e:
                messages.error(request, f'Erro ao criar local: {str(e)}')
    else:
        form = LocalForm()
    
    return render(request, 'ficha3/local_form.html', {'form': form, 'title': 'Novo Local'})


def local_detail(request, pk):
    """Detalhes de um local específico"""
    local = get_object_or_404(Local, pk=pk)
    
    # Buscar sessões do local
    sessoes = local.sessoes.select_related('evento').order_by('-inicio').all()[:10]
    
    context = {
        'local': local,
        'sessoes': sessoes,
    }
    return render(request, 'ficha3/local_detail.html', context)


# ============================================================================
# API VIEWS (AJAX)
# ============================================================================

def api_clientes(request):
    """API para retornar clientes em formato JSON"""
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM vista_clientes LIMIT 100")
        columns = [col[0] for col in cursor.description]
        clientes = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    return JsonResponse({'clientes': clientes})


def api_locais(request):
    """API para retornar locais em formato JSON"""
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM vista_locais")
        columns = [col[0] for col in cursor.description]
        locais = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    return JsonResponse({'locais': locais})
