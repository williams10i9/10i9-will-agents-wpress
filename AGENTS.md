# AGENTS.md — 10i9-will-agents-wpress

Guia para agentes de código (Codex, Cursor Composer, Claude Code) neste repositório.

## Projeto

- **Nome:** Will Agents for WordPress (`10i9-will-agents-wpress`)
- **Stack:** Python 3.10+, [uv](https://docs.astral.sh/uv/), CrewAI, FastAPI, Ollama
- **Versão:** ver [VERSION](VERSION) e [CHANGELOG.md](CHANGELOG.md)

## Setup

```bash
uv sync
cp .env.example .env
# Editar OLLAMA_BASE_URL (servidor Ollama na LAN)
```

Entry points: `uv run agent-console` (UI `:8787`), `uv run local-agents` (POC terminal).

## Arquitetura (resumo)

- Máquina A: Ollama + modelo
- Máquina B: este app + agentes + (futuro) scripts EKS/WP
- Detalhes: [README.md](README.md)

## Onde documentar trabalho

| Tipo | Local |
|------|--------|
| Plano confirmado no chat | [plans/](plans/) (`plan_*.md`, PT-BR) |
| Épicos / tasks | [backlog/](backlog/) |
| Brainstorm | [rascunho/](rascunho/) |

## Segurança

- `.env` e `JIRA_ENV_FILE` **nunca** no git
- Jira: GET/busca apenas — sem create/update/comment
- POC: agentes geram texto; não executar deploy PRD sem aprovação humana documentada

## Relação com willbot

| Repo | Papel |
|------|--------|
| Este | Orientação/planejamento local + UI |
| [10i9-willbot-autodeploy](../10i9-willbot-autodeploy/) | Orquestração terminal, fluxos SLAC, deploy assistido |

## Monorepo Lactalis

Contexto workspace (sem git na raiz): [../CLAUDE.md](../CLAUDE.md).  
Regras Cursor: `../.cursor/rules/will-agents-wpress-*.mdc` quando a pasta pai existir.
