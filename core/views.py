# views.py - ARQUIVO COMPLETO E CORRIGIDO
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone
from datetime import timedelta
from .models import Evento, Perfil, Comprovante, Inscricao
from django.contrib.auth import logout as auth_logout

# Decorator personalizado para verificar se é admin
def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, 'Acesso restrito a administradores.')
            return redirect('eventos_pagina')
        return view_func(request, *args, **kwargs)
    return wrapper

def tela_eventos_pagina(request):
    eventos = Evento.objects.all().order_by('-data')
    return render(request, 'eventos_pagina.html', {'eventos': eventos})

def tela_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    
    # Verificar se o usuário está inscrito neste evento
    inscrito = False
    if request.user.is_authenticated:
        inscrito = Inscricao.objects.filter(usuario=request.user, evento=evento).exists()
    
    return render(request, 'evento.html', {
        'evento': evento,
        'inscrito': inscrito
    })

@login_required
def tela_criar_evento(request):
    # Verificar se o usuário é administrador
    if not request.user.is_superuser:
        messages.error(request, 'Acesso restrito a administradores.')
        return redirect('eventos_pagina')
    
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        categoria = request.POST.get('categoria')
        formato = request.POST.get('formato')
        data = request.POST.get('data')
        hora = request.POST.get('hora')
        link = request.POST.get('link')
        requisitos = request.POST.get('requisitos')
        horas_str = request.POST.get('horas', '0')
        local = request.POST.get('local')
        organizador = request.POST.get('organizador')
        imagem_url = request.POST.get('imagem_url')
        admin_criador = request.POST.get('admin_criador') == 'on'
        
        try:
            horas = int(horas_str) if horas_str else 0
        except ValueError:
            horas = 0
            
        evento = Evento.objects.create(
            titulo=titulo,
            descricao=descricao,
            categoria=categoria,
            formato=formato,
            data=data,
            hora=hora,
            link=link,
            requisitos=requisitos,
            horas=horas,
            local=local,
            organizador=organizador,
            imagem_url=imagem_url,
            admin_criador=admin_criador,
            criado_por=request.user
        )
        
        if admin_criador:
            request.session['is_admin'] = True
        
        messages.success(request, 'Evento criado com sucesso!')
        return redirect('evento', evento_id=evento.id)
    
    return render(request, 'criar_evento.html')

@login_required
def editar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    
    # Verificar se o usuário é administrador OU criador do evento
    if not request.user.is_superuser and evento.criado_por != request.user:
        messages.error(request, 'Você não tem permissão para editar este evento.')
        return redirect('evento', evento_id=evento_id)
    
    if request.method == 'POST':
        evento.titulo = request.POST.get('titulo')
        evento.descricao = request.POST.get('descricao')
        evento.categoria = request.POST.get('categoria')
        evento.formato = request.POST.get('formato')
        evento.data = request.POST.get('data')
        evento.hora = request.POST.get('hora')
        evento.link = request.POST.get('link')
        evento.requisitos = request.POST.get('requisitos')
        
        horas_str = request.POST.get('horas', '0')
        try:
            evento.horas = int(horas_str) if horas_str else 0
        except ValueError:
            evento.horas = 0
            
        evento.local = request.POST.get('local')
        evento.organizador = request.POST.get('organizador')
        evento.imagem_url = request.POST.get('imagem_url')
        evento.save()
        
        messages.success(request, 'Evento atualizado com sucesso!')
        return redirect('evento', evento_id=evento.id)
    
    return render(request, 'editar_evento.html', {'evento': evento})

@login_required
def deletar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    
    # Verificar se o usuário é administrador OU criador do evento
    if not request.user.is_superuser and evento.criado_por != request.user:
        messages.error(request, 'Você não tem permissão para deletar este evento.')
        return redirect('evento', evento_id=evento_id)
    
    if request.method == 'POST':
        evento.delete()
        messages.success(request, 'Evento deletado com sucesso!')
        return redirect('eventos_pagina')
    
    return render(request, 'confirmar_delete.html', {'evento': evento})

def login_usuario(request):
    # Verificar se veio do logout
    logout_success = request.GET.get('logout') == 'success'
    
    if logout_success:
        messages.success(request, 'Logout realizado com sucesso!')
    
    if request.method == 'POST':
        # CORREÇÃO: O campo no template é 'email' (não 'username')
        email_or_username = request.POST.get('email')  # Mudei de 'username' para 'email'
        password = request.POST.get('senha')
        
        print(f"Tentando login com: {email_or_username}")
        
        # Primeiro, tentar autenticar como username
        user = authenticate(request, username=email_or_username, password=password)
        
        # Se não funcionar E se for um email (contém '@'), tentar buscar por email
        if user is None and email_or_username and '@' in email_or_username:
            try:
                # Buscar usuário pelo email
                user_by_email = User.objects.get(email=email_or_username)
                # Autenticar com o username encontrado
                user = authenticate(request, username=user_by_email.username, password=password)
                print(f"Usuário encontrado por email: {user_by_email.username}")
            except User.DoesNotExist:
                user = None
                print(f"Nenhum usuário encontrado com email: {email_or_username}")
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Login realizado com sucesso!')
            return redirect('eventos_pagina')
        else:
            print(f"Falha na autenticação para: {email_or_username}")
            messages.error(request, 'Email/usuário ou senha incorretos.')
    
    return render(request, 'login.html')

def logout_usuario(request):
    # Usar auth_logout do Django (mais confiável)
    auth_logout(request)
    
    # Limpar a sessão completamente
    request.session.flush()
    
    # Adicionar cabeçalhos para evitar cache
    response = redirect('login')

    
    return response

def registrar_usuario(request):
    if request.method == 'POST':
        nome_completo = request.POST.get('nome')  
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar')
        
        if senha != confirmar_senha:
            messages.error(request, 'As senhas não coincidem.')
            return redirect('register')
        
        # Criar username a partir do email
        username = email.split('@')[0]
        
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este e-mail já está cadastrado.')
            return redirect('register')
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=senha
        )
        
        # Separar nome e sobrenome
        nome_partes = nome_completo.split()
        if len(nome_partes) >= 2:
            user.first_name = ' '.join(nome_partes[:-1])  
            user.last_name = nome_partes[-1]  
        else:
            user.first_name = nome_completo
        
        user.save()
        
        # Criar perfil associado
        Perfil.objects.create(usuario=user)
        
        # Logar o usuário automaticamente após cadastro
        login(request, user)
        
        # Informar o usuário sobre seu username
        messages.success(request, f'Conta criada com sucesso! Seu nome de usuário é: {username}')
        messages.info(request, 'Você pode usar seu email ou nome de usuário para fazer login.')
        
        return redirect('eventos_pagina')
    
    return render(request, 'register.html')

@login_required
def perfil_usuario(request):
    try:
        perfil = Perfil.objects.get(usuario=request.user)
    except Perfil.DoesNotExist:
        perfil = Perfil.objects.create(usuario=request.user)
    
    return render(request, 'perfil.html', {'usuario': request.user, 'perfil': perfil})

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        usuario = request.user
        usuario.first_name = request.POST.get('first_name', usuario.first_name)
        usuario.last_name = request.POST.get('last_name', usuario.last_name)
        usuario.email = request.POST.get('email', usuario.email)
        usuario.save()
        
        perfil, created = Perfil.objects.get_or_create(usuario=usuario)
        perfil.telefone = request.POST.get('telefone', perfil.telefone)
        perfil.matricula = request.POST.get('matricula', perfil.matricula)
        perfil.curso = request.POST.get('curso', perfil.curso)
        perfil.save()
        
        messages.success(request, 'Perfil atualizado com sucesso!')
        return redirect('perfil')
    
    return render(request, 'editar_perfil.html')

@login_required
def deletar_conta(request):
    if request.method == 'POST':
        request.user.delete()
        messages.success(request, 'Sua conta foi excluída com sucesso.')
        return redirect('login')
    
    return render(request, 'confirmar_deletar_conta.html')

def login_admin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_superuser:
            login(request, user)
            messages.success(request, 'Login de administrador realizado!')
            return redirect('eventos_pagina')
        else:
            messages.error(request, 'Credenciais inválidas ou não é administrador.')
    
    return render(request, 'login_admin.html')

@login_required
def tela_inscricao(request):
    # Verificar se veio de um evento específico
    evento_id = request.GET.get('evento_id')
    
    if not evento_id:
        messages.error(request, 'Evento não especificado.')
        return redirect('eventos_pagina')
    
    try:
        evento = Evento.objects.get(id=evento_id)
    except Evento.DoesNotExist:
        messages.error(request, 'Evento não encontrado.')
        return redirect('eventos_pagina')
    
    # Verificar se já está inscrito
    if Inscricao.objects.filter(usuario=request.user, evento=evento).exists():
        messages.warning(request, 'Você já está inscrito neste evento!')
        return redirect('listar_inscricoes')
    
    if request.method == 'POST':
        # Criar inscrição
        Inscricao.objects.create(
            usuario=request.user,
            evento=evento,
            status='confirmada'
        )
        
        messages.success(request, f'Inscrição no evento "{evento.titulo}" realizada com sucesso!')
        return redirect('listar_inscricoes')
    
    return render(request, 'inscricao.html', {'evento': evento})

@login_required
def listar_inscricoes(request):
    inscricoes = Inscricao.objects.filter(usuario=request.user).order_by('-data_inscricao')
    
    # Filtrar por status se fornecido
    status_filtro = request.GET.get('status')
    if status_filtro and status_filtro != 'todos':
        inscricoes = inscricoes.filter(status=status_filtro)
    
    # Contar por status para os filtros
    total_inscricoes = inscricoes.count()
    inscricoes_pendentes = Inscricao.objects.filter(usuario=request.user, status='pendente').count()
    inscricoes_confirmadas = Inscricao.objects.filter(usuario=request.user, status='confirmada').count()
    inscricoes_canceladas = Inscricao.objects.filter(usuario=request.user, status='cancelada').count()
    inscricoes_participou = Inscricao.objects.filter(usuario=request.user, status='participou').count()
    
    context = {
        'inscricoes': inscricoes,
        'total_inscricoes': total_inscricoes,
        'inscricoes_pendentes': inscricoes_pendentes,
        'inscricoes_confirmadas': inscricoes_confirmadas,
        'inscricoes_canceladas': inscricoes_canceladas,
        'inscricoes_participou': inscricoes_participou,
        'status_filtro': status_filtro or 'todos',
    }
    
    return render(request, 'listar_inscricoes.html', context)

@login_required
def editar_inscricao(request, inscricao_id):
    try:
        inscricao = Inscricao.objects.get(id=inscricao_id, usuario=request.user)
    except Inscricao.DoesNotExist:
        messages.error(request, 'Inscrição não encontrada ou você não tem permissão para editá-la.')
        return redirect('listar_inscricoes')
    
    if request.method == 'POST':
        status = request.POST.get('status')
        observacoes = request.POST.get('observacoes')
        
        inscricao.status = status
        inscricao.observacoes = observacoes
        inscricao.save()
        
        messages.success(request, 'Inscrição atualizada com sucesso!')
        return redirect('listar_inscricoes')
    
    context = {
        'inscricao': inscricao,
    }
    
    return render(request, 'editar_inscricao.html', context)

@login_required
def cancelar_inscricao(request, inscricao_id):
    if request.method == 'POST':
        try:
            inscricao = Inscricao.objects.get(id=inscricao_id, usuario=request.user)
            inscricao.status = 'cancelada'
            inscricao.save()
            
            messages.success(request, f'Inscrição no evento "{inscricao.evento.titulo}" cancelada com sucesso!')
        except Inscricao.DoesNotExist:
            messages.error(request, 'Inscrição não encontrada ou você não tem permissão para cancelá-la.')
    
    return redirect('listar_inscricoes')

@login_required
def deletar_inscricao(request, inscricao_id):
    if request.method == 'POST':
        try:
            inscricao = Inscricao.objects.get(id=inscricao_id, usuario=request.user)
            evento_titulo = inscricao.evento.titulo
            inscricao.delete()
            
            messages.success(request, f'Inscrição no evento "{evento_titulo}" removida com sucesso!')
        except Inscricao.DoesNotExist:
            messages.error(request, 'Inscrição não encontrada ou você não tem permissão para removê-la.')
    
    return redirect('listar_inscricoes')

@login_required
def verificar_inscricao_evento(request, evento_id):
    """Verifica se o usuário está inscrito em um evento específico"""
    try:
        evento = Evento.objects.get(id=evento_id)
        inscrito = Inscricao.objects.filter(usuario=request.user, evento=evento).exists()
        
        return JsonResponse({
            'inscrito': inscrito,
            'evento_titulo': evento.titulo,
            'evento_id': evento.id
        })
    except Evento.DoesNotExist:
        return JsonResponse({'error': 'Evento não encontrado'}, status=404)

@login_required
def tela_resumo_horas(request):
    comprovantes = Comprovante.objects.filter(usuario=request.user)
    horas_totais = sum(c.carga_horaria for c in comprovantes if c.status == 'aprovado')
    horas_restantes = max(0, 120 - horas_totais)
    progress_percent = min(100, int((horas_totais / 120) * 100))
    
    # Calcular distribuição por categoria (apenas aprovados)
    categorias = {
        'evento_academico': {'nome': 'Eventos Acadêmicos', 'horas': 0, 'meta': 50, 'icon': 'fa-graduation-cap'},
        'extensao': {'nome': 'Extensão', 'horas': 0, 'meta': 20, 'icon': 'fa-hands-helping'},
        'cultura': {'nome': 'Cultura', 'horas': 0, 'meta': 20, 'icon': 'fa-palette'},
        'carreira': {'nome': 'Carreira', 'horas': 0, 'meta': 15, 'icon': 'fa-briefcase'},
        'esporte': {'nome': 'Esporte', 'horas': 0, 'meta': 15, 'icon': 'fa-running'},
    }
    
    for comprovante in comprovantes.filter(status='aprovado'):
        if comprovante.categoria_sugerida in categorias:
            categorias[comprovante.categoria_sugerida]['horas'] += comprovante.carga_horaria
    
    # Calcular porcentagens
    for key in categorias:
        cat = categorias[key]
        if cat['meta'] > 0:
            cat['percent'] = min(100, int((cat['horas'] / cat['meta']) * 100))
            cat['restante'] = max(0, cat['meta'] - cat['horas'])
        else:
            cat['percent'] = 0
            cat['restante'] = 0
    
    # Contar comprovantes pendentes
    pendentes = comprovantes.filter(status='pendente').count()
    
    context = {
        'comprovantes': comprovantes,
        'horas_totais': horas_totais,
        'horas_restantes': horas_restantes,
        'progress_percent': progress_percent,
        'pendentes': pendentes,
        'categorias': categorias,
    }
    
    return render(request, 'resumo_horas.html', context)

@login_required
def tela_envio_comprovante(request):
    if request.method == 'POST':
        arquivo = request.FILES.get('arquivo')
        emissor = request.POST.get('emissor')
        carga_horaria = request.POST.get('carga_horaria')
        data_evento = request.POST.get('data_evento')
        categoria_sugerida = request.POST.get('categoria_sugerida', 'outros')
        contem_cnpj = 'contem_cnpj' in request.POST
        contem_assinatura = 'contem_assinatura' in request.POST
        contem_qrcode = 'contem_qrcode' in request.POST
        
        # Validações
        if not arquivo:
            messages.error(request, 'Por favor, selecione um arquivo.')
            return render(request, 'envio_comprovante.html')
        
        if not carga_horaria or not carga_horaria.isdigit():
            messages.error(request, 'Carga horária inválida. Insira um número.')
            return render(request, 'envio_comprovante.html')
        
        # Criar comprovante
        comprovante = Comprovante.objects.create(
            usuario=request.user,
            arquivo=arquivo,
            emissor=emissor,
            carga_horaria=int(carga_horaria),
            data_evento=data_evento,
            categoria_sugerida=categoria_sugerida,
            contem_cnpj=contem_cnpj,
            contem_assinatura=contem_assinatura,
            contem_qrcode=contem_qrcode,
            status='pendente'
        )
        
        messages.success(request, 'Comprovante enviado com sucesso! Aguarde a análise.')
        return redirect('envio_comprovante')
    
    return render(request, 'envio_comprovante.html')

@login_required
def validacao_horas(request):
    # Apenas administradores podem acessar
    if not request.user.is_superuser:
        messages.error(request, 'Acesso restrito a administradores.')
        return redirect('eventos_pagina')
    
    # Filtros
    curso_filtro = request.GET.get('curso', 'Todos')
    categoria_filtro = request.GET.get('categoria', 'Todas')
    periodo_filtro = request.GET.get('periodo', 'Todos')
    status_filtro = request.GET.get('status', 'Todos')
    organizador_filtro = request.GET.get('organizador', 'Todos')
    
    # Buscar comprovantes pendentes por padrão
    comprovantes = Comprovante.objects.all().order_by('-data_envio')
    
    # Aplicar filtros
    if curso_filtro != 'Todos':
        comprovantes = comprovantes.filter(usuario__perfil__curso=curso_filtro)
    
    if categoria_filtro != 'Todas':
        comprovantes = comprovantes.filter(categoria_sugerida=categoria_filtro)
    
    if status_filtro != 'Todos':
        comprovantes = comprovantes.filter(status=status_filtro)
    else:
        # Por padrão, mostrar apenas pendentes
        comprovantes = comprovantes.filter(status='pendente')
    
    if organizador_filtro != 'Todos':
        comprovantes = comprovantes.filter(emissor__icontains=organizador_filtro)
    
    # Filtrar por período
    if periodo_filtro == 'ultimo_mes':
        um_mes_atras = timezone.now() - timedelta(days=30)
        comprovantes = comprovantes.filter(data_envio__gte=um_mes_atras)
    elif periodo_filtro == 'ultima_semana':
        uma_semana_atras = timezone.now() - timedelta(days=7)
        comprovantes = comprovantes.filter(data_envio__gte=uma_semana_atras)
    
    # Obter dados para os filtros
    cursos = Perfil.objects.exclude(curso__isnull=True).exclude(curso='').values_list('curso', flat=True).distinct()
    categorias = Comprovante.CATEGORIA_CHOICES
    organizadores = Comprovante.objects.values_list('emissor', flat=True).distinct()
    
    context = {
        'comprovantes': comprovantes,
        'cursos': cursos,
        'categorias': categorias,
        'organizadores': organizadores,
        'filtro_curso': curso_filtro,
        'filtro_categoria': categoria_filtro,
        'filtro_periodo': periodo_filtro,
        'filtro_status': status_filtro,
        'filtro_organizador': organizador_filtro,
    }
    
    return render(request, 'validacao_horas.html', context)

@login_required
@csrf_exempt
def aprovar_comprovante(request, comprovante_id):
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Acesso negado'}, status=403)
    
    if request.method == 'POST':
        try:
            comprovante = Comprovante.objects.get(id=comprovante_id)
            comprovante.status = 'aprovado'
            comprovante.save()
            
            # Atualizar horas completadas do usuário
            perfil, created = Perfil.objects.get_or_create(usuario=comprovante.usuario)
            perfil.horas_completadas += comprovante.carga_horaria
            perfil.save()
            
            return JsonResponse({'success': True})
        except Comprovante.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Comprovante não encontrado'}, status=404)
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'}, status=405)

@login_required
@csrf_exempt
def rejeitar_comprovante(request, comprovante_id):
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Acesso negado'}, status=403)
    
    if request.method == 'POST':
        data = json.loads(request.body)
        justificativa = data.get('justificativa', '')
        
        try:
            comprovante = Comprovante.objects.get(id=comprovante_id)
            comprovante.status = 'rejeitado'
            comprovante.justificativa = justificativa
            comprovante.save()
            
            return JsonResponse({'success': True})
        except Comprovante.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Comprovante não encontrado'}, status=404)
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'}, status=405)

@login_required
@csrf_exempt
def acao_em_lote(request):
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Acesso negado'}, status=403)
    
    if request.method == 'POST':
        data = json.loads(request.body)
        acao = data.get('acao')  # 'aprovar' ou 'rejeitar'
        ids = data.get('ids', [])
        justificativa = data.get('justificativa', '')
        
        if not ids:
            return JsonResponse({'success': False, 'error': 'Nenhum comprovante selecionado'})
        
        comprovantes = Comprovante.objects.filter(id__in=ids)
        
        if acao == 'aprovar':
            comprovantes.update(status='aprovado')
            # Atualizar horas para cada usuário
            for comprovante in comprovantes:
                perfil, created = Perfil.objects.get_or_create(usuario=comprovante.usuario)
                perfil.horas_completadas += comprovante.carga_horaria
                perfil.save()
                
        elif acao == 'rejeitar':
            comprovantes.update(status='rejeitado', justificativa=justificativa)
        
        return JsonResponse({'success': True, 'count': len(ids)})
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'}, status=405)

@login_required
def visualizar_comprovante(request, comprovante_id):
    if not request.user.is_superuser:
        messages.error(request, 'Acesso restrito a administradores.')
        return redirect('eventos_pagina')
    
    comprovante = get_object_or_404(Comprovante, id=comprovante_id)
    
    return render(request, 'visualizar_comprovante.html', {
        'comprovante': comprovante
    })