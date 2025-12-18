# permissions.py

## Visão geral

Este projeto usa permissões personalizadas do **Django REST Framework (DRF)** para implementar o controle de acesso descrito no enunciado.

Há 3 classes principais:

- `IsGestor`: gestor (admin/staff) com acesso total.
- `IsMotorista`: motorista autenticado, com acesso restrito (principalmente aos próprios dados e recursos vinculados a ele).
- `IsCliente`: cliente autenticado, com acesso somente leitura aos próprios dados e entregas.

Essas permissões são combinadas em várias views usando o operador `|` (OR), por exemplo:

- `permission_classes = [IsGestor | IsMotorista]`
- `permission_classes = [IsGestor | IsCliente]`

Na prática:

- `has_permission()` controla **o acesso ao endpoint** (antes de buscar o objeto).
- `has_object_permission()` controla **o acesso ao objeto específico** (depois de carregar o registro do banco).

---

## Imports usados

```py
from rest_framework import permissions
```

- `permissions.BasePermission`: base para criar permissões customizadas.
- `permissions.SAFE_METHODS`: conjunto de métodos que não alteram estado (`GET`, `HEAD`, `OPTIONS`).

---

## Permissão: `IsGestor`

### Trecho do código

```py
class IsGestor(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.is_staff
        )
```

### Explicação

- Exige que o usuário esteja autenticado (`is_authenticated`).
- Exige que o usuário seja **staff** (`is_staff=True`).
  - No projeto, isso representa o perfil de **Gestor/Administrador**.

**Efeito prático**:

- Se a view usar apenas `IsGestor`, então clientes e motoristas recebem `403 Forbidden`.

---

## Permissão: `IsMotorista`

### Objetivo

Permitir que motoristas:

- Consultem seus dados e recursos associados (rotas, entregas da própria rota, etc.).
- Alterem apenas o que for permitido pelas views/serializers (a permissão controla “pode acessar”, e o serializer controla “o que pode alterar”).

### Regras em `has_permission()`

```py
class IsMotorista(permissions.BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        if request.user.is_staff:
            return True

        if not hasattr(request.user, "motorista"):
            return False

        if request.method in ["POST", "DELETE"]:
            return False

        return True
```

### Explicação (endpoint / nível “global”)

- **Autenticação obrigatória**.
- Se o usuário for gestor (`is_staff=True`), passa (gestor pode tudo).
- Se o usuário não tiver perfil `motorista` (`user.motorista`), não passa.
- Se o método for `POST` ou `DELETE`, não passa.
  - Ou seja: motorista não cria nem apaga recursos por padrão.

**Resumo (no nível do endpoint)**:

- Motorista pode: `GET`, `PUT`, `PATCH`, `HEAD`, `OPTIONS`.
- Motorista não pode: `POST`, `DELETE`.

> Observação importante: permitir `PUT/PATCH` aqui não significa que qualquer campo pode ser alterado.
> Quem define o que realmente é editável é o serializer e/ou a lógica da view.

### Regras em `has_object_permission()`

```py
def has_object_permission(self, request, view, obj):
    if request.user.is_staff:
        return True

    motorista = request.user.motorista

    if obj == motorista:
        return True

    if getattr(obj, "motorista", None) == motorista:
        return True

    rota = getattr(obj, "rota", None)
    if rota and getattr(rota, "motorista", None) == motorista:
        return True

    return False
```

### Explicação (objeto / nível “por registro”)

Para um motorista (não staff), o acesso ao **objeto** é permitido se:

1. O objeto é o próprio motorista (`obj == request.user.motorista`)
   - Ex.: acessar `Motorista` do próprio perfil.

2. O objeto tem um atributo `motorista` igual ao motorista autenticado
   - Ex.: `Entrega.motorista == request.user.motorista`.

3. O objeto tem uma `rota` cujo `motorista` é o motorista autenticado
   - Ex.: acessar uma entrega que está em uma rota do motorista.

Se nenhuma das condições for verdadeira, retorna `False` → `403 Forbidden`.

**Exemplos práticos**:

- Motorista acessando `/api/motoristas/{id}/`:
  - Se `{id}` for o dele → permitido.
  - Se `{id}` for de outro motorista → negado.

- Motorista acessando `/api/entregas/{codigo}/`:
  - Se a entrega for dele (diretamente em `entrega.motorista`) → permitido.
  - Se a entrega estiver na rota dele (`entrega.rota.motorista`) → permitido.
  - Se for de outro motorista → negado.

---

## Permissão: `IsCliente`

### Objetivo

Permitir que clientes:

- Tenham acesso **somente leitura**.
- Vejam apenas seus próprios dados e suas entregas.

### Regras em `has_permission()`

```py
class IsCliente(permissions.BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        if request.user.is_staff:
            return True

        if not hasattr(request.user, "cliente"):
            return False

        if request.method not in permissions.SAFE_METHODS:
            return False

        return True
```

### Explicação (endpoint / nível “global”)

- Autenticação obrigatória.
- Gestor passa (gestor pode tudo).
- Usuário precisa ter perfil `cliente` (`user.cliente`).
- Só passa se o método for seguro (`GET`, `HEAD`, `OPTIONS`).
  - Portanto cliente não consegue `POST`, `PUT`, `PATCH`, `DELETE`.

### Regras em `has_object_permission()`

```py
def has_object_permission(self, request, view, obj):
    if request.user.is_staff:
        return True

    if hasattr(obj, "cliente") and obj.cliente == request.user.cliente:
        return True

    if obj == request.user.cliente:
        return True

    return False
```

### Explicação (objeto / nível “por registro”)

Cliente (não staff) acessa o **objeto** se:

- O objeto tem atributo `cliente` e ele é o cliente autenticado
  - Ex.: `Entrega.cliente == request.user.cliente`.
- OU o próprio objeto é o perfil do cliente
  - Ex.: o registro `Cliente` do próprio usuário.

Caso contrário, `403 Forbidden`.

---

## Como essas permissões aparecem nas views

Em geral, o padrão do projeto é:

- **Gestor**: consegue tudo.
- **Motorista**: enxerga e opera somente no que for dele.
- **Cliente**: apenas leitura, somente do que for dele.

Exemplos típicos:

- `ClienteViewSet`: `IsGestor | IsCliente`
  - Gestor vê todos os clientes.
  - Cliente vê apenas o próprio perfil.

- `MotoristaViewSet`: `IsGestor | IsMotorista`
  - List/create/destroy normalmente ficam só para gestor.
  - Retrieve/update podem ser liberados para o próprio motorista via `has_object_permission()`.

- `EntregaViewSet`: `IsGestor | IsMotorista | IsCliente`
  - O queryset é filtrado por perfil.
  - A permissão por objeto impede acesso cruzado.

---

## Observação importante (permissão x serializer)

Permissão responde: **“pode acessar este endpoint/objeto?”**

Serializer/view responde: **“quais campos e quais ações são permitidas?”**

Por isso é comum:

- Permitir `PATCH` para motorista (por permissão),
- mas restringir os campos editáveis (por serializer) a `status` e `observacoes`.
