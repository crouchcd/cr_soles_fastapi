from __future__ import annotations

from datetime import datetime

from sqlalchemy import Text, Integer, Boolean, Numeric, DateTime, func, text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.db import Base


class Extractions(Base):
    __tablename__ = "extractions"
    __table_args__ = {"schema": "public"}

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    paper_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("public.papers.id", ondelete="CASCADE"),
        nullable=False,
    )
    run_id: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("public.pipeline_runs.id", ondelete="SET NULL"),
    )
    extraction_version: Mapped[str] = mapped_column(Text, nullable=False)
    is_current: Mapped[bool | None] = mapped_column(Boolean)
    meets_target_criteria: Mapped[bool | None] = mapped_column(Boolean)
    eligibility_confidence: Mapped[float | None] = mapped_column(Numeric)
    exclusion_reason: Mapped[str | None] = mapped_column(Text)
    brain_measure_present: Mapped[bool | None] = mapped_column(Boolean)
    brain_measure_description: Mapped[str | None] = mapped_column(Text)
    brain_measure_category: Mapped[str | None] = mapped_column(Text)
    cognition_measure_present: Mapped[bool | None] = mapped_column(Boolean)
    cognition_measure_description: Mapped[str | None] = mapped_column(Text)
    cognitive_domain: Mapped[str | None] = mapped_column(Text)
    moderator_present: Mapped[bool | None] = mapped_column(Boolean)
    moderator_description: Mapped[str | None] = mapped_column(Text)
    moderator_category: Mapped[str | None] = mapped_column(Text)
    interaction_tested: Mapped[bool | None] = mapped_column(Boolean)
    interaction_description: Mapped[str | None] = mapped_column(Text)
    sample_size: Mapped[int | None] = mapped_column(Integer)
    population_description: Mapped[str | None] = mapped_column(Text)
    study_design: Mapped[str | None] = mapped_column(Text)
    country: Mapped[str | None] = mapped_column(Text)
    statistical_approach: Mapped[str | None] = mapped_column(Text)
    main_finding_summary: Mapped[str | None] = mapped_column(Text)
    overall_confidence: Mapped[float | None] = mapped_column(Numeric)
    human_review_status: Mapped[str | None] = mapped_column(Text)
    reviewed_by: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("public.profiles.id", ondelete="SET NULL"),
    )
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    papers = relationship(
        "Papers",
        back_populates="extractions",
        primaryjoin="Extractions.paper_id == Papers.id",
        foreign_keys=paper_id,
        passive_deletes=True,
    )
    pipeline_runs = relationship(
        "PipelineRuns",
        back_populates="extractions",
        primaryjoin="Extractions.run_id == PipelineRuns.id",
        foreign_keys=run_id,
        passive_deletes=True,
    )
    evaluations = relationship(
        "Evaluations",
        back_populates="extractions",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    extraction_evidence = relationship(
        "ExtractionEvidence",
        back_populates="extractions",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
