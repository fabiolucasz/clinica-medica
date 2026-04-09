// Verificador de expiração de token
class TokenChecker {
    constructor() {
        this.checkInterval = 5 * 60 * 1000; // 5 minutos
        this.warningShown = false;
        this.init();
    }

    init() {
        // Só ativar se houver token na sessão
        if (this.hasToken()) {
            console.log('Token checker iniciado');
            this.startChecking();
        }
    }

    hasToken() {
        // Verificar se há indicadores de sessão ativa
        return document.querySelector('[data-user-role]') || 
               window.location.pathname.includes('/painel/') ||
               window.location.pathname.includes('/area_paciente/');
    }

    startChecking() {
        setInterval(() => {
            this.checkToken();
        }, this.checkInterval);
    }

    async checkToken() {
        try {
            // Fazer uma requisição simples para verificar se o token ainda é válido
            const response = await fetch('/api/check-token/', {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            if (response.status === 401) {
                // Token expirado
                this.handleTokenExpired();
            }
        } catch (error) {
            console.error('Erro ao verificar token:', error);
        }
    }

    handleTokenExpired() {
        if (!this.warningShown) {
            this.warningShown = true;
            
            // Mostrar alerta amigável
            const alertDiv = document.createElement('div');
            alertDiv.className = 'alert alert-warning alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3';
            alertDiv.style.zIndex = '9999';
            alertDiv.innerHTML = `
                <strong>Sessão expirada!</strong> Sua sessão expirou. Redirecionando para o login...
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;
            
            document.body.appendChild(alertDiv);

            // Redirecionar após 3 segundos
            setTimeout(() => {
                window.location.href = '/login/';
            }, 3000);
        }
    }
}

// Inicializar quando a página carregar
document.addEventListener('DOMContentLoaded', () => {
    new TokenChecker();
});
