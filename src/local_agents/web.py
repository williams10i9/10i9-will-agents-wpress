"""Painel local para orquestrar agentes temporários, sem integrações externas."""

import os
import re
import threading
import uuid
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")
os.environ.setdefault("CREWAI_DISABLE_TELEMETRY", "true")
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434")

from crewai import Agent, Crew, LLM, Process, Task

STATIC_DIR = Path(__file__).with_name("static")
app = FastAPI(title="Central de Agentes Local")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

lock = threading.Lock()
mission: dict[str, Any] = {
    "status": "idle",
    "agents": [],
    "events": [],
    "result": None,
}
chat_history: list[dict[str, str]] = []
JIRA_ENV_FILE = Path(os.environ.get("JIRA_ENV_FILE", "/home/will/Downloads/env"))


class MissionRequest(BaseModel):
    message: str = Field(min_length=3, max_length=6000)


def event(message: str) -> None:
    with lock:
        mission["events"].append(message)


def set_agent(name: str, role: str, status: str) -> None:
    with lock:
        for agent in mission["agents"]:
            if agent["name"] == name:
                agent["status"] = status
                return
        mission["agents"].append({"name": name, "role": role, "status": status})


def jira_credentials() -> tuple[str, str, str]:
    """Lê credenciais sem executar o arquivo e sem enviá-las à interface."""
    try:
        values: dict[str, str] = {}
        for raw_line in JIRA_ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if line.startswith("export "):
                line = line[7:].strip()
            if "=" not in line or line.startswith("#"):
                continue
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip().strip("'\"")
        return values["JIRA_BASE_URL"].rstrip("/"), values["JIRA_EMAIL"], values["JIRA_API_TOKEN"]
    except (OSError, KeyError) as exc:
        raise RuntimeError("As credenciais de leitura do Jira não estão disponíveis.") from exc


def jira_reader(message: str) -> str | None:
    """Consulta uma issue ou um projeto por prefixo, exclusivamente por GET/POST de busca."""
    issue_match = re.search(r"\b([A-Z][A-Z0-9]+-\d+)\b", message.upper())
    prefix_match = re.search(r"\b([A-Z][A-Z0-9]+)-(?=\s|$)", message.upper())
    if not issue_match and not prefix_match:
        return None

    base_url, email, token = jira_credentials()
    fields = ["summary", "status", "priority", "assignee", "updated"]
    if issue_match:
        key = issue_match.group(1)
        response = requests.get(
            f"{base_url}/rest/api/3/issue/{key}",
            params={"fields": ",".join(fields)},
            auth=(email, token),
            timeout=30,
        )
        response.raise_for_status()
        issues = [response.json()]
        heading = f"Leitura do card {key}"
    else:
        project = prefix_match.group(1)
        response = requests.post(
            f"{base_url}/rest/api/3/search/jql",
            json={
                "jql": f"project = {project} ORDER BY updated DESC",
                "maxResults": 30,
                "fields": fields,
            },
            auth=(email, token),
            timeout=30,
        )
        response.raise_for_status()
        issues = response.json().get("issues", [])
        heading = f"Cards {project}- (até 30, mais recentes primeiro)"

    if not issues:
        return f"**{heading}**\n\nNenhum card encontrado."
    rows = []
    for issue in issues:
        item = issue["fields"]
        status_name = item.get("status", {}).get("name", "Sem status")
        priority = (item.get("priority") or {}).get("name", "Sem prioridade")
        assignee = (item.get("assignee") or {}).get("displayName", "Não atribuído")
        rows.append(f"- **{issue['key']}** — {item.get('summary', 'Sem título')}  \n  {status_name} · {priority} · {assignee}")
    return f"**{heading}**\n\n" + "\n".join(rows) + "\n\nConsulta somente leitura. Nenhum card foi alterado."


def run_mission(user_message: str) -> None:
    """Cria especialistas para esta missão e os remove quando terminam."""
    try:
        jira_requested = bool(re.search(r"\b[A-Z][A-Z0-9]+-(?:\d+|(?=\s|$))", user_message.upper()))
        if jira_requested:
            event("O orquestrador criou um agente temporário de leitura Jira.")
            set_agent("Leitor Jira", "Consulta cards sem alterar dados", "consultando")
            result = jira_reader(user_message)
            if result is None:
                raise RuntimeError("Não identifiquei uma chave ou prefixo Jira válido.")
            set_agent("Leitor Jira", "Consulta cards sem alterar dados", "concluído")
            event("A consulta foi concluída e o agente de leitura Jira foi removido.")
            with lock:
                mission["result"] = result
                mission["status"] = "completed"
                chat_history.append({"user": user_message, "assistant": result})
                mission["agents"] = []
            return

        event("O orquestrador avaliou a solicitação e criou especialistas temporários.")
        set_agent("Analista", "Transforma a orientação em um plano", "trabalhando")
        set_agent("Guardião", "Revisa limites e aprovações", "aguardando")

        history = "\n".join(
            f"Usuário: {item['user']}\nOrquestrador: {item['assistant']}"
            for item in chat_history[-3:]
            if item.get("assistant")
        ) or "Sem histórico anterior."
        llm = LLM(model="ollama/qwen3:8b", base_url=OLLAMA_BASE_URL, temperature=0.2)
        analyst = Agent(
            role="Analista de automação",
            goal="Converter a orientação do usuário em um plano curto, concreto e seguro.",
            backstory="Você é um especialista temporário. Não usa ferramentas e não acessa sistemas externos.",
            llm=llm,
            verbose=False,
        )
        guardian = Agent(
            role="Guardião de segurança",
            goal="Revisar o plano e indicar o que exige aprovação humana.",
            backstory="Você é temporário, conservador e bloqueia Jira, WordPress e comandos externos nesta POC.",
            llm=llm,
            verbose=False,
        )
        plan = Task(
            description=(
                f"Histórico recente:\n{history}\n\nNova orientação do usuário:\n{user_message}\n\n"
                "Responda em português com um plano objetivo. Não alegue ter acessado Jira, WordPress, "
                "arquivos, navegadores ou comandos."
            ),
            expected_output="Plano em etapas e dúvidas que o orquestrador deve confirmar.",
            agent=analyst,
        )
        review = Task(
            description=(
                "Revise o plano anterior. Diga quais limites foram respeitados e quais ações futuras "
                "exigiriam aprovação humana. Seja breve e responda em português."
            ),
            expected_output="Checklist de segurança curto.",
            agent=guardian,
            context=[plan],
        )

        crew = Crew(agents=[analyst, guardian], tasks=[plan, review], process=Process.sequential, verbose=False)
        result = crew.kickoff().raw
        set_agent("Analista", "Transforma a orientação em um plano", "concluído")
        set_agent("Guardião", "Revisa limites e aprovações", "concluído")
        event("Os especialistas concluíram a missão e foram removidos da equipe ativa.")
        with lock:
            mission["result"] = result
            mission["status"] = "completed"
            chat_history.append({"user": user_message, "assistant": result})
            mission["agents"] = []
    except Exception as exc:
        with lock:
            mission["status"] = "failed"
            mission["result"] = f"A missão não foi concluída: {exc}"
            mission["agents"] = []
        event("A missão foi interrompida; nenhum agente permaneceu ativo.")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/state")
def state() -> dict[str, Any]:
    with lock:
        return {**mission, "history": chat_history[-8:]}


@app.get("/api/config")
def config() -> dict[str, str]:
    parsed = urlparse(OLLAMA_BASE_URL)
    return {
        "ollama_url": OLLAMA_BASE_URL,
        "ollama_host": parsed.hostname or "Não configurado",
    }


@app.post("/api/missions")
def create_mission(request: MissionRequest) -> dict[str, str]:
    with lock:
        if mission["status"] == "working":
            raise HTTPException(status_code=409, detail="Uma missão já está em andamento.")
        mission.update({"status": "working", "agents": [], "events": [], "result": None, "id": str(uuid.uuid4())})
    threading.Thread(target=run_mission, args=(request.message,), daemon=True).start()
    return {"status": "started"}


def main() -> None:
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8787)
