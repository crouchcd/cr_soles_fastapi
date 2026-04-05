from __future__ import annotations

from datetime import datetime

from sqlalchemy import Text, Integer, Numeric, DateTime, func, text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.db import Base


class PipelineSteps(Base):
    __tablename__ = "pipeline_steps"
    __table_args__ = {"schema": "cr_soles"}

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    run_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("cr_soles.pipeline_runs.id", ondelete="CASCADE"),
        nullable=False,
    )
    step_name: Mapped[str | None] = mapped_column(Text)
    step_order: Mapped[int | None] = mapped_column(Integer)
    model_name: Mapped[str | None] = mapped_column(Text)
    model_provider: Mapped[str | None] = mapped_column(Text)
    prompt_version: Mapped[str | None] = mapped_column(Text)
    input_ref: Mapped[str | None] = mapped_column(Text)
    output_ref: Mapped[str | None] = mapped_column(Text)
    input_tokens: Mapped[int | None] = mapped_column(Integer)
    output_tokens: Mapped[int | None] = mapped_column(Integer)
    cost_usd_estimate: Mapped[float | None] = mapped_column(Numeric)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    duration_ms: Mapped[int | None] = mapped_column(Integer)
    error_message: Mapped[str | None] = mapped_column(Text)
    metrics_json: Mapped[dict | None] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    pipeline_runs = relationship(
        "PipelineRuns",
        back_populates="pipeline_steps",
        primaryjoin="PipelineSteps.run_id == PipelineRuns.id",
        foreign_keys=run_id,
        passive_deletes=True,
    )
