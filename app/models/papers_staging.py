from __future__ import annotations

from datetime import datetime

from sqlalchemy import Text, Integer, Boolean, DateTime, func, text, ForeignKey, Identity
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.db import Base


class PapersStaging(Base):
    __tablename__ = "staging_papers"
    __table_args__ = {"schema": "public"}

    idx: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    id: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("public.papers.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    is_approved: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    approval_timestamp: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # Replicates papers columns
    title: Mapped[str] = mapped_column(Text, nullable=False)
    abstract: Mapped[str | None] = mapped_column(Text)
    doi: Mapped[str | None] = mapped_column(Text)
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
        back_populates="staging_items",
        primaryjoin="PapersStaging.id == Papers.id",
        foreign_keys=id,
        passive_deletes=True,
    )
