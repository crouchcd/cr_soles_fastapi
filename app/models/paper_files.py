from __future__ import annotations

from datetime import datetime

from sqlalchemy import Text, Integer, BigInteger, Boolean, DateTime, func, text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.db import Base


class PaperFiles(Base):
    __tablename__ = "paper_files"
    __table_args__ = {"schema": "cr_soles"}

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    paper_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("cr_soles.papers.id", ondelete="CASCADE"),
        nullable=False,
    )
    file_kind: Mapped[str | None] = mapped_column(Text)
    storage_path: Mapped[str] = mapped_column(Text, nullable=False)
    file_name: Mapped[str | None] = mapped_column(Text)
    mime_type: Mapped[str | None] = mapped_column(Text)
    file_size_bytes: Mapped[int | None] = mapped_column(BigInteger)
    checksum_sh256: Mapped[str | None] = mapped_column(Text)
    version: Mapped[int | None] = mapped_column(Integer)
    is_primary: Mapped[bool | None] = mapped_column(Boolean)
    uploaded_by: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("cr_soles.profiles.id", ondelete="SET NULL"),
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    papers = relationship(
        "Papers",
        back_populates="paper_files",
        primaryjoin="PaperFiles.paper_id == Papers.id",
        foreign_keys=paper_id,
        passive_deletes=True,
    )
