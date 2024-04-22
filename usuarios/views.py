from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.models import User

# Crie suas views aqui.
def cadastro(request): 
    if  request.method == "GET": 
        return render(request, 'cadastro.html')
    elif request.method  == "POST":
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        username = request.POST.get('username')
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        confirmar_senha = request.POST.get('confirmar_senha')
        
        if senha != confirmar_senha:
            messages.add_message(request, constants.ERROR, "As senhas informadas devem ser iguais!")
            return redirect('/usuarios/cadastro')
        if len(senha) < 6: 
            messages.add_message(request, constants.ERROR, "A senha não pode ter menos do que 6 caracteres!")
            return redirect('/usuarios/cadastro')
            
        users = User.objects.filter(username=username)
        
        if users.exists(): 
            messages.add_message(request, constants.ERROR, "Usuário já existe no sistema!")
            return redirect('/usuarios/cadastro')
        
        User.objects.create_user(
        first_name=nome,
        last_name=sobrenome,
        username=username,
        email=email,
        password=senha
        )
            
        return redirect('/usuarios/login')

def login_view(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        
        user = auth.authenticate(request, username=username, password=senha)
        
        if user:
            auth.login(request, user)
            return redirect('/pacientes/home')
        
        messages.add_message(request, constants.ERROR, 'Usuário e/ou senha inválidos!')
        return redirect('/usuarios/login')
    
    
def sair(request):
    auth.logout(request)
    return redirect('/usuarios/login')    