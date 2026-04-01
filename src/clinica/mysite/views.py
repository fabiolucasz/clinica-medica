from django.shortcuts import render, redirect
import requests

# Create your views here.
base_url = 'http://127.0.0.1:8001'

def token_required(view_func):
    """Decorator para verificar se o usuário tem token válido na sessão"""
    def wrapper(request, *args, **kwargs):
        token = request.session.get('fastapi_token')
        if not token:
            return redirect('login_view')
        
        # Opcional: validar o token a cada requisição
        # validated = validate_token(token)
        # if not validated:
        #     return redirect('login_view')
        
        return view_func(request, *args, **kwargs)
    return wrapper

def index(request):
    return render(request, 'index.html')

def login_view(request):
    login_url = f'{base_url}/auth/login-json/'
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        payload = {
            "email": username,
            "password": password
        }

        response = requests.post(login_url, json=payload)
        if response.status_code == 200:
            token = response.json()['access_token']
            # Criar sessão no Django com o token
            request.session['fastapi_token'] = token
            
            # Validar o token e obter dados completos do usuário
            validated = validate_token(token)
            if validated and validated.get('user'):
                request.session['user_data'] = validated['user']
                
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
    return redirect('login_view')