from django.shortcuts import render

def tela_index_kaylane(request):
    return render(request, 'index_kaylane.html')

def tela_criar_evento(request):
    return render(request, 'criar_evento.html')

def tela_inscricao(request):
    return render(request, 'inscricao.html')

def tela_perfil(request):
    return render(request, 'perfil.html')

def tela_register(request):
    return render(request, 'register.html')

def tela_resumo_horas(request):
    return render(request, 'resumo_horas.html')

def tela_envio_comprovante(request):
    return render(request, 'envio_comprovante.html')    