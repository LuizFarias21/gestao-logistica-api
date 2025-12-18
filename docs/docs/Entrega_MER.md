# 📦 Entidade: Entrega

## 📝 Descrição
A entidade **Entrega** é o núcleo da operação logística no sistema. Ela representa o objeto de serviço contratado pelo cliente, contendo as informações de **origem**, **destino**, **volumetria/capacidade** e o **rastreamento do ciclo de vida do transporte**, desde a solicitação inicial até a finalização do serviço.

---

## 📊 Tabela de Campos

| Campo                   | Tipo                    | Descrição                                                                 |
|------------------------|-------------------------|---------------------------------------------------------------------------|
| `id`                   | PK (UUID / Int)         | Identificador único da entrega.                                           |
| `codigo_rastreio`      | String (Unique)         | Código único para consulta e rastreamento da entrega.                     |
| `cliente_id`           | FK (Cliente)            | Referência ao cliente que solicitou o serviço.                            |
| `rota_id`              | FK (Rota) *(nullable)*  | Referência à rota vinculada.                                              |
| `motorista_id`         | FK (Motorista) *(nullable)* | Referência ao motorista responsável pela entrega.                     |
| `endereco_origem`      | String / Address        | Endereço completo de coleta da carga.                                     |
| `endereco_destino`     | String / Address        | Endereço completo de entrega final.                                       |
| `status`               | Enum                    | `pendente`, `em_trânsito`, `entregue`, `cancelada`.                       |
| `capacidade_necessaria`| Decimal / Int           | Peso ou volume necessário (obrigatório para cálculo de rota).             |
| `valor_frete`          | Decimal                 | Valor cobrado pelo serviço de transporte.                                 |
| `data_solicitacao`     | DateTime                | Data e hora em que o pedido foi criado.                                   |
| `data_entrega_prevista`| DateTime                | Prazo estimado para a conclusão da entrega.                               |
| `data_entrega_real`    | DateTime *(nullable)*   | Data e hora exata da conclusão da entrega.                                |
| `observacoes`          | Text                    | Notas adicionais e instruções especiais.                                  |

---

## 🔗 Relacionamentos

- **N : 1 — Cliente**  
  Uma entrega pertence a um único cliente.

- **N : 1 — Rota**  
  Uma entrega pode ser agrupada em uma rota (opcional no início).

- **N : 1 — Motorista**  
  Uma entrega pode ter um motorista atribuído.

---

## ⚙️ Funcionalidades e Endpoints (API)

### CRUD Básico

- `GET /api/entregas/`  
  Lista entregas  
  - Gestor: vê todas  
  - Cliente: vê apenas as suas  

- `POST /api/entregas/`  
  Cria uma nova solicitação de entrega.

- `GET /api/entregas/{id}/`  
  Retorna os detalhes de uma entrega específica.

- `PUT / PATCH /api/entregas/{id}/`  
  Atualiza dados da entrega (ex: endereço, correções).

- `DELETE /api/entregas/{id}/`  
  Cancela ou remove uma entrega.

---

### Rotas Específicas

- `PATCH /api/entregas/{id}/atribuir-motorista/`  
  Vincula manualmente uma entrega a um motorista.

- `GET /api/entregas/{id}/rastreamento/`  
  Visualização pública ou autenticada do status e da previsão de entrega.

- `PATCH /api/entregas/{id}/status/`  
  Permite que o motorista atualize o status da entrega (ex: para **entregue**).

---

## ⚠️ Regras de Negócio Importantes

### 🔄 Fluxo de Status
- A entrega inicia como **pendente**.  
- Ao ser associada a uma rota ativa, muda para **em_trânsito**.  
- Ao finalizar, muda para **entregue** ou **cancelada**.

### 📦 Capacidade Obrigatória
- O campo `capacidade_necessaria` é **obrigatório** para permitir o cálculo de lotação do veículo.

### ⏱️ Fechamento Automático
- Quando o motorista marca a entrega como **entregue**, o campo `data_entrega_real` deve ser preenchido automaticamente com o horário do sistema.

### 🔐 Permissões de Visibilidade
- **Gestor**: acesso total (CRUD).  
- **Motorista**: visualiza apenas entregas atribuídas a ele e pode atualizar o status.  
- **Cliente**: acesso somente leitura às suas próprias entregas (via ID ou código de rastreio).

### 🧩 Integridade de Dados
- O sistema deve impedir a criação de entregas **sem endereço válido** ou **sem cliente vinculado**.

---

