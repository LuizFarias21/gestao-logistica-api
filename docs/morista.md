
# 🚚 Entidade: Motorista (B) - Modelagem Django

Esta tabela detalha os campos, tipos e definições da classe `Motorista` conforme implementada no `models.py`.

| Campo | Tipo Django | Descrição | Restrições/Detalhes |
| :--- | :--- | :--- | :--- |
| `id` | `models.Model` (PK) | Chave Primária. | Gerado automaticamente. |
| `nome` | `CharField` | Nome completo do motorista. | [cite_start]`max_length=100`[cite: 135]. |
| `cpf` | `CharField` | Cadastro de Pessoa Física. | `max_length=11`, **`unique=True`**. |
| `cnh` | `CharField` | Número da CNH. | `max_length=9`, **`unique=True`**. |
| `telefone` | `CharField` | Telefone de contato. | `max_length=15`. |
| `status` | `CharField` | Estado operacional do motorista. | [cite_start]`max_length=10`, **`choices`** (disponível, em_rota, ativo, inativo)[cite: 139]. |
| `data_cadastro`| `DateTimeField` | Data de registro no sistema. | `auto_now_add=True`, `editable=False`. |

---

## 🔗 Relacionamentos (Conforme Requisitos do Projeto)

[cite_start]A classe `Motorista` é um ponto central de relacionamento[cite: 141].

| Relacionamento | Tipo | Entidade Relacionada | Local da Chave (FK) |
| :--- | :--- | :--- | :--- |
| **Realiza** | [cite_start]1:N [cite: 142] | [cite_start]Entrega (A) [cite: 142] | [cite_start]Entidade `Entrega` (campo `motorista_id`)[cite: 43]. |
| **Possui** | [cite_start]1:N [cite: 143] | [cite_start]Rota (C) [cite: 143] | [cite_start]Entidade `Rota` (campo `motorista_id`)[cite: 46, 150]. |
| **Dirige** | [cite_start]1:1 [cite: 144] | [cite_start]Veículo (D) [cite: 144] | [cite_start]Pode ser no `Motorista` (como `OneToOneField`) ou no `Veículo`[cite: 40]. |

## ⚙️ Opções de Status (`STATUS_CHOICES`)

O campo `status` utiliza as seguintes opções definidas no modelo:

* `'disponivel'`
* `'em_rota'`
* `'ativo'`
* `'inativo'`

***

Gostaria de ver o código Django para a classe `Veiculo` ou `Entrega`, incluindo a chave estrangeira (`ForeignKey`) para `Motorista`?