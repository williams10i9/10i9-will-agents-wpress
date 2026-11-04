"""Executa uma POC local, sem acesso a Jira, WordPress ou comandos do sistema."""

import os
from pathlib import Path

from dotenv import load_dotenv

# Evita que o CrewAI guarde estado na pasta pessoal do usuário. Todo estado desta
# POC fica no diretório .runtime do projeto, que pode ser removido sem afetar o SO.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")
os.environ.setdefault("XDG_DATA_HOME", str(PROJECT_ROOT / ".runtime" / "data"))
os.environ.setdefault("XDG_CACHE_HOME", str(PROJECT_ROOT / ".runtime" / "cache"))
os.environ.setdefault("CREWAI_DISABLE_TELEMETRY", "true")

from crewai import Agent, Crew, LLM, Process, Task


def main() -> None:
    llm = LLM(
        model="ollama/qwen3:8b",
        base_url=os.environ.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434"),
        temperature=0.2,
    )

    planner = Agent(
        role="Planejador de automação",
        goal="Transformar uma solicitação em um plano seguro e verificável.",
        backstory="Você trabalha apenas com propostas. Não acessa serviços externos nem executa comandos.",
        llm=llm,
        verbose=True,
    )
    reviewer = Agent(
        role="Revisor de segurança",
        goal="Identificar riscos e impor aprovação humana antes de qualquer ação externa.",
        backstory="Você bloqueia alterações em Jira, WordPress, arquivos fora da área de testes e execução de comandos.",
        llm=llm,
        verbose=True,
    )

    plan = Task(
        description=(
            "Crie um plano curto para uma automação que analisa uma tarefa de desenvolvimento "
            "e sugere passos de implementação. Não use ferramentas, não invente acesso a Jira "
            "ou WordPress e não execute comandos. Responda em português."
        ),
        expected_output="Plano em etapas com suposições e pontos de aprovação humana.",
        agent=planner,
    )
    safety_review = Task(
        description=(
            "Revise o plano anterior. Liste permissões mínimas necessárias no futuro e os "
            "controles obrigatórios para manter Jira e WordPress fora do escopo desta POC. "
            "Responda em português."
        ),
        expected_output="Checklist de segurança objetivo.",
        agent=reviewer,
        context=[plan],
    )

    crew = Crew(
        agents=[planner, reviewer],
        tasks=[plan, safety_review],
        process=Process.sequential,
        verbose=True,
    )
    result = crew.kickoff()
    print("\n=== Resultado da POC ===\n")
    print(result.raw)


if __name__ == "__main__":
    main()
