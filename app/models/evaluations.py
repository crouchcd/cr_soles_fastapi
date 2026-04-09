from __future__ import annotations

from datetime import datetime

from sqlalchemy import Text, Numeric, DateTime, func, text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.db import Base


class Evaluations(Base):
    __tablename__ = "evaluations"
    __table_args__ = {"schema": "public"}

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    paper_id: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("public.papers.id", ondelete="CASCADE"),
    )
    extraction_id: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("public.extractions.id", ondelete="CASCADE"),
    )
    evaluator_id: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("public.profiles.id", ondelete="SET NULL"),
    )
    evaluation_type: Mapped[str | None] = mapped_column(Text)
    dimension: Mapped[str | None] = mapped_column(Text)
    score: Mapped[float | None] = mapped_column(Numeric)
    label: Mapped[str | None] = mapped_column(Text)
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    extractions = relationship(
        "Extractions",
        back_populates="evaluations",
        primaryjoin="Evaluations.extraction_id == Extractions.id",
        foreign_keys=extraction_id,
        passive_deletes=True,
    )
