
# API Projeto Django

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg?logo=python)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-5.0%2B-green.svg?logo=Django)](https://www.djangoproject.com/)
[![SQLite](https://img.shields.io/badge/SQLite-003B57.svg?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
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
- [Deploy](#deploy)

## Visão Geral

Forneça uma descrição concisa do propósito da API, seus objetivos principais e o problema que resolve. Inclua informações sobre o domínio de aplicação, público-alvo e funcionalidades de alto nível.

## Pacotes Utilizados

Liste todos os pacotes Python necessários, com versões recomendadas. Utilize um formato de tabela para maior clareza.

| Pacote                  | Versão       | Descrição                                      |
|-------------------------|--------------|------------------------------------------------|
| Django                  | >=5.0        | Framework web principal                        |
| djangorestframework     | latest       | Toolkit para construção de APIs REST           |
| psycopg2-binary         | latest       | Adaptador PostgreSQL                           |
| django-environ          | latest       | Gerenciamento de variáveis de ambiente         |
| drf-yasg                | latest       | Geração automática de documentação Swagger     |
| ...                     | ...          | ...                                            |

> **Nota:** Consulte o arquivo `requirements.txt` para a lista completa e versões exatas.

## Estrutura do Projeto

Apresente a organização dos diretórios e arquivos principais. Utilize uma árvore de diretórios para visualização clara.

```
projeto_api/
├── manage.py
├── requirements.txt
├── .env.example
├── projeto/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── core/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   └── urls.py
│   └── ...
├── docs/
│   └── database_diagram.png
└── scripts/
    └── deploy.sh
```

Descreva brevemente o propósito de cada diretório e módulo relevante.

## Diagrama de Banco de Dados

![Diagrama de Banco de Dados](./docs/database_diagram.png)

> **Descrição:** Inclua um diagrama ER (Entidade-Relacionamento) gerado por ferramentas como `django-extensions` ou `pygraphviz`. Descreva as principais entidades, relacionamentos e campos críticos.

## Documentação da API

A documentação interativa está disponível em `/api/docs/` (Swagger UI) ou `/api/redoc/` (ReDoc) no ambiente de desenvolvimento.

### Endpoints Principais

| Método | Endpoint              | Descrição                          | Autenticação |
|--------|-----------------------|------------------------------------|--------------|
| GET    | `/api/items/`         | Lista todos os itens               | Opcional     |
| POST   | `/api/items/`         | Cria um novo item                  | Requerida    |
| GET    | `/api/items/{id}/`    | Recupera um item específico        | Opcional     |
| ...    | ...                   | ...                                | ...          |

> **Detalhes:** Consulte a interface Swagger para schemas de request/response, parâmetros e exemplos.

## Configuração do Ambiente

Siga os passos abaixo para configurar o ambiente local.

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/usuario/projeto_api.git
   cd projeto_api
   ```

2. **Crie um ambiente virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente:**
   ```bash
   cp .env.example .env
   # Edite .env com suas credenciais
   ```

5. **Aplique as migrações e inicie o servidor:**
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

## Deploy(opcional)

### Plataforma Recomendada: [Render / Railway / AWS]

1. **Prepare o `Procfile`:**
   ```
   web: gunicorn projeto.wsgi:application --log-file -
   ```

2. **Configure variáveis de ambiente** na plataforma de deploy.

3. **Execute migrações em produção:**
   ```bash
   python manage.py migrate
   ```

4. **Colete arquivos estáticos (se aplicável):**
   ```bash
   python manage.py collectstatic
   ```

> **CI/CD:** Integração com GitHub Actions disponível em `.github/workflows/deploy.yml`.


