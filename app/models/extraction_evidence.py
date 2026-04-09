from __future__ import annotations

from datetime import datetime

from sqlalchemy import Text, Integer, Numeric, DateTime, func, text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.db import Base


class ExtractionEvidence(Base):
    __tablename__ = "extraction_evidence"
    __table_args__ = {"schema": "public"}

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    extraction_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("public.extractions.id", ondelete="CASCADE"),
        nullable=False,
    )
    field_name: Mapped[str | None] = mapped_column(Text)
    evidence_text: Mapped[str | None] = mapped_column(Text)
    page_number: Mapped[int | None] = mapped_column(Integer)
    section_label: Mapped[str | None] = mapped_column(Text)
    char_start: Mapped[int | None] = mapped_column(Integer)
    char_end: Mapped[int | None] = mapped_column(Integer)
    table_or_figure_label: Mapped[str | None] = mapped_column(Text)
    confidence: Mapped[float | None] = mapped_column(Numeric)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    extractions = relationship(
        "Extractions",
        back_populates="extraction_evidence",
        primaryjoin="ExtractionEvidence.extraction_id == Extractions.id",
        foreign_keys=extraction_id,
        passive_deletes=True,
    )
