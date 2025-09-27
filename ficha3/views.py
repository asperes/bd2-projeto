from django.http import HttpResponse
from django.template import loader
from .models import Evento, Avaliacao, Organizador

def index(request):
	template = loader.get_template("base_generic.html")
	return HttpResponse(template.render())

def eventos_list(request):
	eventos = Evento.objects.all().order_by('data_inicio')
	template = loader.get_template("Eventos/eventos_list.html")
	context = {"eventos": eventos}
	return HttpResponse(template.render(context, request))


def avaliacao_list(request):
	avaliacoes = Avaliacao.objects.all().order_by('criado_em')
	template = loader.get_template("Avaliacao/avaliacao_list.html")
	context = {"avaliacoes": avaliacoes}
	return HttpResponse(template.render(context, request))

def organizador_list(request):
	organizadores = Organizador.objects.all().order_by('nome')
	template = loader.get_template("Organizador/organizador_list.html")
	context = {"organizadores": organizadores}
	return HttpResponse(template.render(context, request))