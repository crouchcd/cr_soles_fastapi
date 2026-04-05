from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Session

from app.models.agents_logs import PipelineRuns


def create_pipeline_run(
    db: Session,
    *,
    paper_id=None,
    run_type: str | None = None,
    status: str | None = None,
    triggered_by=None,
    runpod_instance_label: str | None = None,
    git_commit_sha: str | None = None,
    pipeline_version: str | None = None,
    config_json: dict | None = None,
    started_at: datetime | None = None,
    finished_at: datetime | None = None,
    duration_seconds: int | None = None,
    error_summary: str | None = None,
) -> PipelineRuns:
    run = PipelineRuns(
        paper_id=paper_id,
        run_type=run_type,
        status=status,
        triggered_by=triggered_by,
        runpod_instance_label=runpod_instance_label,
        git_commit_sha=git_commit_sha,
        pipeline_version=pipeline_version,
        config_json=config_json,
        started_at=started_at,
        finished_at=finished_at,
        duration_seconds=duration_seconds,
        error_summary=error_summary,
    )
    db.add(run)
    db.flush()
    return run
