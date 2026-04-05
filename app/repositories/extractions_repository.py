from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Session

from app.models.extractions import Extractions


def create_extraction(
    db: Session,
    *,
    paper_id,
    extraction_version: str,
    run_id=None,
    is_current: bool | None = None,
    meets_target_criteria: bool | None = None,
    eligibility_confidence: float | None = None,
    exclusion_reason: str | None = None,
    brain_measure_present: bool | None = None,
    brain_measure_description: str | None = None,
    brain_measure_category: str | None = None,
    cognition_measure_present: bool | None = None,
    cognition_measure_description: str | None = None,
    cognitive_domain: str | None = None,
    moderator_present: bool | None = None,
    moderator_description: str | None = None,
    moderator_category: str | None = None,
    interaction_tested: bool | None = None,
    interaction_description: str | None = None,
    sample_size: int | None = None,
    population_description: str | None = None,
    study_design: str | None = None,
    country: str | None = None,
    statistical_approach: str | None = None,
    main_finding_summary: str | None = None,
    overall_confidence: float | None = None,
    human_review_status: str | None = None,
    reviewed_by=None,
    reviewed_at: datetime | None = None,
) -> Extractions:
    extraction = Extractions(
        paper_id=paper_id,
        extraction_version=extraction_version,
        run_id=run_id,
        is_current=is_current,
        meets_target_criteria=meets_target_criteria,
        eligibility_confidence=eligibility_confidence,
        exclusion_reason=exclusion_reason,
        brain_measure_present=brain_measure_present,
        brain_measure_description=brain_measure_description,
        brain_measure_category=brain_measure_category,
        cognition_measure_present=cognition_measure_present,
        cognition_measure_description=cognition_measure_description,
        cognitive_domain=cognitive_domain,
        moderator_present=moderator_present,
        moderator_description=moderator_description,
        moderator_category=moderator_category,
        interaction_tested=interaction_tested,
        interaction_description=interaction_description,
        sample_size=sample_size,
        population_description=population_description,
        study_design=study_design,
        country=country,
        statistical_approach=statistical_approach,
        main_finding_summary=main_finding_summary,
        overall_confidence=overall_confidence,
        human_review_status=human_review_status,
        reviewed_by=reviewed_by,
        reviewed_at=reviewed_at,
    )
    db.add(extraction)
    db.flush()
    return extraction
