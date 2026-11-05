# Changelog

Alterações notáveis do **10i9-will-agents-wpress** (UI local + agentes CrewAI / Ollama).

Formato [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/).  
SemVer: quando clonado no monorepo Lactalis, ver [global/cursor_standards/VERSIONING.md](../global/cursor_standards/VERSIONING.md).

## [Unreleased]

### Added

- Scaffold de desenvolvimento assistido (AGENTS.md, CLAUDE.md, backlog, plans, regras workspace).
- Documentação operacional no README (Ollama remoto, agent-console, Jira read-only).

### Changed

- `pyproject.toml`: pacote renomeado para `will-agents-wpress`; dependências explícitas `python-dotenv` e `requests`.

## [0.1.0] - 2026-11-04

POC inicial: CrewAI + FastAPI (`agent-console`), leitor Jira somente leitura, CLI `local-agents`.
