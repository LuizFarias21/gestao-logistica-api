# serializers.py


## Visão geral

- O projeto usa **Django REST Framework (DRF)**.
- `ModelSerializer` gera automaticamente campos a partir dos models.
- Alguns serializers restringem campos com `read_only_fields`.
- Existe um serializer “reduzido” para a visão do cliente (`EntregaClienteSerializer`).

---

## Imports usados

```py
from rest_framework import serializers
from .models import Cliente, Motorista, Rota, Entrega, Veiculo
```

- `serializers`: módulo do DRF para serialização/validação.
- `.models`: importa os models que serão mapeados.

---

## Serializer: `ClienteSerializer`

### Trecho do serializer

```py
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ["id", "nome", "endereco", "telefone"]
        read_only_fields = ["user"]
```

### Explicação

- `ModelSerializer`: cria automaticamente campos do model.
- `fields`: expõe somente `id`, `nome`, `endereco`, `telefone`.
- `read_only_fields = ["user"]`:
  - Intenção: impedir que o cliente set/alter o vínculo com `User` via API.
  - Observação: `user` não está listado em `fields`; então ele **não aparece** no payload mesmo assim.

---

## Serializer: `MotoristaSerializer`

### Trecho do serializer

```py
class MotoristaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motorista
        fields = ["id", "nome", "cpf", "cnh", "telefone", "status"]
```

### Explicação

- Expõe os campos básicos de cadastro e o `status`.
- Não expõe `user` nem `data_cadastro` (logo, não aparecem na API por este serializer).

---

## Serializer: `VeiculoSerializer`

### Trecho do serializer

```py
class VeiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veiculo
        fields = "__all__"
```

### Explicação

- `fields = "__all__"`: expõe todos os campos do model `Veiculo`.
- Isso inclui campos como `motorista` (se existir no model) e campos numéricos.

---

## Serializer: `EntregaSerializer`

### Trecho do serializer

```py
class EntregaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrega
        fields = "__all__"
        read_only_fields = ["data_solicitacao"]
```

### Explicação

- Expõe todos os campos do model `Entrega`.
- `data_solicitacao` é somente leitura:
  - Faz sentido porque no model ela é `auto_now_add=True`.
  - Ajuda a evitar tentativas de “forçar” a data via API.

---

## Serializer: `RotaSerializer`

### Trecho do serializer

```py
class RotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rota
        fields = "__all__"
        read_only_fields = ["data_rota"]
```

### Explicação

- Expõe todos os campos do model `Rota`.
- `data_rota` é somente leitura:
  - Faz sentido porque no model ela é `auto_now_add=True`.

---

## Serializer: `EntregaClienteSerializer` (visão restrita)

### Trecho do serializer

```py
class EntregaClienteSerializer(serializers.ModelSerializer):
    """
    Serializer restrito para visão do Cliente.
    Mostra apenas identificação, status e previsão.
    """
    class Meta:
        model = Entrega
        fields = ["codigo_rastreio", "status", "data_entrega_prevista"]
```

### Explicação

- Objetivo: quando o usuário é um cliente (e não staff), retornar **apenas**:
  - `codigo_rastreio`: identificação
  - `status`: estado atual
  - `data_entrega_prevista`: previsão
- Esse serializer é selecionado dinamicamente no `EntregaViewSet.get_serializer_class()` (ver documentação de `views.py`).
