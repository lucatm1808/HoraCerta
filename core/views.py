from django.shortcuts import render
from .models import PaginaHome, PaginaPerfil, PaginaInscricao, PaginaResumoHoras


def tela_index_kaylane(request):
    home = PaginaHome.objects.first()
    contexto = {"home": home}
    return render(request, "index_kaylane.html", contexto)


def tela_criar_evento(request):
    return render(request, "criar_evento.html")


def tela_inscricao(request):
    pagina = PaginaInscricao.objects.first()
    contexto = {"pagina": pagina}
    return render(request, "inscricao.html", contexto)


def tela_perfil(request):
    perfil = None
    if request.user.is_authenticated:
        try:
            perfil = PaginaPerfil.objects.get(usuario=request.user)
        except PaginaPerfil.DoesNotExist:
            perfil = None
    contexto = {"perfil": perfil}
    return render(request, "perfil.html", contexto)


def tela_register(request):
    return render(request, "register.html")


def tela_resumo_horas(request):
    pagina = PaginaResumoHoras.objects.first()
    contexto = {"pagina": pagina}
    return render(request, "resumo_horas.html", contexto)


def tela_envio_comprovante(request):
    return render(request, "envio_comprovante.html")


def tela_evento(request):
    return render(request, "evento.html")


def tela_eventos_pagina(request):
    return render(request, "eventos_pagina.html")


def tela_validacao_horas(request):
    return render(request, "validacao_horas.html")
