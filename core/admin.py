# admin.py - CORRIGIDO E SIMPLIFICADO
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Evento, Perfil, Comprovante

# Define uma inline para o Perfil
class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'Perfil'
    fields = ['telefone', 'matricula', 'curso', 'horas_completadas']

# Define uma nova classe UserAdmin que inclui a inline do Perfil
class CustomUserAdmin(UserAdmin):
    inlines = (PerfilInline,)
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'date_joined']
    list_filter = ['is_active', 'is_staff', 'is_superuser', 'groups']
    search_fields = ['username', 'email', 'first_name', 'last_name']

# Desregistra o User padrão e registra com a nova configuração
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'categoria', 'data', 'formato', 'admin_criador', 'criado_por', 'criado_em']
    list_filter = ['categoria', 'formato', 'data', 'admin_criador']
    search_fields = ['titulo', 'descricao', 'organizador']
    readonly_fields = ['criado_em']
    
    # Campos para exibir no formulário de edição
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'descricao', 'categoria', 'imagem_url')
        }),
        ('Detalhes do Evento', {
            'fields': ('formato', 'data', 'hora', 'local', 'link')
        }),
        ('Organização', {
            'fields': ('organizador', 'requisitos', 'horas', 'admin_criador')
        }),
        ('Sistema', {
            'fields': ('criado_por', 'criado_em')
        }),
    )

@admin.register(Comprovante)
class ComprovanteAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'emissor', 'carga_horaria', 'data_evento', 'status', 'data_envio']
    list_filter = ['status', 'data_evento', 'data_envio']
    search_fields = ['usuario__username', 'emissor', 'justificativa']
    readonly_fields = ['data_envio']
    
    fieldsets = (
        ('Informações do Comprovante', {
            'fields': ('usuario', 'evento', 'arquivo', 'emissor', 'carga_horaria', 'data_evento', 'categoria_sugerida')
        }),
        ('Requisitos do Documento', {
            'fields': ('contem_cnpj', 'contem_assinatura', 'contem_qrcode')
        }),
        ('Status', {
            'fields': ('status', 'justificativa', 'data_envio')
        }),
    )