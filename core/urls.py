from django.urls import path
from . import views

urlpatterns = [
    path("", views.tela_index_kaylane, name="kaylane_home"),
    path("validacao_horas/", views.tela_validacao_horas, name="validacao_horas"),
    path("criar-evento/", views.tela_criar_evento, name="criar_evento"),
    path("inscricao/", views.tela_inscricao, name="inscricao"),
    path("perfil/", views.tela_perfil, name="perfil"),
    path("register/", views.tela_register, name="register"),
    path("resumo-horas/", views.tela_resumo_horas, name="resumo_horas"),
    path("envio-comprovante/", views.tela_envio_comprovante, name="envio_comprovante"),
    path("evento/", views.tela_evento, name="evento"),
    path("eventos-pagina/", views.tela_eventos_pagina, name="eventos_pagina"),
    path("validacao-horas/", views.tela_validacao_horas, name="validacao_horas"),
]
