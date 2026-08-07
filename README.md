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
| boto3 | 1.35.0+ | Cliente AWS S3 para Supabase Storage |
| filetype | 1.2.0+ | Detecção de tipo de arquivo |
| python-multipart | 0.0.9+ | Upload de arquivos multipart |
| openai | 2.53.0+ | Cliente OpenAI para chat com IA |

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
│       ├── routes/               # 18 módulos de endpoints
│       │   ├── agendamentos.py   # CRUD de agendamentos
│       │   ├── agenda.py         # Consulta de agenda
│       │   ├── pacientes.py      # Gestão de pacientes
│       │   ├── medicos.py        # Gestão de médicos
│       │   ├── clinicas.py       # Gestão de clínicas
│       │   ├── salas.py          # Gestão de salas
│       │   ├── user.py           # Autenticação JWT
│       │   ├── upload.py         # Upload de arquivos
│       │   └── ...               # Outros módulos
│       ├── models/               # SQLAlchemy models
│       ├── schemas/              # Pydantic schemas
│       ├── crud/                 # Operações de banco
│       ├── auth/                 # Lógica de autenticação
│       ├── storage/              # Integração com Storage
│       │   └── supabase.py       # Cliente S3 Supabase
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
        │   │   │   ├── cadastrar_paciente.html  # Cadastro com foto
        │   │   │   ├── cadastrar_medico.html    # Cadastro com documentos
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
- **Pacientes**: Cadastro com dados pessoais, contato, endereço, **foto de perfil**
- **Médicos**: Cadastro com especialidade, conselho, número do registro, **documentos profissionais**
- **Alocação**: Médicos em salas com horários específicos

### Upload de Arquivos (Supabase Storage)
- **Fotos de Perfil**: Upload para pacientes e médicos (PNG, JPG, JPEG - máx 5MB)
- **Documentos Profissionais**: Upload de PDFs para médicos (RG, CPF, Diploma, Certificados - máx 10MB)
- **Integração S3**: Armazenamento em bucket Supabase com estrutura organizada por usuário
- **Validação**: Verificação de tipo MIME e tamanho de arquivo
- **Permissões**: Controle de acesso por roles (admin, médico, atendente)

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

### Storage
- **Supabase Storage**: Integração S3-compatible para armazenamento de arquivos
- **Bucket Structure**: `/{user_id}/profile/` para fotos e `/{user_id}/documents/` para documentos

### Chat com Inteligência Artificial
- **Assistente Virtual**: Chatbot para coleta de dados de pacientes
- **Extração Estruturada**: IA extrai automaticamente informações do paciente (nome, whatsapp, data de nascimento, especialidade desejada, convênio)
- **Armazenamento em Memória**: Histórico de chat armazenado temporariamente na memória do servidor
- **Persistência de Leads**: Dados estruturados salvos no banco de dados quando coleta é completa
- **Integração OpenAI**: Usa modelo GPT-4o-mini para respostas contextuais
- **Contexto da Clínica**: IA treinada para atuar como assistente de agendamento

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

### Upload
```
POST   /upload/profile-image/{user_id}    # Upload foto de perfil
POST   /upload/document/{user_id}         # Upload documento profissional
DELETE /upload/file/{user_id}            # Remover arquivo
GET    /upload/validation-info           # Informações de validação
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

### Chat com IA
```
POST   /chat                       # Enviar mensagem e receber resposta da IA
GET    /leads                      # Listar leads (requer autenticação)
```

## Variáveis de Ambiente

### API (`.env`)
```
DATABASE_URL=postgresql://user:pass@localhost:5432/clinica_db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Supabase Storage Configuration
SUPABASE_STORAGE_URL=https://seu-projeto.storage.supabase.co
SUPABASE_S3_ENDPOINT=https://seu-projeto.storage.supabase.co/storage/v1/s3
SUPABASE_ACCESS_KEY=sua-access-key-s3
SUPABASE_SECRET_KEY=sua-secret-key-s3
SUPABASE_REGION=sa-east-1
SUPABASE_BUCKET=clinica-files

# OpenAI Configuration
AI_API_KEY=sk-proj-...  # Sua API key da OpenAI
AI_BASE_URL=https://api.openai.com/v1
AI_MODEL=gpt-4o-mini
```

### Web (Django settings)
```python
SECRET_KEY = 'django-insecure-...'
DEBUG = True
BASE_URL = 'http://127.0.0.1:8001'  # URL da API FastAPI
```

## Execução com Docker Compose

### Pré-requisitos
- Docker
- Docker Compose

### 1. Clonar e entrar no projeto
```bash
git clone https://github.com/fabiolucasz/clinica-medica.git
```

```bash
cd clinica-medica
```

### 2. Iniciar os serviços
```bash
docker compose up -d --build
```



### 3. Acesso
- **Django**: http://localhost:8000
- **API Docs**: http://localhost:8001/docs
- **Métricas**: http://localhost:8001/metrics

### Comandos úteis
```bash
# Ver logs
docker compose logs -f

# Parar serviços
docker compose down

# Rebuild após alterações
docker compose up -d --build

# Acessar shell do container web
docker compose exec web sh

# Acessar shell do container api
docker compose exec api sh
```

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

- [x] **Upload de arquivos**: Fotos de perfil e documentos com Supabase Storage
- [x] **Chat com IA**: Assistente virtual para coleta de dados de pacientes
- [ ] Área do paciente (portal web)
- [ ] Notificações push
- [ ] Relatórios em PDF
- [ ] Integração com calendários externos (Google Calendar)
- [ ] API RESTful pública para parceiros

## Licença

MIT License - Sistema desenvolvido para gestão de clínicas médicas.
