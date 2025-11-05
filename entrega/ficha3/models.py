from django.db import models

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