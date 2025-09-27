from django.db import models
from django.core.exceptions import ValidationError
import uuid
from decimal import Decimal

# Create your models here.
class Organizador(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)

    def __str__(self):
        return self.nome

class Local(models.Model):
    nome = models.CharField(max_length=100)
    morada = models.CharField(max_length=200)
    capacidade = models.PositiveIntegerField()
    contacto = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class CategoriaEvento(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome

class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    organizador = models.ForeignKey(Organizador, on_delete=models.CASCADE, related_name='eventos')
    ativo = models.BooleanField(default=True)
    categoria = models.ForeignKey(CategoriaEvento, on_delete=models.SET_NULL, null=True, related_name='eventos')

    def __str__(self):
        return self.titulo

class GeneroArtista(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome

class Artista(models.Model):
    nome = models.CharField(max_length=100)
    bio = models.TextField()
    genero = models.ForeignKey(GeneroArtista, on_delete=models.SET_NULL, null=True, related_name='artistas')

    def __str__(self):
        return self.nome

class Sessao(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='sessoes')
    local = models.ForeignKey(Local, on_delete=models.CASCADE, related_name='sessoes')
    inicio = models.DateTimeField()
    fim = models.DateTimeField()
    preco = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.evento.titulo} @ {self.inicio}"

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)
    morada = models.CharField(max_length=200)
    data_registo = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Fatura(models.Model):
    ESTADO_CHOICES = [
        ('P', 'Paga'),
        ('N', 'Não Paga'),
        ('C', 'Cancelada'),
    ]
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='faturas')
    numero_unico = models.CharField(max_length=50, unique=True)
    data_emissao = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES)

    def save(self, *args, **kwargs):
        if not self.numero_unico:
            self.numero_unico = str(uuid.uuid4())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.numero_unico

class Bilhete(models.Model):
    TIPO_CHOICES = [
        ('NORMAL', 'Normal'),
        ('ESTUDANTE', 'Estudante'),
        ('SENIOR', 'Sénior'),
        ('VIP', 'VIP'),
        ('CRIANCA', 'Criança'),
    ]
    sessao = models.ForeignKey(Sessao, on_delete=models.CASCADE, related_name='bilhetes')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='bilhetes')
    codigo_unico = models.CharField(max_length=100, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    usado = models.BooleanField(default=False)
    comprado_em = models.DateTimeField(auto_now_add=True)
    preco_final = models.DecimalField(max_digits=8, decimal_places=2)
    lugar = models.CharField(max_length=20)

    def display_label(self):
        return f"{self.sessao.evento.titulo} — {self.get_tipo_display()} — {self.preco_final}€ — Lugar: {self.lugar}"

    def save(self, *args, **kwargs):
        if not self.codigo_unico:
            self.codigo_unico = str(uuid.uuid4())
        if not self.preco_final:
            tipo_multipliers = {
                'NORMAL': Decimal('1.0'),
                'ESTUDANTE': Decimal('0.7'),
                'SENIOR': Decimal('0.8'),
                'VIP': Decimal('1.5'),
                'CRIANCA': Decimal('0.5'),
            }
            multiplier = tipo_multipliers.get(self.tipo, Decimal('1.0'))
            self.preco_final = self.sessao.preco * multiplier
        super().save(*args, **kwargs)

    def __str__(self):
        return self.codigo_unico

class Performance(models.Model):
    artista = models.ForeignKey(Artista, on_delete=models.CASCADE, related_name='performances')
    sessao = models.ForeignKey(Sessao, on_delete=models.CASCADE, related_name='performances')
    duracao_estim = models.PositiveIntegerField(help_text="Duração em minutos")

    def __str__(self):
        return f"{self.artista.nome} em {self.sessao}"

class Avaliacao(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='avaliacoes')
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='avaliacoes')
    sessao = models.ForeignKey(Sessao, on_delete=models.CASCADE, related_name='avaliacoes', null=True, blank=True)
    nota = models.PositiveSmallIntegerField()
    comentario = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avaliação {self.nota} por {self.cliente.nome}"

class FaturasItem(models.Model):
    fatura = models.ForeignKey(Fatura, on_delete=models.CASCADE, related_name='itens')
    bilhete = models.OneToOneField(Bilhete, on_delete=models.CASCADE, related_name='fatura_item')

    def __str__(self):
        return f"Item {self.bilhete} na {self.fatura}"

    def clean(self):
        if self.fatura.cliente != self.bilhete.cliente:
            raise ValidationError("O bilhete deve pertencer ao mesmo cliente da fatura.")

    class Meta:
        verbose_name = "Item da Fatura"
        verbose_name_plural = "Itens da Fatura"