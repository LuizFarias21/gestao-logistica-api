# Modelo Entidade-Relacionamento (MER)

Este documento descreve o Modelo Entidade-Relacionamento (MER) com base nos modelos atuais da aplicação (`core/models.py`).

> Observação: os campos `id`, `created_at`/`updated_at` não existem explicitamente aqui (exceto campos `DateTimeField` já definidos). O `id` (PK) é criado automaticamente pelo Django.

---

## User (Django)

### 1. Descrição

Entidade de autenticação do Django (`django.contrib.auth.models.User`). É utilizada como base de login e controle de acesso. O sistema cria perfis específicos associados ao usuário: `Cliente` e `Motorista`.

### 2. Tabela de Campos

| Nome do Campo | Tipo | Descrição |
|---|---|---|
| id | Integer (PK) | Identificador único do usuário (automático) |
| username | String | Nome de usuário para login |
| password | String | Hash da senha |
| is_staff | Boolean | Indica se o usuário é Gestor (admin) |

> Campos adicionais do `User` existem no Django, mas aqui listamos os essenciais para o funcionamento do sistema.

### 3. Relacionamentos

- 1:1 com `Cliente` (opcional)
- 1:1 com `Motorista` (opcional)

### 4. Regras de Negócio Importantes ⚠️

- Um usuário pode ser **Cliente** ou **Motorista** (ou nenhum), conforme cadastro.
- Usuários com `is_staff = true` são tratados como **Gestores** para permissões.

---

## Cliente

### 1. Descrição

Representa o cliente solicitante de entregas. É um perfil associado a um `User` e armazena informações cadastrais básicas.

### 2. Tabela de Campos

| Nome do Campo | Tipo | Descrição |
|---|---|---|
| id | Integer (PK) | Identificador único do cliente (automático) |
| user | OneToOne(User) | Usuário de autenticação associado ao cliente |
| nome | String (120) | Nome completo ou Razão Social |
| endereco | String (255) | Endereço principal |
| telefone | String (20) | Telefone para contato |

### 3. Relacionamentos

- 1:1 com `User`
- 1:N com `Entrega` (um cliente pode solicitar várias entregas)

### 4. Regras de Negócio Importantes ⚠️

- Um `Cliente` deve estar associado a exatamente um `User`.
- Entregas sempre precisam de um `Cliente` válido.

---

## Motorista

### 1. Descrição

Representa o motorista responsável por executar entregas e cumprir rotas. É um perfil associado a um `User`.

### 2. Tabela de Campos

| Nome do Campo | Tipo | Descrição |
|---|---|---|
| id | Integer (PK) | Identificador único do motorista (automático) |
| user | OneToOne(User) | Usuário de autenticação associado ao motorista |
| nome | String (100) | Nome do motorista |
| cpf | String (11) | CPF sem ponto/traço (único) |
| cnh | String (11) | CNH sem ponto/traço (único) |
| telefone | String (20) | Telefone para contato |
| status | Choice(String) | `disponivel`, `em_rota`, `inativo` |
| data_cadastro | DateTime | Data/hora de cadastro (automático) |

### 3. Relacionamentos

- 1:1 com `User`
- 1:1 com `Veiculo` (opcional) — via `Veiculo.motorista`
- 1:N com `Rota`
- 1:N com `Entrega` (opcional por entrega)

### 4. Regras de Negócio Importantes ⚠️

- `cpf` e `cnh` são únicos.
- Um motorista pode ter **no máximo um veículo** vinculado por vez (relação 1:1).

---

## Veiculo

### 1. Descrição

Representa um veículo da frota, com dados de identificação, tipo e capacidade. Pode ser atribuído a um motorista.

### 2. Tabela de Campos

| Nome do Campo | Tipo | Descrição |
|---|---|---|
| id | Integer (PK) | Identificador único do veículo (automático) |
| placa | String (7) | Placa sem traços (única) |
| modelo | String (70) | Modelo e marca |
| tipo | Choice(String) | `CARRO`, `VAN`, `CAMINHAO` |
| capacidade_maxima | Decimal(10,2) | Capacidade em KG |
| km_atual | Decimal(10,2) | Hodômetro atual (KM) |
| status | Choice(String) | `DISPONIVEL`, `EM_USO`, `MANUTENCAO` |
| motorista | OneToOne(Motorista) | Motorista responsável (opcional) |

### 3. Relacionamentos

- 1:1 com `Motorista` (opcional)
- 1:N com `Rota`

### 4. Regras de Negócio Importantes ⚠️

- `placa` é única.
- Um veículo pode ser vinculado a **no máximo um motorista** por vez.

---

## Rota

### 1. Descrição

Representa uma rota planejada/andamento/concluída que agrupa entregas e é executada por um motorista com um veículo específico.

### 2. Tabela de Campos

| Nome do Campo | Tipo | Descrição |
|---|---|---|
| id | Integer (PK) | Identificador único da rota (automático) |
| motorista | ForeignKey(Motorista) | Motorista responsável (obrigatório) |
| veiculo | ForeignKey(Veiculo) | Veículo utilizado (obrigatório) |
| nome | String (100) | Nome da rota |
| descricao | Text | Descrição (opcional) |
| data_rota | DateTime | Data/hora de criação (automático) |
| status | Choice(String) | `planejada`, `em_andamento`, `concluida` |

### 3. Relacionamentos

- N:1 com `Motorista`
- N:1 com `Veiculo`
- 1:N com `Entrega` (uma rota pode conter várias entregas)

### 4. Regras de Negócio Importantes ⚠️

- Uma `Rota` deve ter `motorista` e `veiculo` válidos (ambos são obrigatórios).
- Entregas podem ser associadas a uma rota (ou não), dependendo do fluxo.

---

## Entrega

### 1. Descrição

Representa uma entrega com rastreio, origem/destino, capacidade necessária, valor do frete e status. Pode estar vinculada a uma rota e a um motorista.

### 2. Tabela de Campos

| Nome do Campo | Tipo | Descrição |
|---|---|---|
| id | Integer (PK) | Identificador único da entrega (automático) |
| codigo_rastreio | String (50) | Código único de rastreamento (único) |
| cliente | ForeignKey(Cliente) | Cliente solicitante (obrigatório) |
| rota | ForeignKey(Rota) | Rota associada (opcional) |
| motorista | ForeignKey(Motorista) | Motorista responsável (opcional) |
| endereco_origem | String (255) | Endereço de origem |
| endereco_destino | String (255) | Endereço de destino |
| status | Choice(String) | `pendente`, `em_transito`, `entregue`, `cancelada` |
| capacidade_necessaria | Decimal(10,2) | Peso/volume necessário (KG) |
| valor_frete | Decimal(10,2) | Valor do frete (R$) |
| data_solicitacao | DateTime | Data/hora da solicitação (automático) |
| data_entrega_prevista | DateTime | Previsão de entrega (opcional) |
| data_entrega_real | DateTime | Data real de entrega (opcional) |
| observacoes | Text | Observações adicionais (opcional) |

### 3. Relacionamentos

- N:1 com `Cliente`
- N:1 com `Rota` (opcional)
- N:1 com `Motorista` (opcional)

### 4. Regras de Negócio Importantes ⚠️

- `codigo_rastreio` é único.
- Toda entrega deve ter `cliente` e endereços de origem/destino.
- Uma entrega pode existir sem rota/motorista até ser planejada/atribuída.

---

## Resumo dos Relacionamentos (MER)

```text
User 1:1 Cliente
User 1:1 Motorista
Motorista 1:1 Veiculo (opcional)
Motorista 1:N Rota
Veiculo 1:N Rota
Cliente 1:N Entrega
Rota 1:N Entrega (opcional por entrega)
Motorista 1:N Entrega (opcional por entrega)
```
