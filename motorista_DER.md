# Motorista_MER.md

## Descrição
A entidade **Motorista (B)** representa o profissional responsável por realizar as entregas da frota. Ele interage com o sistema para consultar rotas atribuídas e atualizar o status das mercadorias em tempo real.

## Tabela de Campos
| Nome do Campo | Tipo (Django) | Descrição |
| :--- | :--- | :--- |
| id | AutoField | Identificador único do motorista (PK). |
| User | OneToOneField | Vínculo com o usuário do Django para login e permissões (related_name="motorista"). |
| nome | CharField | Nome completo do motorista. |
| cpf | CharField | Cadastro de Pessoa Física. |
| cnh | CharField | Carteira Nacional de Habilitação. |
| telefone | CharField | Número de contato do profissional. |
| status | CharField | Opções: ativo, inativo, em_rota ou disponível. |
| data_cadastro | DateTimeField | Data em que o motorista foi registrado no sistema. |

## Relacionamentos
* **1:1 com User**: Cada motorista está obrigatoriamente vinculado a um usuário do sistema para autenticação.
* **1:1 com Veículo**: Quando ativo, o motorista está vinculado a um veículo específico.
* **1:N com Rota**: Um motorista pode ter várias rotas, mas cada rota pertence a um único motorista.
* **1:N com Entrega**: Um motorista realiza várias entregas ao longo do tempo.

## Regras de Negócio Importantes ⚠️

* **Vínculo de Veículo**: Um motorista só pode ter um veículo ativo vinculado por vez.
* **Atualização de Status**: O motorista é responsável por atualizar o status das entregas (ex: "saiu para entrega", "entregue", "cliente ausente").
* **Privacidade de Dados**: O motorista possui acesso restrito apenas aos seus próprios dados e entregas.
* **Validação de Rota**: O motorista só pode visualizar as rotas que foram especificamente atribuídas a ele pelo Gestor.
