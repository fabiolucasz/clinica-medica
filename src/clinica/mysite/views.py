from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

# Create your views here.

def index(request):

    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('painel:index')
        else:
            return render(request, 'registration/login.html', {'error': 'Usuário ou senha inválidos'})
    
    return render(request, 'registration/login.html')


