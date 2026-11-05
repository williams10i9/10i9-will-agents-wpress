# Plan — configuração desenvolvimento assistido

**Data:** 2026-11-04  
**Épico:** [epic-001-agent-console-local](../backlog/epic-001-agent-console-local/epic.md)  
**Status:** entregue (1ª passagem)

## Objetivo

Incluir `10i9-will-agents-wpress` no ecossistema de desenvolvimento assistido do workspace Lactalis (Claude, Cursor/Composer, Codex), com paridade de tooling (backlog, versionamento, plans) em relação ao willbot.

## Checklist

### Padrões globais (workspace, sem git no remote wpress)

- [x] `global/cursor_standards/BACKLOG.md` — linha will-agents-wpress + seção backlog vs plans
- [x] `global/cursor_standards/VERSIONING.md` — CHANGELOG + VERSION
- [x] `.cursor/skills/backlog-bootstrap/SKILL.md` — quarto projeto
- [x] `.cursor/rules/tooling-backlog.mdc` e `tooling-versioning.mdc` — globs

### Regras Claude / Cursor (workspace)

- [x] `.claude/rules/will-agents-wpress-scope.md`
- [x] `.claude/rules/will-agents-wpress-plans.md`
- [x] `.cursor/rules/will-agents-wpress-scope.mdc`
- [x] `.cursor/rules/will-agents-wpress-plans-trigger.mdc` (alwaysApply)
- [x] `CLAUDE.md` raiz workspace
- [x] `.cursor/rules/workspace-lactalis-no-root-git.mdc` — repo próprio wpress

### Repo `10i9-will-agents-wpress` (commit neste remote)

- [x] `AGENTS.md`, `CLAUDE.md`, `CHANGELOG.md`, `VERSION`
- [x] `backlog/`, `plans/`, `rascunho/`
- [x] `pyproject.toml` — nome `will-agents-wpress`, deps explícitas
- [x] README — seção desenvolvimento assistido
- [x] `.vscode/settings.json` — interpreter `.venv`
- [x] Este plan + épico 001

### Documentação global

- [x] `global/global_docs/docs_will_agents_wpress.md`

## Não feito (próximas sessões)

- Integração UI ↔ willbot CLI
- Novos agentes com ferramentas (WP/EKS)
- Tag git `v0.1.0` (só com aprovação explícita)

## Aceite

Todos os itens marcados `[x]` acima verificáveis por path no monorepo Lactalis e no repo wpress.
