from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('criar-evento/', views.criar_evento, name='criar_evento'),
    path('perfil/', views.perfil, name='perfil'),
    path('inscricao/', views.inscricao, name='inscricao'),
    path('registro/', views.registro, name='registro'),
    path('test/', views.test, name='test'),
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/excluir/<int:user_id>/', views.excluir_usuario, name='excluir_usuario'),
    
    # Novas URLs de autenticação
    path('login/', views.fazer_login, name='fazer_login'),
    path('logout/', views.fazer_logout, name='fazer_logout'),
]