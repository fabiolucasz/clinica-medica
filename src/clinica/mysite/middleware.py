from django.shortcuts import redirect
from .views import validate_token

class TokenExpirationMiddleware:
    """Middleware para verificar expiração do token em todas as requisições"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Verificar se há token na sessão
        token = request.session.get('fastapi_token')
        
        if token:
            # Verificar se o token ainda é válido
            if not validate_token(token):
                # Token expirado - limpar sessão e redirecionar
                request.session.flush()
                return redirect('/login/')
        
        response = self.get_response(request)
        return response
