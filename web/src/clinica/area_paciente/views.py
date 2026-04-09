from django.shortcuts import render, redirect
from django.contrib.auth import logout

# Create your views here.


def index(request):
    return render(request, 'area_paciente/dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('login')