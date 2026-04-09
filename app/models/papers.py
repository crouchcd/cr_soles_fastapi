from __future__ import annotations

from datetime import datetime

from sqlalchemy import Text, Integer, Boolean, DateTime, CheckConstraint, Index, func, text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.db import Base


class Papers(Base):
    __tablename__ = "papers"
    __table_args__ = (
        CheckConstraint(
            "ingestion_status = ANY (ARRAY['queued'::text, 'ingested'::text, 'failed'::text, 'needs_review'::text])",
            name="papers_ingestion_status_check",
        ),
        CheckConstraint(
            "year_published IS NULL OR (year_published >= 1800 AND year_published <= 2100)",
            name="papers_year_check",
        ),
        Index("idx_papers_doi", "doi"),
        Index("idx_papers_year_published", "year_published"),
        Index("idx_papers_first_author", "first_author"),
        Index("idx_papers_ingestion_status", "ingestion_status"),
        {"schema": "public"},
    )

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
    ocr_required: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    language: Mapped[str] = mapped_column(
        Text, nullable=False, server_default=text("'en'")
    )
    ingestion_status: Mapped[str] = mapped_column(
        Text, nullable=False, server_default=text("'queued'")
    )
    dedupe_key: Mapped[str | None] = mapped_column(Text)
    notes: Mapped[str | None] = mapped_column(Text)
    created_by: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("public.profiles.id", ondelete="SET NULL"),
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
