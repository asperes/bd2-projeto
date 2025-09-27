from django.shortcuts import render, redirect
from .models import Fatura, Bilhete, Cliente, FaturasItem
from .forms import FaturaWithBilhetesForm, BilheteForm
from django.core.paginator import Paginator
from django.db import transaction

def fatura_list(request):
    faturas = Fatura.objects.all().order_by('-data_emissao')
    paginator = Paginator(faturas, 8)  # 8 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'ficha3/fatura_list.html', {'page_obj': page_obj})

def fatura_select_cliente(request):
    clientes = Cliente.objects.all()
    clientes_com_bilhetes = []
    for c in clientes:
        bilhetes_livres = c.bilhetes.filter(fatura_item__isnull=True)
        if bilhetes_livres.exists():
            clientes_com_bilhetes.append(c)
    print("Clientes com bilhetes elegíveis:", [c.nome for c in clientes_com_bilhetes])  # Debug line
    has_bilhetes = bool(clientes_com_bilhetes)
    return render(request, 'ficha3/fatura_select_cliente.html', {
        'clientes': clientes_com_bilhetes,
        'has_bilhetes': has_bilhetes,
    })

def fatura_add(request):
    if request.method == 'POST':
        form = FaturaWithBilhetesForm(request.POST)
        if form.is_valid():
            bilhetes = form.cleaned_data['bilhetes']
            total = sum(b.preco_final for b in bilhetes)
            with transaction.atomic():
                fatura = form.save(commit=False)
                fatura.total = total
                fatura.save()
                for bilhete in bilhetes:
                    FaturasItem.objects.create(fatura=fatura, bilhete=bilhete)
            return redirect('fatura_list')
        cliente_obj = None
        if 'cliente' in request.POST:
            try:
                cliente_obj = Cliente.objects.get(pk=request.POST['cliente'])
            except Cliente.DoesNotExist:
                cliente_obj = None
    else:
        if 'cliente' not in request.GET or not request.GET.get('cliente'):
            return redirect('fatura_select_cliente')
        initial = {'cliente': request.GET.get('cliente')}
        form = FaturaWithBilhetesForm(initial=initial)
        try:
            cliente_obj = Cliente.objects.get(pk=request.GET.get('cliente'))
        except Cliente.DoesNotExist:
            cliente_obj = None
    return render(request, 'ficha3/fatura_add.html', {'form': form, 'cliente_obj': cliente_obj})

def bilhete_list(request):
    bilhetes = Bilhete.objects.all().order_by('-comprado_em')
    paginator = Paginator(bilhetes, 8)  # 8 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'ficha3/bilhete_list.html', {'page_obj': page_obj})

def bilhete_add(request):
    if request.method == 'POST':
        form = BilheteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bilhete_list')
    else:
        form = BilheteForm()
    return render(request, 'ficha3/bilhete_add.html', {'form': form})
