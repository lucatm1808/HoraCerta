from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Perfil

def home(request):
    # Se o usuário já estiver autenticado, redireciona para criar_evento
    if request.user.is_authenticated:
        return redirect('criar_evento')
    else:
        # Se não estiver autenticado, redireciona para o login
        return redirect('fazer_login')

def test(request):
    return render(request, 'index.html')

def criar_evento(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo', '').strip()
        context = {'success': True, 'titulo': titulo}
        return render(request, 'criar_evento.html', context)
    return render(request, 'criar_evento.html')

@login_required
def perfil(request):
    # O perfil será criado automaticamente pelo signal quando o usuário for criado
    perfil = get_object_or_404(Perfil, usuario=request.user)
    
    if request.method == 'POST':
        # Atualizar informações básicas do usuário
        request.user.first_name = request.POST.get('nome', '').strip()
        request.user.email = request.POST.get('email', '').strip()
        request.user.save()
        
        # Atualizar perfil
        perfil.curso = request.POST.get('curso', '').strip()
        perfil.periodo = request.POST.get('periodo', '').strip()
        perfil.interesses = request.POST.get('interesses', '').strip()
        perfil.save()
        
        # Atualizar senha se fornecida
        senha_atual = request.POST.get('senha_atual', '').strip()
        nova_senha = request.POST.get('nova_senha', '').strip()
        confirmar_senha = request.POST.get('confirmar_senha', '').strip()
        
        if senha_atual and nova_senha and confirmar_senha:
            if request.user.check_password(senha_atual):
                if nova_senha == confirmar_senha:
                    request.user.set_password(nova_senha)
                    request.user.save()
                    update_session_auth_hash(request, request.user)
                    messages.success(request, 'Senha atualizada com sucesso!')
                else:
                    messages.error(request, 'As senhas não coincidem.')
            else:
                messages.error(request, 'Senha atual incorreta.')
        
        messages.success(request, 'Perfil atualizado com sucesso!')
        return redirect('perfil')
    
    context = {
        'perfil': perfil,
        'user': request.user
    }
    return render(request, 'perfil.html', context)

def inscricao(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        return render(request, 'inscricao.html', {'confirmed': True, 'email': email})
    return render(request, 'inscricao.html')

def registro(request):
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        email = request.POST.get('email', '').strip()
        senha = request.POST.get('senha', '').strip()
        confirmar = request.POST.get('confirmar', '').strip()

        if senha == confirmar and nome and email:
            # Verificar se usuário já existe
            if User.objects.filter(email=email).exists():
                context = {'error': 'Este email já está cadastrado.'}
                return render(request, 'register.html', context)
            else:
                # Criar novo usuário - O PERFIL SERÁ CRIADO AUTOMATICAMENTE PELO SIGNAL
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=senha,
                    first_name=nome
                )
                # NÃO criar perfil manualmente aqui - o signal cuida disso
                
                # Fazer login automático
                user = authenticate(username=email, password=senha)
                if user is not None:
                    login(request, user)
                    messages.success(request, f'Bem-vindo(a), {nome}!')
                    return redirect('perfil')
        else:
            context = {'error': 'Por favor, preencha todos os campos corretamente.'}
            return render(request, 'register.html', context)

    return render(request, 'register.html')

# Views administrativas
@login_required
def listar_usuarios(request):
    # Se não for superusuário, mostra mensagem de erro mas NÃO redireciona
    if not request.user.is_superuser:
        messages.error(request, 'Acesso não autorizado. Apenas administradores podem visualizar esta página.')
        # Em vez de redirect, vamos renderizar a página com a mensagem de erro
        usuarios = User.objects.none()  # Lista vazia
    else:
        usuarios = User.objects.all().select_related('perfil')
    
    return render(request, 'listar_usuarios.html', {'usuarios': usuarios})

@login_required
def excluir_usuario(request, user_id):
    if not request.user.is_superuser:
        messages.error(request, 'Acesso não autorizado.')
        return redirect('home')
    
    usuario = get_object_or_404(User, id=user_id)
    if usuario != request.user:
        usuario.delete()
        messages.success(request, 'Usuário excluído com sucesso!')
    else:
        messages.error(request, 'Você não pode excluir sua própria conta!')
    
    return redirect('listar_usuarios')

def fazer_login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        senha = request.POST.get('senha', '').strip()
        
        # Autenticar o usuário
        user = authenticate(request, username=email, password=senha)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bem-vindo de volta, {user.first_name}!')
            return redirect('perfil')
        else:
            messages.error(request, 'Email ou senha incorretos.')
    
    return render(request, 'login.html')

def fazer_logout(request):
    logout(request)
    messages.success(request, 'Você saiu da sua conta.')
    return redirect('home')