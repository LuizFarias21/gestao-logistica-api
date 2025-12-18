
# API Sistema de Gestão de Logística e Entregas

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg?logo=python)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-5.0%2B-green.svg?logo=Django)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.16%2B-red.svg?logo=django)](https://www.django-rest-framework.org/)
[![SQLite](https://img.shields.io/badge/SQLite-003B57.svg?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Ruff](https://img.shields.io/badge/Ruff-0.14.7-FCC21B.svg?logo=ruff&logoColor=black)](https://docs.astral.sh/ruff/)
[![Faker](https://img.shields.io/badge/Faker-39.0.0-orange.svg)](https://faker.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)




## Instituições de Fomento e Parceria
[![Website IFB](https://img.shields.io/badge/Website-IFB-%23508C3C.svg?labelColor=%23C8102E)](https://www.ifb.edu.br/) 
[![Website ihwbr](https://img.shields.io/badge/Website-ihwbr-%23DAA520.svg?labelColor=%232E2E2E)](https://hardware.org.br/)

## Orientador
[![GitHub diegomo2](https://img.shields.io/badge/GitHub-diegomo2_(Diego_Martins)-%23181717.svg?logo=github&logoColor=white)](https://github.com/diegomo2)
[![Lattes Diego Martins](https://img.shields.io/badge/Lattes-Diego_Martins-green.svg?logo=cnpq&logoColor=white)](http://lattes.cnpq.br/3680205494685813)

## Sumário

- [Visão Geral](#visão-geral)
- [Pacotes Utilizados](#pacotes-utilizados)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Diagrama de Banco de Dados](#diagrama-de-banco-de-dados)
- [Documentação da API](#documentação-da-api)
- [Configuração do Ambiente](#configuração-do-ambiente)

## Visão Geral

API REST desenvolvida em Django para gerenciamento de logística e entregas. O sistema permite o controle completo de clientes, motoristas, veículos, rotas e entregas, fornecendo funcionalidades para:

- **Gestão de Clientes**: Cadastro e gerenciamento de clientes solicitantes de entregas
- **Gestão de Motoristas**: Controle de motoristas com status de disponibilidade e histórico de entregas
- **Gestão de Veículos**: Controle de frota com capacidade, tipo e status de cada veículo
- **Gestão de Rotas**: Planejamento e acompanhamento de rotas de entrega
- **Gestão de Entregas**: Sistema completo de rastreamento de entregas com código único

O sistema utiliza autenticação por token e implementa controle de permissões baseado em perfis (Gestor, Motorista e Cliente), garantindo que cada usuário tenha acesso apenas às funcionalidades apropriadas ao seu papel.

## Pacotes Utilizados

| Pacote                  | Versão       | Descrição                                      |
|-------------------------|--------------|------------------------------------------------|
| Django                  | 5.2.8        | Framework web principal                        |
| djangorestframework     | 3.16.1       | Toolkit para construção de APIs REST           |
| drf-spectacular         | 0.29.0       | Geração automática de documentação OpenAPI/Swagger |
| drf-spectacular-sidecar | 2025.12.1    | Arquivos estáticos para UI do Swagger          |
| django-filter           | 25.2         | Filtragem avançada de querysets               |
| Faker                   | 39.0.0       | Geração de dados fictícios para testes         |
| PyYAML                  | 6.0.3        | Parser e emitter para YAML                     |
| ruff                    | 0.14.7       | Linter e formatador de código Python           |

> **Nota:** Consulte o arquivo `requirements.txt` para a lista completa e versões exatas.

## Estrutura do Projeto

```
gestao-logistica-api/
├── manage.py                  # Script de gerenciamento do Django
├── requirements.txt           # Dependências do projeto
├── db.sqlite3                # Banco de dados SQLite
├── README.md                 # Documentação do projeto
├── CONTRIBUTING.md           # Guia de contribuição
├── config/                   # Configurações do projeto Django
│   ├── __init__.py
│   ├── settings.py          # Configurações principais
│   ├── urls.py              # URLs raiz do projeto
│   ├── asgi.py              # Configuração ASGI
│   └── wsgi.py              # Configuração WSGI
├── core/                     # App principal da aplicação
│   ├── __init__.py
│   ├── models.py            # Modelos: Cliente, Motorista, Veículo, Rota, Entrega
│   ├── views.py             # ViewSets da API
│   ├── serializers.py       # Serializers do DRF
│   ├── urls.py              # Rotas da API
│   ├── permissions.py       # Permissões customizadas
│   ├── admin.py             # Configuração do Django Admin
│   ├── apps.py              # Configuração da app
│   ├── management/
│   │   └── commands/
│   │       └── popular_banco.py  # Comando para popular banco de dados
│   └── migrations/          # Migrações do banco de dados
└── docs/                     # Documentação adicional
```

### Descrição dos Módulos

- **config/**: Contém as configurações centrais do Django, incluindo settings, URLs principais e configurações WSGI/ASGI
- **core/**: Aplicação principal contendo toda a lógica de negócio, modelos de dados, serializers e views da API
- **management/commands/**: Scripts personalizados do Django, incluindo comando para popular o banco de dados com dados de teste

## Diagrama de Banco de Dados

### Modelos Principais

#### Cliente
- **Campos**: user (OneToOne com User), nome, endereco, telefone
- **Relacionamentos**: Uma entrega pertence a um cliente

#### Motorista
- **Campos**: user (OneToOne com User), nome, cpf, cnh, telefone, status (disponivel/em_rota/inativo), data_cadastro
- **Relacionamentos**: Um motorista pode ter um veículo e várias rotas/entregas

#### Veículo
- **Campos**: placa, modelo, tipo (CARRO/VAN/CAMINHAO), capacidade_maxima, km_atual, status (DISPONIVEL/EM_USO/MANUTENCAO), motorista
- **Relacionamentos**: Um veículo é atribuído a um motorista e pode estar em várias rotas

#### Rota
- **Campos**: motorista, veiculo, nome, descricao, data_rota, status (planejada/em_andamento/concluida)
- **Relacionamentos**: Uma rota pertence a um motorista e veículo, e contém várias entregas

#### Entrega
- **Campos**: codigo_rastreio (único), cliente, rota, motorista, endereco_origem, endereco_destino, status (pendente/em_transito/entregue/cancelada), capacidade_necessaria, valor_frete, data_solicitacao, data_entrega_prevista, data_entrega_real, observacoes
- **Relacionamentos**: Uma entrega pertence a um cliente e pode estar associada a uma rota e motorista

### Relacionamentos
```
User ──1:1── Cliente ──1:N── Entrega
User ──1:1── Motorista ──1:1── Veículo
Motorista ──1:N── Rota ──1:N── Entrega
Veículo ──1:N── Rota
Motorista ──1:N── Entrega
```

## Documentação da API

A documentação interativa está disponível em:
- **Swagger UI**: `http://localhost:8000/api/docs/`
- **ReDoc**: `http://localhost:8000/api/docs/redoc/`
- **Schema OpenAPI**: `http://localhost:8000/api/schema/`

### Autenticação

A API utiliza Token Authentication. Para obter um token:

```bash
POST /api/auth/token/
Content-Type: application/json

{
    "username": "seu_usuario",
    "password": "sua_senha"
}
```

Use o token nas requisições subsequentes:
```bash
Authorization: Token <seu_token_aqui>
```

### Endpoints Principais

| Método | Endpoint                              | Descrição                                    | Permissão       |
|--------|---------------------------------------|----------------------------------------------|-----------------|
| POST   | `/api/auth/token/`                   | Obter token de autenticação                  | Público         |
| GET    | `/api/clientes/`                     | Listar clientes                              | Gestor          |
| POST   | `/api/clientes/`                     | Criar novo cliente                           | Gestor          |
| GET    | `/api/clientes/{id}/`                | Detalhes do cliente                          | Gestor/Cliente  |
| GET    | `/api/motoristas/`                   | Listar motoristas                            | Gestor          |
| POST   | `/api/motoristas/`                   | Criar novo motorista                         | Gestor          |
| GET    | `/api/motoristas/{id}/`              | Detalhes do motorista                        | Gestor/Motorista|
| GET    | `/api/motoristas/{id}/entregas/`     | Entregas do motorista                        | Motorista       |
| GET    | `/api/motoristas/{id}/rotas/`        | Rotas do motorista                           | Motorista       |
| POST   | `/api/motoristas/{id}/atribuir-veiculo/` | Atribuir veículo ao motorista           | Gestor          |
| GET    | `/api/veiculos/`                     | Listar veículos                              | Gestor/Motorista|
| POST   | `/api/veiculos/`                     | Criar novo veículo                           | Gestor          |
| GET    | `/api/veiculos/{id}/`                | Detalhes do veículo                          | Gestor/Motorista|
| GET    | `/api/rotas/`                        | Listar rotas                                 | Gestor/Motorista|
| POST   | `/api/rotas/`                        | Criar nova rota                              | Gestor          |
| GET    | `/api/rotas/{id}/`                   | Detalhes da rota                             | Gestor/Motorista|
| POST   | `/api/rotas/{id}/iniciar/`           | Iniciar rota                                 | Motorista       |
| POST   | `/api/rotas/{id}/finalizar/`         | Finalizar rota                               | Motorista       |
| GET    | `/api/entregas/`                     | Listar entregas                              | Depende do perfil|
| POST   | `/api/entregas/`                     | Criar nova entrega                           | Gestor          |
| GET    | `/api/entregas/{id}/`                | Detalhes da entrega                          | Depende do perfil|
| GET    | `/api/entregas/rastrear/{codigo}/`   | Rastrear entrega por código                  | Cliente         |

### Perfis de Permissão

- **Gestor (is_staff)**: Acesso total ao sistema, pode gerenciar todos os recursos
- **Motorista**: Pode visualizar suas rotas, entregas e atualizar status
- **Cliente**: Pode visualizar e criar suas próprias entregas, rastrear status

> **Detalhes:** Consulte a interface Swagger para schemas detalhados de request/response, parâmetros e exemplos de uso.

## Configuração do Ambiente

### Pré-requisitos

- Python 3.12 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/usuario/gestao-logistica-api.git
   cd gestao-logistica-api
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Linux/Mac
   .venv\Scripts\activate         # Windows
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute as migrações do banco de dados:**
   ```bash
   python manage.py migrate
   ```

5. **Crie um superusuário (Gestor):**
   ```bash
   python manage.py createsuperuser
   ```

6. **(Opcional) Popular o banco com dados de teste:**
   ```bash
   python manage.py popular_banco
   ```

7. **Inicie o servidor de desenvolvimento:**
   ```bash
   python manage.py runserver
   ```

8. **Acesse a aplicação:**
   - API: `http://localhost:8000/api/`
   - Admin: `http://localhost:8000/admin/`
   - Documentação Swagger: `http://localhost:8000/api/docs/`
   - Documentação ReDoc: `http://localhost:8000/api/docs/redoc/`




