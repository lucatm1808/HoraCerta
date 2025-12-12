# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Autenticação e perfil
    path('register/', views.registrar_usuario, name='register'),
    path('', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
    path('perfil/', views.perfil_usuario, name='perfil'),
    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),
    path('deletar-conta/', views.deletar_conta, name='deletar_conta'),
    
    # Eventos
    path('criar-evento/', views.tela_criar_evento, name='criar_evento'),
    path('eventos-pagina/', views.tela_eventos_pagina, name='eventos_pagina'),
    path('evento/<int:evento_id>/', views.tela_evento, name='evento'),
    path('editar-evento/<int:evento_id>/', views.editar_evento, name='editar_evento'),
    path('deletar-evento/<int:evento_id>/', views.deletar_evento, name='deletar_evento'),
    
    # Comprovantes e horas
    path('envio-comprovante/', views.tela_envio_comprovante, name='envio_comprovante'),
    path('resumo-horas/', views.tela_resumo_horas, name='resumo_horas'),
    
    # Administração
    path('login-admin/', views.login_admin, name='login_admin'),
    path('validacao-horas/', views.validacao_horas, name='validacao_horas'),
    path('aprovar-comprovante/<int:comprovante_id>/', views.aprovar_comprovante, name='aprovar_comprovante'),
    path('rejeitar-comprovante/<int:comprovante_id>/', views.rejeitar_comprovante, name='rejeitar_comprovante'),
    path('acao-em-lote/', views.acao_em_lote, name='acao_em_lote'),
    path('visualizar-comprovante/<int:comprovante_id>/', views.visualizar_comprovante, name='visualizar_comprovante'),
    
    # Inscrições (CRUD) - NOVAS URLs
    path('inscricao/', views.tela_inscricao, name='inscricao'),
    path('inscricoes/', views.listar_inscricoes, name='listar_inscricoes'),
    path('inscricao/editar/<int:inscricao_id>/', views.editar_inscricao, name='editar_inscricao'),
    path('inscricao/cancelar/<int:inscricao_id>/', views.cancelar_inscricao, name='cancelar_inscricao'),
    path('inscricao/deletar/<int:inscricao_id>/', views.deletar_inscricao, name='deletar_inscricao'),
    path('inscricao/verificar/<int:evento_id>/', views.verificar_inscricao_evento, name='verificar_inscricao_evento'),
]