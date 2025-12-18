# views.py

## Visão geral

- O arquivo define **ViewSets** (DRF) baseados em `ModelViewSet`.
- Regras principais:
  - **Gestor** (staff) costuma ter acesso total.
  - **Cliente** costuma ver apenas seus próprios dados.
  - **Motorista** costuma ver apenas o que está associado ao seu perfil.
- Existem endpoints extras via `@action` (ex.: rotas do motorista, veículos disponíveis, dashboard da rota).

---

## Imports usados

```py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from .models import Cliente, Motorista, Veiculo, Rota, Entrega
from .serializers import (
    ClienteSerializer,
    MotoristaSerializer,
    RotaSerializer,
    EntregaSerializer,
    VeiculoSerializer,
    EntregaClienteSerializer,
)
from .permissions import IsGestor, IsMotorista, IsCliente
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import ValidationError
from django.utils import timezone
```

- `ModelViewSet`: fornece CRUD padrão (list/retrieve/create/update/destroy).
- `Response`: resposta HTTP em JSON.
- `action`: cria rotas adicionais em ViewSets.
- `get_object_or_404`: utilitário para buscar objeto ou retornar 404.
- `extend_schema`: anotações para documentação OpenAPI (drf-spectacular).
- `ValidationError`: erro de validação retornado como 400.

---

## ViewSet: `ClienteViewSet`

### Trecho do código

```py
class ClienteViewSet(viewsets.ModelViewSet):
    serializer_class = ClienteSerializer
    permission_classes = [IsGestor | IsCliente]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Cliente.objects.all()
        if hasattr(user, "cliente"):
            return Cliente.objects.filter(id=user.cliente.id)
        return Cliente.objects.none()
```

### Explicação

- `permission_classes = [IsGestor | IsCliente]`:
  - Permite acesso se o usuário for gestor **ou** cliente.
- `get_queryset()` restringe a listagem:
  - Gestor (`is_staff=True`) vê todos.
  - Cliente vê apenas o próprio registro (`user.cliente`).
  - Outros perfis recebem queryset vazio.

---

## ViewSet: `MotoristaViewSet`

### Trecho do código (permissões e ações)

```py
class MotoristaViewSet(viewsets.ModelViewSet):
    queryset = Motorista.objects.all()
    serializer_class = MotoristaSerializer
    permission_classes = [IsGestor | IsMotorista]

    def get_permissions(self):
        if self.action in ["list", "create", "destroy"]:
            return [IsGestor()]
        return super().get_permissions()

    @action(detail=True, methods=["get"], permission_classes=[IsMotorista])
    def entregas(self, request, pk=None):
        motorista = self.get_object()
        entregas = Entrega.objects.filter(motorista=motorista)
        serializer = EntregaSerializer(entregas, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"], permission_classes=[IsMotorista])
    def rotas(self, request, pk=None):
        motorista = self.get_object()
        rotas = Rota.objects.filter(motorista=motorista)
        serializer = RotaSerializer(rotas, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="atribuir-veiculo", permission_classes=[IsGestor])
    def atribuir_veiculo(self, request, pk=None):
        ...
```

### Explicação

- `get_permissions()` faz regra por ação:
  - `list`, `create`, `destroy`: somente gestor.
  - Demais ações (`retrieve`, `update`, etc.): aplica `permission_classes` padrão.
- `@action detail=True` cria endpoints por motorista (usa `pk` do motorista):
  - `GET /api/motoristas/{id}/entregas/`: lista entregas do motorista.
  - `GET /api/motoristas/{id}/rotas/`: lista rotas do motorista.
- `atribuir_veiculo`:
  - Endpoint: `POST /api/motoristas/{id}/atribuir-veiculo/`.
  - Corpo esperado: `{ "veiculo": <id> }`.
  - Busca veículo por `id` e vincula `veiculo.motorista = motorista`.
  - Retorna 400 se `veiculo` não vier no payload.

---

## ViewSet: `VeiculoViewSet`

### Trecho do código

```py
class VeiculoViewSet(viewsets.ModelViewSet):
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer
    permission_classes = [IsGestor]

    @action(detail=False)
    def disponiveis(self, request):
        disponiveis = Veiculo.objects.filter(status="DISPONIVEL")
        serializer = self.get_serializer(disponiveis, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def rotas(self, request, pk=None):
        veiculo = self.get_object()
        serializer = RotaSerializer(veiculo.rotas.all(), many=True)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        if instance.rotas.filter(status="EM_ANDAMENTO").exists():
            raise ValidationError(
                "Não é possível excluir este veículo pois ele está vinculado a uma rota em andamento."
            )
        super().perform_destroy(instance)
```

### Explicação

- Apenas `IsGestor`: CRUD da frota fica restrito.
- `disponiveis`:
  - Endpoint: `GET /api/veiculos/disponiveis/`.
  - Filtra por `status="DISPONIVEL"`.
- `rotas`:
  - Endpoint: `GET /api/veiculos/{id}/rotas/`.
  - Retorna histórico de rotas do veículo via `veiculo.rotas`.
- `perform_destroy`:
  - Bloqueia exclusão se houver rota com `status="EM_ANDAMENTO"`.
  - Lança `ValidationError` (resposta 400).

---

## ViewSet: `RotaViewSet`

### Trecho do código

```py
class RotaViewSet(viewsets.ModelViewSet):
    serializer_class = RotaSerializer
    permission_classes = [IsGestor | IsMotorista]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Rota.objects.all()

        if hasattr(user, "motorista"):
            return Rota.objects.filter(motorista=user.motorista)

        return Rota.objects.none()

    @action(detail=True, methods=["get"])
    def dashboard(self, request, pk=None):
        rota = self.get_object()
        entregas = rota.entregas.all()
        ...
        return Response(data)
```

### Explicação

- Queryset:
  - Gestor vê todas as rotas.
  - Motorista vê apenas rotas vinculadas ao seu perfil.
- `dashboard`:
  - Endpoint: `GET /api/rotas/{id}/dashboard/`.
  - Retorna uma “visão consolidada” com:
    - dados da rota
    - motorista
    - veículo
    - progresso (total/concluídas/pendentes)
    - lista resumida de entregas (código/endereço/status)

---

## ViewSet: `EntregaViewSet`

### Trecho do código (lookup e serializer dinâmico)

```py
class EntregaViewSet(viewsets.ModelViewSet):
    queryset = Entrega.objects.all()
    serializer_class = EntregaSerializer
    permission_classes = [IsGestor | IsMotorista | IsCliente]

    lookup_field = 'codigo_rastreio'

    def get_serializer_class(self):
        if hasattr(self.request.user, "cliente") and not self.request.user.is_staff:
            return EntregaClienteSerializer
        return EntregaSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Entrega.objects.all()
        if hasattr(user, "motorista"):
            return Entrega.objects.filter(motorista=user.motorista)
        if hasattr(user, "cliente"):
            return Entrega.objects.filter(cliente=user.cliente)
        return Entrega.objects.none()
```

### Explicação

- `lookup_field = 'codigo_rastreio'`:
  - As rotas de detalhe usam o código ao invés do `id`.
  - Ex.: `GET /api/entregas/{codigo_rastreio}/`.
- `get_serializer_class()`:
  - Cliente (não staff) recebe `EntregaClienteSerializer` (visão reduzida).
  - Outros perfis recebem `EntregaSerializer` (completo).
- `get_queryset()`:
  - Gestor vê tudo.
  - Motorista vê entregas do próprio motorista.
  - Cliente vê entregas do próprio cliente.

### Trecho do código (validações na criação)

```py
def perform_create(self, serializer):
    if not serializer.validated_data.get("endereco_origem"):
        raise ValidationError({"endereco_origem": "O endereço de origem é obrigatório."})
    if not serializer.validated_data.get("endereco_destino"):
        raise ValidationError({"endereco_destino": "O endereço de destino é obrigatório."})
    if not serializer.validated_data.get("cliente"):
        raise ValidationError({"cliente": "O cliente é obrigatório."})
    serializer.save()
```

### Explicação

- Reforça obrigatoriedade de campos na criação.
- `ValidationError` retorna 400 com o dicionário de erros.

### Ações extras (`@action`)

#### Atribuir motorista

```py
@action(detail=True, methods=["patch"], permission_classes=[IsGestor])
def atribuir_motorista(self, request, codigo_rastreio=None):
    ...
```

- Endpoint: `PATCH /api/entregas/{codigo_rastreio}/atribuir_motorista/`.
- Payload esperado: `{ "motorista_id": <int> }`.

#### Marcar como entregue

```py
@action(detail=True, methods=["patch"], permission_classes=[IsGestor | IsMotorista])
def marcar_entregue(self, request, codigo_rastreio=None):
    ...
    entrega.status = "entregue"
    entrega.data_entrega_real = timezone.now()
    entrega.save()
```

- Endpoint: `PATCH /api/entregas/{codigo_rastreio}/marcar_entregue/`.
- Se não for staff, valida se o motorista da entrega é o mesmo do usuário.

#### Rastreamento

```py
@action(detail=True, methods=["get"])
def rastreamento(self, request, codigo_rastreio=None):
    entrega = self.get_object()
    serializer = self.get_serializer(entrega)
    return Response(serializer.data)
```

- Endpoint: `GET /api/entregas/{codigo_rastreio}/rastreamento/`.
- Retorna os dados serializados conforme o serializer escolhido (reduzido para cliente, completo para outros).
