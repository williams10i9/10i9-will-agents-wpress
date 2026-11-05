# Will Agents for WordPress

Interface local para orquestrar agentes temporários. A aplicação pode rodar em uma máquina de operação e usar o Ollama hospedado em outra máquina da mesma rede.

## Arquitetura

```text
Máquina A (GPU)                         Máquina B (operação)
Ollama + modelo qwen3:8b  <── rede ──  Interface + agentes + scripts EKS/WordPress
192.168.1.8:11434                       navegador em http://127.0.0.1:8787
```

O modelo permanece na Máquina A. A Máquina B envia solicitações ao Ollama e recebe as respostas; seus agentes, scripts e futuras integrações de deploy ficam na Máquina B.

## Preparar a Máquina A: servidor Ollama

1. Instale o Ollama e baixe o modelo uma única vez:

   ```bash
   ollama pull qwen3:8b
   ```

2. Configure o serviço para aceitar conexões da rede local:

   ```bash
   sudo systemctl edit ollama
   ```

   Adicione:

   ```ini
   [Service]
   Environment="OLLAMA_HOST=192.168.1.8:11434"
   ```

3. Recarregue e reinicie o serviço:

   ```bash
   sudo systemctl daemon-reload
   sudo systemctl restart ollama
   ```

4. Confirme que atende na rede:

   ```bash
   curl http://192.168.1.8:11434/api/tags
   ```

Substitua `192.168.1.8` pelo IP LAN atual da Máquina A caso ele mude. Depois dessa configuração, para usar o cliente Ollama diretamente na Máquina A, informe o mesmo endereço:

```bash
OLLAMA_HOST=192.168.1.8:11434 ollama list
```

## Preparar a Máquina B após clonar o projeto

1. Clone o repositório e entre na raiz:

   ```bash
   git clone <URL-DO-REPOSITORIO> will-agents-wpress
   cd will-agents-wpress
   ```

2. Instale o `uv`, se necessário:

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. Crie o arquivo de configuração local a partir do exemplo:

   ```bash
   cp .env.example .env
   ```

4. Em `.env`, defina o IP da Máquina A:

   ```text
   OLLAMA_BASE_URL=http://192.168.1.8:11434
   ```

5. Instale as dependências e valide a comunicação:

   ```bash
   uv sync
   curl http://192.168.1.8:11434/api/tags
   ```

6. Inicie a interface:

   ```bash
   CREWAI_DISABLE_TELEMETRY=true uv run agent-console
   ```

7. Abra `http://127.0.0.1:8787` no navegador da Máquina B.

## Desenvolvimento assistido

Configuração para Claude Code, Cursor (Composer) e Codex:

| Artefato | Uso |
|----------|-----|
| [AGENTS.md](AGENTS.md) | Entrada para Codex e agentes genéricos |
| [CLAUDE.md](CLAUDE.md) | Contexto ao abrir só este repo |
| [backlog/](backlog/) | Épicos e tasks (`epic-NNN`) |
| [plans/](plans/) | Planos confirmados no chat |

No monorepo Lactalis (`lactalis/`), regras adicionais ficam na raiz do workspace ([`CLAUDE.md`](../CLAUDE.md), `.cursor/rules/will-agents-wpress-*.mdc`) — **não** são commitadas neste remote.

## Jira somente leitura

O agente Leitor Jira usa o arquivo configurado em `JIRA_ENV_FILE` ou, por padrão, `/home/will/Downloads/env`. Esse arquivo deve permanecer fora do Git e conter `JIRA_BASE_URL`, `JIRA_EMAIL` e `JIRA_API_TOKEN`.

Exemplos de mensagens no chat:

- `Consulte SLAC-844`
- `Mostre todos os cards SLAC-`

Ele retorna até 30 cards mais recentes e não cria, edita ou comenta tickets.

## Versionamento

Versione o código e o `uv.lock`. Não versione `.venv/`, `.runtime/`, `.env` ou arquivos de credenciais: isso já está definido em `.gitignore`.
