# CLAUDE.md — 10i9-will-agents-wpress

Instruções para Claude Code neste repositório.

## O que é

Interface local (**agent-console**) para orquestrar agentes CrewAI temporários com Ollama (modelo `qwen3:8b`). A GPU pode ficar em outra máquina (`OLLAMA_BASE_URL`). Jira: **somente leitura** via arquivo externo (`JIRA_ENV_FILE`).

Deploy WordPress/EKS real: usar [10i9-lactalis-guides](../10i9-lactalis-guides/) e CLI [10i9-willbot-autodeploy](../10i9-willbot-autodeploy/) — **não** reimplementar fluxos de `lib/flows/` aqui.

## Comandos

```bash
cp .env.example .env   # OLLAMA_BASE_URL, opcional JIRA_ENV_FILE
uv sync
CREWAI_DISABLE_TELEMETRY=true uv run agent-console   # http://127.0.0.1:8787
uv run local-agents    # POC CLI sem UI
```

Não usar `npm run` para validar mudanças neste projeto.

## Mapa de código

| Path | Responsabilidade |
|------|------------------|
| `src/local_agents/web.py` | FastAPI, missões, leitor Jira, estáticos |
| `src/local_agents/main.py` | POC CrewAI linha de comando |
| `src/local_agents/static/` | UI do painel |
| `.runtime/` | Cache/dados CrewAI (gitignored) |

## Regras de implementação

- Comentários de código em **inglês**; docs de produto em **português (BR)**.
- Sem escrita Jira, sem comandos de sistema, sem WP/PRD até épico/plan explícito.
- Plans acionáveis: [plans/](plans/) · épicos: [backlog/](backlog/).

## Workspace Lactalis

Se este repo estiver em `lactalis/10i9-will-agents-wpress/`, regras adicionais do monorepo: [../CLAUDE.md](../CLAUDE.md), [../.claude/rules/will-agents-wpress-scope.md](../.claude/rules/will-agents-wpress-scope.md).

Commits **nesta pasta** (repo git próprio). Arquivos em `../.cursor/`, `../global/` não entram no remote deste repo.
