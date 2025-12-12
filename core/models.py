# models.py - CONTEÚDO COMPLETO E CORRETO
from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    matricula = models.CharField(max_length=20, blank=True, null=True)
    curso = models.CharField(max_length=100, blank=True, null=True)
    horas_completadas = models.IntegerField(default=0)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.usuario.email

class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    categoria = models.CharField(max_length=100, blank=True, null=True)
    formato = models.CharField(max_length=20, choices=[('presencial', 'Presencial'), ('remoto', 'Remoto')])
    data = models.DateField()
    hora = models.TimeField()
    link = models.URLField(blank=True, null=True)
    requisitos = models.TextField(blank=True, null=True)
    imagem_url = models.URLField(blank=True, null=True)
    horas = models.IntegerField(default=0)
    local = models.CharField(max_length=200, blank=True, null=True)
    organizador = models.CharField(max_length=200, blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    admin_criador = models.BooleanField(default=False)
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.titulo

class Comprovante(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aprovado', 'Aprovado'),
        ('rejeitado', 'Rejeitado'),
    ]
    
    CATEGORIA_CHOICES = [
        ('evento_academico', 'Evento Acadêmico'),
        ('extensao', 'Extensão'),
        ('cultura', 'Cultura'),
        ('carreira', 'Carreira'),
        ('esporte', 'Esporte'),
        ('outros', 'Outros'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    evento = models.ForeignKey('Evento', on_delete=models.SET_NULL, null=True, blank=True)
    arquivo = models.FileField(upload_to='comprovantes/')
    emissor = models.CharField(max_length=200)
    carga_horaria = models.IntegerField(help_text="Carga horária em horas")
    data_evento = models.DateField()
    categoria_sugerida = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, default='outros')
    contem_cnpj = models.BooleanField(default=False)
    contem_assinatura = models.BooleanField(default=False)
    contem_qrcode = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    justificativa = models.TextField(blank=True, null=True)
    data_envio = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comprovante de {self.usuario.username} - {self.data_evento}"
    
    def get_categoria_sugerida_display(self):
        return dict(self.CATEGORIA_CHOICES).get(self.categoria_sugerida, self.categoria_sugerida)

class Inscricao(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
        ('participou', 'Participou'),
        ('ausente', 'Ausente'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    data_inscricao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    observacoes = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ['usuario', 'evento']  # Evita inscrição duplicada
    
    def __str__(self):
        return f"{self.usuario.username} - {self.evento.titulo} ({self.status})"