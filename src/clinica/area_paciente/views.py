from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.urls import reverse_lazy

# Create your views here.

def index(request):
    # TODO: Implementar lógica de login
    return render(request, 'area_paciente/index.html')

def dashboard(request):
    # TODO: Implementar lógica de dashboard
    
    return render(request, 'area_paciente/dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('login')