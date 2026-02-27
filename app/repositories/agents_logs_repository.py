from __future__ import annotations
from sqlalchemy.orm import Session

from app.models.agents_logs import AgentLogs


def create_agent_log(
    db: Session,
    *,
    agent_name: str,
    paper_id=None,
    extraction_id=None,
    raw_output: str | None = None,
    cleaned_output: dict | None = None,
    input_text: str | None = None,
    node_name: str | None = None,
    prompt_hash: str | None = None,
    model_name: str | None = None,
) -> AgentLogs:
    log = AgentLogs(
        paper_id=paper_id,
        extraction_id=extraction_id,
        agent_name=agent_name,
        raw_output=raw_output,
        cleaned_output=cleaned_output,
        input=input_text,
        node_name=node_name,
        prompt_hash=prompt_hash,
        model_name=model_name,
    )
    db.add(log)
    db.flush()
    return log
