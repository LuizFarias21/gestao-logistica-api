# settings.py


## Visão geral

- Projeto Django (Django 5.2.x).
- API baseada em Django REST Framework (DRF) com autenticação por **Token**.
- Documentação OpenAPI via **drf-spectacular**.
- Banco de dados local: **SQLite** (`db.sqlite3`).

---

## Base do projeto (`BASE_DIR`)

### Trecho do código

```py
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
```

### Explicação

- `BASE_DIR` aponta para a raiz do projeto.
- É usado para construir paths (ex.: banco `db.sqlite3`).

---

## Segurança e ambiente (DEV)

### Trecho do código

```py
SECRET_KEY = "django-insecure-th(suvk^8e8boq1i#&%!_x1ix_dw&&bk%yd&0z)j9echmkhd$5"
DEBUG = True
ALLOWED_HOSTS = []
```

### Explicação

- `SECRET_KEY`: chave criptográfica do Django.
- `DEBUG = True`: habilita modo de desenvolvimento.
- `ALLOWED_HOSTS`: vazio → em produção precisaria listar domínios/hosts permitidos.

---

## Apps instalados

### Trecho do código

```py
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
    "rest_framework",
    "rest_framework.authtoken",
    "django_filters",
    "drf_spectacular",
]
```

### Explicação

- `core`: app com models/viewsets/serializers da solução.
- `rest_framework`: habilita DRF.
- `rest_framework.authtoken`: habilita tokens via `TokenAuthentication` e endpoint `obtain_auth_token`.
- `django_filters`: suporte a filtros (se usado em views/viewsets).
- `drf_spectacular`: gera schema OpenAPI e UIs (Swagger/Redoc).

---

## Configuração do DRF

### Trecho do código

```py
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}
```

### Explicação

- **Autenticação**:
  - `TokenAuthentication`: API stateless via token.
  - `SessionAuthentication`: útil em browser/admin ou testes com sessão.
- **Permissão padrão**: `IsAuthenticated`.
  - Ou seja: por padrão, endpoints exigem login/token.
  - ViewSets podem sobrescrever via `permission_classes`.
- **Schema**: `AutoSchema` do drf-spectacular.

---

## drf-spectacular (OpenAPI)

### Trecho do código

```py
SPECTACULAR_SETTINGS = {
    "TITLE": "API de Gestão Logística",
    "DESCRIPTION": "Documentação da API de Gestão Logística",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}
```

### Explicação

- Define metadados da documentação.
- `SERVE_INCLUDE_SCHEMA = False`: normalmente controla se o schema aparece embutido em certas páginas.

---

## Middleware

### Trecho do código

```py
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
```

### Explicação

- Lista padrão do Django.
- `CsrfViewMiddleware` pode afetar chamadas via sessão (não via token), mas com `TokenAuthentication` normalmente não é um problema.

---

## URLs e templates

### Trecho do código

```py
ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
```

### Explicação

- `ROOT_URLCONF` aponta para o arquivo de rotas raiz.
- Templates são padrão (mais relevante para Admin e páginas HTML, não para API JSON).

---

## WSGI

### Trecho do código

```py
WSGI_APPLICATION = "config.wsgi.application"
```

### Explicação

- Entry-point WSGI para servidores (gunicorn/uwsgi).

---

## Banco de dados

### Trecho do código

```py
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

### Explicação

- Usa SQLite local.
- O arquivo `db.sqlite3` fica na raiz do projeto.

---

## Internacionalização

### Trecho do código

```py
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
```

### Explicação

- Linguagem padrão: inglês dos EUA.
- Fuso: UTC.
- `USE_TZ=True`: datas/horas em timezone-aware.

---

## Arquivos estáticos

### Trecho do código

```py
STATIC_URL = "static/"
```

### Explicação

- Configuração básica de estáticos (admin).

---

## Chave primária padrão

### Trecho do código

```py
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
```

### Explicação

- IDs usam `BigAutoField` por padrão (inteiro grande).
