from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    curso = models.CharField(max_length=100, blank=True, null=True)
    periodo = models.IntegerField(blank=True, null=True)
    interesses = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Perfil de {self.usuario.first_name}"

# Signal para criar perfil automaticamente
@receiver(post_save, sender=User)
def criar_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.get_or_create(usuario=instance)