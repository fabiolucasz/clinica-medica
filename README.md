# Clinica Medica WhatsApp

Sistema completo de gestão de clínicas médicas com integração WhatsApp para confirmação, lembrete e cancelamento de consultas. Arquitetura moderna separada em API RESTful (FastAPI) e Frontend Server-Side (Django).

## Arquitetura

O sistema utiliza uma arquitetura em duas camadas:

```
┌─────────────────┐      HTTP/REST      ┌─────────────────┐      PostgreSQL
│   Django Web    │ ◄────────────────► │   FastAPI API   │ ◄─────────────►
│  (Porta 8000)   │   (Token JWT)      │  (Porta 8001)   │     Database
└─────────────────┘                    └─────────────────┘
   Templates HTML                           SQLAlchemy ORM
   Sessões de usuário                      Autenticação JWT
```

- **Frontend**: Django atua como proxy, consumindo a API FastAPI e renderizando templates HTML
- **Backend**: FastAPI fornece endpoints RESTful com autenticação JWT
- **Comunicação**: Django armazena token JWT em sessão e repassa em headers `Authorization: Bearer <token>`

## Tecnologias

### Backend - API (FastAPI)

| Tecnologia | Versão | Propósito |
|------------|--------|-----------|
| Python | 3.12+ | Linguagem principal |
| FastAPI | 0.135.2+ | Framework web async |
| SQLAlchemy | 2.0.48+ | ORM para PostgreSQL |
| Pydantic | 2.12.5+ | Validação de dados |
| python-jose | 3.5.0+ | Tokens JWT |
| passlib[bcrypt] | 1.7.4+ | Hash de senhas |
| psycopg2-binary | 2.9.11+ | Driver PostgreSQL |
| prometheus-client | 0.24.1+ | Métricas de monitoramento |
| structlog | 25.5.0+ | Logging estruturado |
| requests | 2.33.1+ | HTTP client |

### Frontend - Web (Django)

| Tecnologia | Versão | Propósito |
|------------|--------|-----------|
| Python | 3.12+ | Linguagem principal |
| Django | 6.0.2+ | Framework web |
| Django REST Framework | 3.16.1+ | Serialização de dados |
| django-filter | 25.2+ | Filtros de queryset |
| markdown | 3.10.2+ | Renderização de markdown |
| Bootstrap Icons | - | Ícones da interface |

## Estrutura do Projeto

```
clinica-medica-whatsapp/
├── api/                          # Backend FastAPI
│   └── src/
│       ├── routes/               # 17 módulos de endpoints
│       │   ├── agendamentos.py   # CRUD de agendamentos
│       │   ├── agenda.py         # Consulta de agenda
│       │   ├── pacientes.py      # Gestão de pacientes
│       │   ├── medicos.py        # Gestão de médicos
│       │   ├── clinicas.py       # Gestão de clínicas
│       │   ├── salas.py          # Gestão de salas
│       │   ├── user.py           # Autenticação JWT
│       │   └── ...               # Outros módulos
│       ├── models/               # SQLAlchemy models
│       ├── schemas/              # Pydantic schemas
│       ├── crud/                 # Operações de banco
│       ├── auth/                 # Lógica de autenticação
│       └── database/             # Configuração de conexão
│
└── web/                          # Frontend Django
    └── src/clinica/
        ├── painel/               # App principal
        │   ├── templates/        # Templates HTML
        │   │   ├── painel/
        │   │   │   ├── listar_consultas.html    # Agenda visual
        │   │   │   ├── gerenciar_consultas.html # Gestão com WhatsApp
        │   │   │   ├── dashboard.html           # Painel principal
        │   │   │   └── base.html                # Layout base
        │   ├── views.py          # Lógica de views
        │   ├── urls.py           # Roteamento
        │   └── static/           # CSS, JS, imagens
        ├── area_paciente/        # Portal do paciente
        └── mysite/               # Configuração Django
```

## Funcionalidades Implementadas

### Core - Gestão da Clínica
- **Clínicas**: Cadastro completo com endereço, CNPJ, contatos
- **Salas**: Organização por salas de atendimento
- **Especialidades**: Catálogo de especialidades médicas
- **Conselhos**: Tipos de conselho profissional (CRM, CRO, etc.)
- **Estados**: Cadastro de estados brasileiros

### Gestão de Pessoas
- **Pacientes**: Cadastro com dados pessoais, contato, endereço
- **Médicos**: Cadastro com especialidade, conselho, número do registro
- **Alocação**: Médicos em salas com horários específicos

### Agendamentos
- **Calendário Visual**: Agenda semanal com timeline de horários
- **Cores por Status**: Cards coloridos conforme situação
  - `aguardando` - Laranja/Amarelo
  - `confirmada` - Verde
  - `agendado` - Azul (padrão)
  - `cancelada` - Vermelho (opacidade reduzida)
  - `realizada` - Cinza
- **Scroll Sincronizado**: Timeline e grid de consultas rolam juntas
- **Filtros**: Por médico, período, status

### Gestão de Consultas (WhatsApp)
- **Lista Semanal**: Todas as consultas da semana de todos os médicos
- **Alteração de Status**: Dropdown para atualizar status em tempo real
- **Mensagens Prontas**:
  - Confirmação de consulta
  - Lembrete de consulta
  - Cancelamento
  - Confirmação recebida
  - Personalizada
- **Variáveis Dinâmicas**: `{nome}`, `{medico}`, `{data}`, `{hora}`, `{clinica}`
- **Integração WhatsApp Web**: Abre conversa direta com paciente

### Autenticação e Segurança
- **JWT Tokens**: Autenticação stateless com expiração
- **Validação de Token**: Endpoint `/auth/validate-token`
- **Middleware Django**: `TokenExpirationMiddleware` para renovação
- **Proteção CSRF**: Django CSRF em formulários e AJAX

### Monitoramento
- **Métricas Prometheus**: Endpoint `/metrics` na API
- **Logging Estruturado**: structlog com contexto de requisições

## Endpoints da API

### Autenticação
```
POST   /login/access-token         # Login (form)
POST   /auth/validate-token        # Validar token
POST   /signup                     # Cadastro de usuário
GET    /users/me                   # Perfil do usuário logado
```

### Gestão
```
GET    /medicos                    # Listar médicos
GET    /pacientes                  # Listar pacientes
GET    /clinicas                   # Listar clínicas
GET    /salas                      # Listar salas
GET    /especialidades             # Listar especialidades
GET    /estados                    # Listar estados
```

### Agenda
```
GET    /agenda-completa             # Agenda com médicos, vagas, agendamentos
POST   /agendar-consulta           # Criar agendamento
GET    /agendamentos/{id}         # Detalhes do agendamento
PATCH  /agendamentos/{id}/status   # Atualizar status (novo)
GET    /dados-agendamento         # Dados para formulário de agendamento
```

### Dashboard
```
GET    /dashboard/estatisticas    # Estatísticas para dashboard
```

## Variáveis de Ambiente

### API (`.env`)
```
DATABASE_URL=postgresql://user:pass@localhost:5432/clinica_db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Web (Django settings)
```python
SECRET_KEY = 'django-insecure-...'
DEBUG = True
BASE_URL = 'http://127.0.0.1:8001'  # URL da API FastAPI
```

## Execução Local

### Pré-requisitos
- Python 3.12+
- PostgreSQL 14+
- pip ou uv (gerenciador de pacotes)

### 1. Banco de Dados
```bash
# Criar banco PostgreSQL
createdb clinica_db
```

### 2. API (FastAPI)
```bash
cd api
uv sync                          # Instalar dependências
uv run python src/populate_db.py # Popular dados iniciais
uv run uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload
```

### 3. Web (Django)
```bash
cd web/src/clinica
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

### 4. Acesso
- **Django**: http://localhost:8000
- **API Docs**: http://localhost:8001/docs
- **Métricas**: http://localhost:8001/metrics

## Screenshots

### Homepage
Página inicial da clínica

![Homepage](pics/homepage.png)

### Dashboard
Estatísticas de consultas com gráficos

![Dashboard](pics/dashboard.png)

### Agenda Visual
Timeline semanal com consultas coloridas

![Agenda Visual](pics/agenda-visual.png)

### Gerenciar Consultas
Lista com filtros e botão WhatsApp

![Gerenciar Consultas](pics/gerenciar-consultas.png)

### Modal WhatsApp
Seleção de mensagem com preview

![Modal WhatsApp](pics/modal-whatsapp.png)


## Roadmap

- [ ] Área do paciente (portal web)
- [ ] Notificações push
- [ ] Relatórios em PDF
- [ ] Integração com calendários externos (Google Calendar)
- [ ] API RESTful pública para parceiros

## Licença

MIT License - Sistema desenvolvido para gestão de clínicas médicas.
