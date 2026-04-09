from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests

# Create your views here.
base_url = 'http://127.0.0.1:8001'

def token_required(view_func):
    """Decorator para verificar se o usuário tem token válido na sessão"""
    def wrapper(request, *args, **kwargs):
        token = request.session.get('fastapi_token')
        if not token:
            return redirect('/login/')
        
        # Validar o token a cada requisição
        validated = validate_token(token)
        if not validated:
            # Token expirado ou inválido - fazer logout automático
            request.session.flush()
            return redirect('/login/')
        
        return view_func(request, *args, **kwargs)
    return wrapper

def index(request):
    return render(request, 'index.html')

def login_view(request):
    login_url = f'{base_url}/login/access-token'
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # OAuth2 password flow - form data
        response = requests.post(
            login_url,
            data={
                "username": username,
                "password": password
            }
        )
        if response.status_code == 200:
            token = response.json()['access_token']
            # Criar sessão no Django com o token
            request.session['fastapi_token'] = token
            
            # Validar o token e obter dados completos do usuário
            validated = validate_token(token)
            if validated and validated.get('user'):
                request.session['user_data'] = validated['user']
                request.session['user_role'] = validated['user'].get('role')
                
                if validated['user']['role'] == 'administrador':
                    return redirect('painel:listar_pacientes')
                elif validated['user']['role'] == 'medico':
                    return redirect('area_paciente:index')
                elif validated['user']['role'] == 'paciente':
                    return redirect('area_paciente:index')
                else:
                    return render(request, 'index.html', {'error': 'Usuário não tem permissão para acessar esta aplicação'})
            else:
                return render(request, 'index.html', {'error': 'Erro ao validar token'})
        else:
            return render(request, 'registration/login.html', {'error': 'Usuário ou senha inválidos'})
    
    return render(request, 'registration/login.html')


def validate_token(token):
    response = requests.post(
        f'{base_url}/auth/validate-token',
        headers={'Authorization': f'Bearer {token}'}
    )
    if response.status_code == 200:
        return response.json()
    return None


def logout_view(request):
    # Limpar a sessão
    request.session.flush()
    return redirect('/login/')


def check_token(request):
    """Endpoint para verificação AJAX do token"""
    token = request.session.get('fastapi_token')
    
    if not token:
        return JsonResponse({'valid': False}, status=401)
    
    # Validar o token
    validated = validate_token(token)
    if not validated:
        # Limpar sessão se token expirou
        request.session.flush()
        return JsonResponse({'valid': False}, status=401)
    
    return JsonResponse({'valid': True})