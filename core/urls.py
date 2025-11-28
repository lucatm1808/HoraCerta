from django.urls import path
from . import views

urlpatterns = [
    path('kaylane/', views.tela_index_kaylane, name='kaylane_home'),
    path('kaylane/criar-evento/', views.tela_criar_evento, name='criar_evento'),
    path('kaylane/inscricao/', views.tela_inscricao, name='inscricao'),
    path('kaylane/perfil/', views.tela_perfil, name='perfil'),
    path('kaylane/register/', views.tela_register, name='register'),
]