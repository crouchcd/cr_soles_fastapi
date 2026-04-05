from __future__ import annotations

from datetime import datetime

from sqlalchemy import Text, Integer, DateTime, func, text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.db import Base


class PipelineRuns(Base):
    __tablename__ = "pipeline_runs"
    __table_args__ = {"schema": "cr_soles"}

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    paper_id: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("cr_soles.papers.id", ondelete="SET NULL"),
    )
    run_type: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str | None] = mapped_column(Text)
    triggered_by: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("cr_soles.profiles.id", ondelete="SET NULL"),
    )
    runpod_instance_label: Mapped[str | None] = mapped_column(Text)
    git_commit_sha: Mapped[str | None] = mapped_column(Text)
    pipeline_version: Mapped[str | None] = mapped_column(Text)
    config_json: Mapped[dict | None] = mapped_column(JSONB)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    duration_seconds: Mapped[int | None] = mapped_column(Integer)
    error_summary: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    papers = relationship(
        "Papers",
        back_populates="pipeline_runs",
        primaryjoin="PipelineRuns.paper_id == Papers.id",
        foreign_keys=paper_id,
        passive_deletes=True,
    )
    pipeline_steps = relationship(
        "PipelineSteps",
        back_populates="pipeline_runs",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    extractions = relationship(
        "Extractions",
        back_populates="pipeline_runs",
        passive_deletes=True,
    )
