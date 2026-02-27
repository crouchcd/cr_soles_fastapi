from __future__ import annotations
from sqlalchemy.orm import Session

from app.models.evaluations import Evaluations


def create_evaluation(
    db: Session,
    *,
    extraction_id,
    evaluator_id: str,
    agreement_scores: dict | None = None,
    notes: str | None = None,
) -> Evaluations:
    evaluation = Evaluations(
        extraction_id=extraction_id,
        evaluator_id=evaluator_id,
        agreement_scores=agreement_scores,
        notes=notes,
    )
    db.add(evaluation)
    db.flush()
    return evaluation
