from __future__ import annotations

from datetime import datetime

from sqlalchemy import Text, Integer, Boolean, DateTime, func, text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.db import Base


class Papers(Base):
    __tablename__ = "papers"
    __table_args__ = {"schema": "cr_soles"}

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    title: Mapped[str] = mapped_column(Text, nullable=False)
    abstract: Mapped[str | None] = mapped_column(Text)
    doi: Mapped[str | None] = mapped_column(Text, unique=True)
    pmid: Mapped[str | None] = mapped_column(Text)
    year_published: Mapped[int | None] = mapped_column(Integer)
    journal: Mapped[str | None] = mapped_column(Text)
    first_author: Mapped[str | None] = mapped_column(Text)
    authors_display: Mapped[str | None] = mapped_column(Text)
    source_type: Mapped[str | None] = mapped_column(Text)
    source_record_id: Mapped[str | None] = mapped_column(Text)
    pdf_storage_path: Mapped[str | None] = mapped_column(Text)
    full_text_available: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    ocr_required: Mapped[bool | None] = mapped_column(Boolean)
    language: Mapped[str] = mapped_column(
        Text, nullable=False, server_default=text("'en'")
    )
    ingestion_status: Mapped[str | None] = mapped_column(Text)
    dedupe_key: Mapped[str | None] = mapped_column(Text)
    notes: Mapped[str | None] = mapped_column(Text)
    created_by: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("cr_soles.profiles.id", ondelete="SET NULL"),
    )
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

    extractions = relationship(
        "Extractions",
        back_populates="papers",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    pipeline_runs = relationship(
        "PipelineRuns",
        back_populates="papers",
        passive_deletes=True,
    )
    paper_files = relationship(
        "PaperFiles",
        back_populates="papers",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    staging_items = relationship(
        "PapersStaging",
        back_populates="papers",
        passive_deletes=True,
    )
