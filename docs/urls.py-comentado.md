# urls.py


## Visão geral

- `config/urls.py` é o **roteador raiz** do projeto.
- `core/urls.py` define as rotas da API (`/api/...`) via `DefaultRouter` do DRF.
- O projeto expõe endpoints de autenticação por token, schema OpenAPI e documentação Swagger/Redoc.

---

## Arquivo: `config/urls.py`

### Trecho do código

```py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("core.urls")),
]
```

### Explicação

- `path("admin/", ...)`: rota do Django Admin.
- `path("api/", include("core.urls"))`: tudo que estiver em `core/urls.py` passa a ficar sob o prefixo `/api/`.

---

## Arquivo: `core/urls.py`

### Trecho do código

```py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from .views import MotoristaViewSet, VeiculoViewSet, ClienteViewSet, EntregaViewSet, RotaViewSet

router = DefaultRouter()

router.register(r"motoristas", MotoristaViewSet, basename="motorista")
router.register(r"veiculos", VeiculoViewSet, basename="veiculo")
router.register(r"clientes", ClienteViewSet, basename="cliente")
router.register(r"entregas", EntregaViewSet, basename="entrega")
router.register(r"rotas", RotaViewSet, basename="rota")

urlpatterns = [
    path("auth/token/", obtain_auth_token, name="api_token_auth"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("docs/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("", include(router.urls)),
]
```

### Explicação

- `DefaultRouter()`:
  - Cria automaticamente rotas REST padrão para cada ViewSet registrado.
  - Para cada registro `router.register("xxx", ViewSet)` ele cria:
    - `GET /api/xxx/` (list)
    - `POST /api/xxx/` (create)
    - `GET /api/xxx/{lookup}/` (retrieve)
    - `PUT/PATCH /api/xxx/{lookup}/` (update/partial_update)
    - `DELETE /api/xxx/{lookup}/` (destroy)

### Endpoints especiais (não são do router)

- `POST /api/auth/token/`
  - View do DRF para obter token (`obtain_auth_token`).
- `GET /api/schema/`
  - Schema OpenAPI (drf-spectacular).
- `GET /api/docs/`
  - Swagger UI.
- `GET /api/docs/redoc/`
  - Redoc.

### Endpoints criados pelo router

> Observação: o `lookup` padrão é `id`, exceto em `EntregaViewSet`, que usa `lookup_field = "codigo_rastreio"`.

- `/api/motoristas/`
  - Ações extras em `MotoristaViewSet`:
    - `GET /api/motoristas/{id}/entregas/`
    - `GET /api/motoristas/{id}/rotas/`
    - `POST /api/motoristas/{id}/atribuir-veiculo/`

- `/api/veiculos/`
  - Ações extras em `VeiculoViewSet`:
    - `GET /api/veiculos/disponiveis/`
    - `GET /api/veiculos/{id}/rotas/`

- `/api/clientes/`

- `/api/entregas/`
  - Detalhe por rastreio: `GET /api/entregas/{codigo_rastreio}/`
  - Ações extras em `EntregaViewSet`:
    - `PATCH /api/entregas/{codigo_rastreio}/atribuir_motorista/`
    - `PATCH /api/entregas/{codigo_rastreio}/marcar_entregue/`
    - `GET /api/entregas/{codigo_rastreio}/rastreamento/`

- `/api/rotas/`
  - Ações extras em `RotaViewSet`:
    - `GET /api/rotas/{id}/dashboard/`

    - `POST /api/rotas/{id}/atribuir-entregas/`
      - Atribui uma ou mais entregas à rota com validação de capacidade do veículo.
      - Body: `{ "entregas": ["CODIGO1", "CODIGO2"] }`
