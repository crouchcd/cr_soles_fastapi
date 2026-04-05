from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.evaluations import Evaluations


def create_evaluation(
    db: Session,
    *,
    paper_id=None,
    extraction_id=None,
    evaluator_id=None,
    evaluation_type: str | None = None,
    dimension: str | None = None,
    score: float | None = None,
    label: str | None = None,
    notes: str | None = None,
) -> Evaluations:
    evaluation = Evaluations(
        paper_id=paper_id,
        extraction_id=extraction_id,
        evaluator_id=evaluator_id,
        evaluation_type=evaluation_type,
        dimension=dimension,
        score=score,
        label=label,
        notes=notes,
    )
    db.add(evaluation)
    db.flush()
    return evaluation
