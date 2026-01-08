from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.models import User
from usuarios.forms import LoginForms, CadastroForms

def login(request):
    form = LoginForms()

    if request.method == 'POST':
        form = LoginForms(request.POST)

    if form.is_valid():
        nome_login = form['nome_login'].value()
        senha = form['senha'].value()

        usuario = auth.authenticate(
            request,
            username=nome_login,
            password=senha,
        )

        if usuario is not None:
            auth.login(request, usuario)
            messages.success(request, f'{nome_login} logado com sucesso!')
            return redirect('index')
        else:
            messages.error(request, 'Erro ao efetuar login')
            return redirect('login')

    return render(request, 'usuarios/login.html', {'form': form})

def cadastro(request):
    form = CadastroForms()

    if request.method == 'POST':
        form = CadastroForms(request.POST)
        
        if form.is_valid():
            nome_cadastro = form['nome_cadastro'].value()
            email = form['email'].value()
            senha = form['senha_1'].value()

            if User.objects.filter(username=nome_cadastro).exists():
                messages.error(request, 'Usuário já existente!')
                return redirect('cadastro')
            
            usuario = User.objects.create_user(
                username=nome_cadastro, 
                email=email, 
                password=senha)
            
            # Gravar usuário no DB
            usuario.save()

            # Cadastra o usuário e o leva ao login
            messages.success(request, 'Cadastro efetuado com sucesso!')
            return redirect('login')

    return render(request, 'usuarios/cadastro.html', {'form': form})

def logout(request):
    auth.logout(request)
    messages.success(request, 'Logout efetuado com sucesso!')
    return redirect('login')
