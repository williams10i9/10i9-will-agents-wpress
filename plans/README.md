# Plans — Will Agents WordPress

Destino **canônico** de planos quando o escopo é `10i9-will-agents-wpress`, **agent-console**, CrewAI/Ollama ou o usuário cita **will-agents-wpress**.

Demais assuntos do monorepo Lactalis (sem este projeto): [global/cursor_chats](../../global/cursor_chats).

Willbot / autodeploy: [10i9-willbot-autodeploy/plans](../../10i9-willbot-autodeploy/plans/).

## Convenção de nomes

- Arquivo: `plan_<tema_curto>.md` em **snake_case**, conteúdo em **português (BR)**.
- Um plan por iniciativa; **atualizar o mesmo arquivo** enquanto o épico/chat evoluir.
- Modo Plan do Cursor: após confirmação, persistir cópia final aqui (não confiar só em `.cursor/plans/`).

## Rascunho vs plan

| Tipo | Pasta |
|------|--------|
| Visão, brainstorm, sem tasks fechadas | [../rascunho/](../rascunho/) |
| Plano acionável com critérios de pronto | `plans/` (esta pasta) |

## Runbooks

Referenciar [10i9-lactalis-guides](../../10i9-lactalis-guides) e [10i9-willbot-autodeploy](../../10i9-willbot-autodeploy) para deploy — não copiar runbooks inteiros nos plans.

## Segredos

`.env` local e `JIRA_ENV_FILE` externo (gitignored). Ver [docs_credenciais_trash_policy.md](../../global/global_docs/docs_credenciais_trash_policy.md).

## PRD

Qualquer plan que inclua deploy PRD deve documentar **gate de aprovação humana** antes da execução.

## Backlog vs plans

| Pasta | Uso |
|-------|-----|
| [../backlog/](../backlog/) | Épicos **`epic-NNN-<slug>`** e tasks com checklist |
| `plans/` (esta pasta) | Plano de execução confirmado no chat |

## Índice

| Arquivo | Data | Resumo |
|---------|------|--------|
| [plan_config_desenvolvimento_assistido.md](plan_config_desenvolvimento_assistido.md) | 2026-11-04 | Configuração assistida (Claude, Cursor, Codex) — 1ª passagem |
