from django.shortcuts import redirect, render
from usuarios.models import Usuario
from django.contrib import auth
from django.contrib import messages
from django.contrib.messages import constants

# Create your views here.
def login(request):
    if request.user.is_authenticated:
        redirect('registros/listar_cadastros/?enviado=false')
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        login = request.POST.get('login')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=login, password=password)
        if user:
            auth.login(request, user)
            return redirect('/registros/listar_cadastros/?enviado=false')
        else:
            messages.add_message(request, constants.ERROR, 'Login ou senha inválidos!')
            return redirect('/usuarios/login')

def logout(request):
    auth.logout(request)
    return redirect('/usuarios/login')

        
