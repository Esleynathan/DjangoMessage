from django.shortcuts import render
from django.http import HttpResponse
from . models import Usuario
from django.shortcuts import redirect
from hashlib import sha256
from django.contrib import messages
from django.contrib.messages import constants

def login (request):
    status = request.GET.get ('status')
    return render(request, 'login.html', {'status': status})
    
def cadastro (request):
    status = request.GET.get ('status')
    return render(request, 'cadastro.html', {'status': status})
    

def valida_cadastro (request):
    nome = request.POST.get('nome')    
    email = request.POST.get('email')    
    senha = request.POST.get('senha')

    if len(nome.strip()) == 0 or len(email.strip()) == 0:        
        messages.add_message(request, constants.ERROR, 'Nome e email não podem estar vazio.')
        
        return redirect('/auth/cadastro/')

    if len(senha) < 8:
        messages.add_message(request, constants.ERROR, 'Sua senha deve ter no minimo 8 caracteres.')
        return redirect('/auth/cadastro/')
    
    usuario = Usuario.objects.filter(email = email)
    if len(usuario) > 0:
        messages.add_message(request, constants.ERROR, 'Email já cadastrado.')
        return redirect('/auth/cadastro/')

    try:
        senha = sha256 (senha.encode()).hexdigest()

        usuario = Usuario(nome=nome,
                        email=email,
                        senha= senha)
        usuario.save()
        
        messages.add_message(request, constants.SUCCESS, 'Cadastro realizado com suceso.')
        return redirect('/auth/cadastro/')
    except:
        
        messages.add_message(request, constants.ERROR, 'Erro interno do sistema.')
        return redirect('/auth/cadastro/')

def valida_login(request):
    email = request.POST.get('email')    
    senha = request.POST.get('senha')
    senha = sha256 (senha.encode()).hexdigest()

    usuario = Usuario.objects.filter(email = email).filter(senha = senha)
    if len(usuario) == 0:        
        messages.add_message(request, constants.WARNING, 'Email ou senha invalidos.')
        return redirect ('/auth/login/')
    elif len(usuario) > 0:
        request.session['logado'] = True
        request.session['usuario_id'] = usuario[0].id       
        return redirect ('/plataforma/home')

def sair(request):    
    request.session.flush()    
    messages.add_message(request, constants.WARNING, 'Faça login antes de acessar o sistema.')
    return redirect('/auth/login/')