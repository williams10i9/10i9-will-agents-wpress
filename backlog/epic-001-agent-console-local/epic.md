# EPIC 001 — agent-console-local

**Status:** em andamento  
**Prioridade:** alta (base do produto)  
**Depende de:** Ollama acessível na LAN  
**Bloqueia:** integrações futuras willbot ↔ UI

## Objetivo

Manter operacional a central local (`agent-console`): agentes CrewAI temporários, Ollama remoto, leitor Jira somente leitura e documentação/backlog para desenvolvimento assistido.

## Fora de escopo

- Deploy PRD ou escrita em Jira/WordPress
- Duplicar fluxos do CLI willbot (`10i9-willbot-autodeploy/lib/flows/`)

## Tasks (ordem)

| Ordem | Task | Arquivo | Status |
|-------|------|---------|--------|
| 1 | Config desenvolvimento assistido | [plans/plan_config_desenvolvimento_assistido.md](../../plans/plan_config_desenvolvimento_assistido.md) | entregue |

## Checklist (épico)

- [x] README operacional (Ollama duas máquinas, `uv`, agent-console)
- [x] AGENTS.md, CLAUDE.md, backlog, plans, CHANGELOG/VERSION
- [ ] Integração opcional com willbot (futuro)
- [ ] Novos agentes além de Jira read-only + planejamento CrewAI

## Referências

- [plan_config_desenvolvimento_assistido.md](../../plans/plan_config_desenvolvimento_assistido.md)
- [docs_will_agents_wpress.md](../../../global/global_docs/docs_will_agents_wpress.md) (monorepo Lactalis)
