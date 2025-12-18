# models.py

---

## Visão geral (mapa de relacionamentos)

- `User` (Django) ⇄ `Cliente`: **1:1** (um usuário pode ter um perfil de cliente)
- `User` (Django) ⇄ `Motorista`: **1:1** (um usuário pode ter um perfil de motorista)
- `Motorista` ⇄ `Veiculo`: **1:1 opcional** (veículo pode existir sem motorista)
- `Motorista` → `Rota`: **N:1** (um motorista pode ter várias rotas)
- `Veiculo` → `Rota`: **N:1** (um veículo pode ter várias rotas)
- `Cliente` → `Entrega`: **N:1** (um cliente pode ter várias entregas)
- `Rota` → `Entrega`: **N:1 opcional** (entrega pode existir sem estar alocada em rota)
- `Motorista` → `Entrega`: **N:1 opcional** (entrega pode existir sem motorista associado)

### Notas rápidas (Django)

- `null=True` afeta o **banco** (coluna pode ser `NULL`).
- `blank=True` afeta **validação** (admin/forms podem aceitar vazio).
- `unique=True` cria uma restrição de unicidade no banco.
- `choices=...` limita os valores permitidos e melhora a exibição no admin.
- `auto_now_add=True` grava o timestamp apenas **na criação** do registro.

---

## Imports usados

```py
from django.db import models
from django.contrib.auth.models import User
```

- `models`: base para definir tabelas/colunas via ORM.
- `User`: modelo padrão do Django para autenticação/login.

---

## Model: `Cliente`

### Trecho do model

```py
class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cliente")

    nome = models.CharField(max_length=120, help_text="Nome completo ou Razão Social")

    endereco = models.CharField(max_length=255, help_text="Endereço principal")

    telefone = models.CharField(max_length=20, help_text="Telefone para contato")

    def __str__(self):
        return f"{self.nome} ({self.user.username})"
```

### Explicação

- `class Cliente(models.Model)`: cria uma tabela para armazenar clientes.
- `user = OneToOneField(User, ...)`:
  - Relação **1 para 1** com `User`.
  - `on_delete=models.CASCADE`: apagar o usuário apaga o perfil de cliente.
  - `related_name="cliente"`: permite `user.cliente`.
- `nome/endereco/telefone`: campos de texto básicos do cadastro.
- `__str__`: texto de exibição no Django Admin.

---

## Model: `Motorista`

### Trecho do model

```py
class Motorista(models.Model):
    STATUS_CHOICES = (
        ("disponivel", "Disponível"),
        ("em_rota", "Em Rota"),
        ("inativo", "Inativo"),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="motorista",
        help_text="Usuário de login associado a este perfil de cliente",
    )

    nome = models.CharField(max_length=100, help_text="Nome do motorista")

    cpf = models.CharField(max_length=11, unique=True, help_text="CPF sem ponto ou traço")

    cnh = models.CharField(max_length=11, unique=True, help_text="CNH sem ponto ou traço")

    telefone = models.CharField(max_length=20, help_text="Telefone Ex: (61) 91234-5678")

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="disponivel",
        help_text="Status do motorista",
    )

    data_cadastro = models.DateTimeField(
        auto_now_add=True, help_text="Data e hora do cadastro do motorista"
    )

    def __str__(self):
        return self.nome
```

### Explicação

- `STATUS_CHOICES`: define os estados possíveis do motorista (ajuda validação + UI).
- `user`: perfil 1:1 com `User`.
  - Observação: o `help_text` diz “perfil de cliente”; aqui parece ser “perfil de motorista”.
- `cpf` e `cnh`:
  - `unique=True` garante que não existam duplicados.
  - `max_length=11` sugere armazenamento apenas com dígitos.
- `status`: usa `choices` + `default="disponivel"`.
- `data_cadastro`: timestamp automático de criação.

---

## Model: `Veiculo`

### Trecho do model

```py
class Veiculo(models.Model):
    TIPO_VEICULOS = (
        ("CARRO", "Carro"),
        ("VAN", "Van"),
        ("CAMINHAO", "Caminhão"),
    )

    STATUS_VEICULOS = (
        ("DISPONIVEL", "Disponível"),
        ("EM_USO", "Em uso"),
        ("MANUTENCAO", "Manutenção"),
    )

    placa = models.CharField(max_length=7, unique=True, help_text="Placa sem traços (EX: ABC1234)")

    modelo = models.CharField(max_length=70, help_text="Modelo e Marca (Ex: Fiat Ducato)")

    tipo = models.CharField(
        max_length=20,
        choices=TIPO_VEICULOS,
        default="CARRO",
        help_text="Tipo de veículo",
    )

    capacidade_maxima = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Capacidade em KG (EX: 320.00)"
    )

    km_atual = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Leitura atual do hodômetro em KM",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_VEICULOS,
        default="DISPONIVEL",
        help_text="Status atual do veículo",
    )

    motorista = models.OneToOneField(
        "Motorista",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="veiculo",
        help_text="Motorista responsável pelo veículo no momento",
    )

    def __str__(self):
        return f"{self.modelo} ({self.placa})"
```

### Explicação

- `TIPO_VEICULOS` / `STATUS_VEICULOS`: enums para padronizar valores.
- `placa`:
  - `unique=True` evita duplicidade.
  - `max_length=7` assume padrão sem hífen.
- `capacidade_maxima` / `km_atual`:
  - `DecimalField` evita erros comuns de ponto flutuante.
- `motorista = OneToOneField("Motorista", ...)`:
  - Relação 1:1 **opcional**.
  - `null=True`/`blank=True`: veículo pode estar sem motorista.
  - `on_delete=models.SET_NULL`: se apagar o motorista, o veículo continua e “desassocia”.
  - `related_name="veiculo"`: permite `motorista.veiculo`.

---

## Model: `Rota`

### Trecho do model

```py
class Rota(models.Model):
    STATUS_ROTA = (
        ("planejada", "Planejada"),
        ("em_andamento", "Em Andamento"),
        ("concluida", "Concluída"),
    )

    motorista = models.ForeignKey(
        Motorista, on_delete=models.PROTECT, related_name="rotas"
    )
    veiculo = models.ForeignKey(Veiculo, on_delete=models.PROTECT, related_name="rotas")

    nome = models.CharField(max_length=100)
    descricao = models.TextField(null=True, blank=True)
    data_rota = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20, choices=STATUS_ROTA, default="planejada"
    )

    def __str__(self):
        return f"{self.nome} - {self.motorista.nome}"
```

### Explicação

- `motorista` e `veiculo` são `ForeignKey`:
  - **N:1** (muitas rotas podem apontar para o mesmo motorista/veículo).
  - `on_delete=models.PROTECT`: impede apagar motorista/veículo se houver rotas ligadas.
- `descricao`: opcional.
- `data_rota = auto_now_add=True`: captura quando a rota foi criada.
  - Se a intenção for “data agendada” (planejamento), normalmente seria um campo editável.

---

## Model: `Entrega`

### Trecho do model

```py
class Entrega(models.Model):
    STATUS_CHOICES = (
        ("pendente", "Pendente"),
        ("em_transito", "Em Trânsito"),
        ("entregue", "Entregue"),
        ("cancelada", "Cancelada"),
    )

    codigo_rastreio = models.CharField(
        max_length=50, unique=True, help_text="Código único de rastreamento da entrega"
    )

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name="entregas",
        help_text="Cliente solicitante da entrega",
    )

    rota = models.ForeignKey(
        Rota,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="entregas",
        help_text="Rota associada à entrega",
    )

    motorista = models.ForeignKey(
        Motorista,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="entregas",
        help_text="Motorista responsável pela entrega",
    )

    endereco_origem = models.CharField(
        max_length=255, help_text="Endereço de origem da entrega"
    )

    endereco_destino = models.CharField(
        max_length=255, help_text="Endereço de destino da entrega"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pendente",
        help_text="Status atual da entrega",
    )

    capacidade_necessaria = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Peso ou volume necessário em KG para o transporte",
    )

    valor_frete = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Valor do frete em reais"
    )

    data_solicitacao = models.DateTimeField(
        auto_now_add=True, null=True, help_text="Data e hora da solicitação da entrega"
    )

    data_entrega_prevista = models.DateTimeField(
        null=True, blank=True, help_text="Data e hora prevista para a entrega"
    )

    data_entrega_real = models.DateTimeField(
        null=True, blank=True, help_text="Data e hora real da entrega concluída"
    )

    observacoes = models.TextField(
        blank=True, help_text="Observações adicionais sobre a entrega"
    )

    def __str__(self):
        return f"{self.codigo_rastreio} - {self.status}"
```

### Explicação

- `codigo_rastreio`:
  - `unique=True` torna o código um identificador confiável.
- `cliente = ForeignKey(..., PROTECT)`:
  - Impede apagar clientes com entregas (mantém histórico).
- `rota` e `motorista`:
  - `null=True`/`blank=True`: entrega pode existir antes de alocação.
  - `SET_NULL`: apagar rota/motorista não apaga a entrega.
- `status`: controla o fluxo da entrega.
- `capacidade_necessaria` e `valor_frete`: `DecimalField` para valores exatos.
- `data_solicitacao`:
  - `auto_now_add=True` já preenche na criação; `null=True` tende a ser redundante.
- `data_entrega_prevista` / `data_entrega_real`: datas opcionais.
