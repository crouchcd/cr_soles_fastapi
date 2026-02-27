from __future__ import annotations
from sqlalchemy.orm import Session

from app.models.extractions import Extractions


def create_extraction(
    db: Session,
    *,
    paper_id,
    extraction_version: str,
    metadata_jsonb: dict | None = None,
    study_design_jsonb: dict | None = None,
    sample_jsonb: dict | None = None,
    outcomes_jsonb: dict | None = None,
    risk_of_bias_jsonb: dict | None = None,
    status: str = "success",
) -> Extractions:
    extraction = Extractions(
        paper_id=paper_id,
        extraction_version=extraction_version,
        metadata_jsonb=metadata_jsonb,
        study_design_jsonb=study_design_jsonb,
        sample_jsonb=sample_jsonb,
        outcomes_jsonb=outcomes_jsonb,
        risk_of_bias_jsonb=risk_of_bias_jsonb,
        status=status,
    )
    db.add(extraction)
    db.flush()
    return extraction
