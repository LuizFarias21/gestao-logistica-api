# COMO CONTRIBUIR


## 1. Clone o repositório

```bash
git clone https://github.com/LuizFarias21/gestao-logistica-api.git
cd gestao-logistica-api
```

---

## 2. Crie e ative o ambiente virtual

**Linux / macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell)**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows (cmd)**

```cmd
python -m venv .venv
.\.venv\Scripts\activate
```

> Após ativar o `venv`, você deverá ver o prefixo `(.venv)` no seu terminal.

---

## 3. Instale dependências

Com o `venv` ativado:

```bash
pip install -r requirements.txt
```

---

## 4. Crie uma branch

Crie uma branch cujo nome descreva claramente o que você irá fazer. Use um padrão consistente, por exemplo:

* `feat/<descrição-curta>` — para novas funcionalidades
* `fix/<descrição-curta>` — para correções de bug
* `chore/<descrição-curta>` — para tarefas/ajustes

Exemplos:

```bash
git checkout -b feat/adicionar-endpoint-pedidos
git checkout -b fix/corrige-calculo-frete
```

Se estiver relacionado a uma issue, inclua a referência da issue no título do PR e no commit.

---

## 5. Formate o código com `ruff`

Antes de commitar, rode o `ruff` para formatar o código:

```bash
ruff format .
```

Você também pode verificar problemas sem aplicar alterações com:

```bash
ruff check .
```

---

## 6. Faça commits — Conventional Commits em português

Use o padrão **Conventional Commits**, em português. Inclua **#<número-da-issue>** no início da mensagem para vincular à issue quando houver.

Formato sugerido:

```
#5 feat: implementa validação de CPF no cadastro
```

Alguns tipos comuns:

* `feat:` — nova funcionalidade
* `fix:` — correção de bug
* `docs:` — documentação
* `style:` — formatação/código sem alteração lógica
* `refactor:` — refatoração
* `test:` — testes
* `chore:` — tarefas diversas

Exemplo completo:

```bash
git add .
git commit -m "#12 fix: corrige cálculo do total do pedido"
```

---

## 7. Abra um Pull Request

1. Faça push da sua branch para o repositório remoto:

```bash
git push origin dev
```

2. No GitHub, abra um **Pull Request** da sua branch para a `dev`.
3. No PR:

   * Marque o **líder do projeto** como revisor (assinale o usuário responsável no campo de reviewers).

---

## 8. Observações e boas práticas

* Rode `ruff format .` e `ruff check .` para manter o código padronizado.
* Escreva commits pequenos e focados — facilita a revisão.
* Antes de fazer `git push`é recomendável rodar `git pull origin dev` antes.

---
