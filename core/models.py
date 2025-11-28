from django.db import models
from django.contrib.auth.models import User
import uuid


class PaginaHome(models.Model):
    titulo = models.CharField(max_length=200)
    subtitulo = models.CharField(max_length=200, blank=True)
    texto_principal = models.TextField(blank=True)

    def __str__(self):
        return self.titulo


class PaginaPerfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200, default="Meu Perfil")
    descricao = models.TextField(blank=True)

    def __str__(self):
        return f"Perfil de {self.usuario.username}"


class PaginaInscricao(models.Model):
    titulo = models.CharField(max_length=200)
    instrucoes = models.TextField()

    def __str__(self):
        return self.titulo


class PaginaResumoHoras(models.Model):
    titulo = models.CharField(max_length=200)
    observacoes = models.TextField(blank=True)

    def __str__(self):
        return self.titulo


class Evento(models.Model):
    nome = models.CharField(max_length=200)
    data = models.DateField()
    codigo = models.CharField(max_length=8, blank=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = uuid.uuid4().hex[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome} ({self.codigo})"
