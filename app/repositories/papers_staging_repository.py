from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import select, union_all, func
from sqlalchemy.orm import Session
from typing import Any

from app.models.papers_staging import PapersStaging


def list_papers_staging(
    db: Session,
    *,
    offset: int = 0,
    limit: int = 100,
) -> list[PapersStaging]:
    latest_idx_per_paper = (
        select(
            PapersStaging.idx.label("idx"),
            func.row_number()
            .over(
                partition_by=PapersStaging.id,
                order_by=PapersStaging.idx.desc(),
            )
            .label("rn"),
        )
        .where(
            PapersStaging.is_approved.is_(False),
            PapersStaging.id.isnot(None),
        )
        .subquery()
    )

    selected_idxs = union_all(
        select(latest_idx_per_paper.c.idx).where(latest_idx_per_paper.c.rn == 1),
        select(PapersStaging.idx).where(
            PapersStaging.is_approved.is_(False),
            PapersStaging.id.is_(None),
        ),
    ).subquery()

    query = (
        select(PapersStaging)
        .join(selected_idxs, PapersStaging.idx == selected_idxs.c.idx)
        .order_by(PapersStaging.idx.desc())
        .offset(int(offset))
        .limit(int(limit))
    )

    result = db.execute(query)
    return result.scalars().all()


def create_papers_staging(
    db: Session,
    *,
    paper_id: UUID | None = None,
    title: str,
    abstract: str | None = None,
    doi: str | None = None,
    pmid: str | None = None,
    year_published: int | None = None,
    journal: str | None = None,
    first_author: str | None = None,
    authors_display: str | None = None,
    source_type: str | None = None,
    source_record_id: str | None = None,
    pdf_storage_path: str | None = None,
    full_text_available: bool = False,
    ocr_required: bool | None = None,
    language: str = "en",
    ingestion_status: str | None = None,
    dedupe_key: str | None = None,
    notes: str | None = None,
    is_approved: bool | None = None,
    approval_timestamp: Any | None = None,
) -> PapersStaging:
    paper_staging = PapersStaging(
        id=paper_id,
        title=title,
        abstract=abstract,
        doi=doi,
        pmid=pmid,
        year_published=year_published,
        journal=journal,
        first_author=first_author,
        authors_display=authors_display,
        source_type=source_type,
        source_record_id=source_record_id,
        pdf_storage_path=pdf_storage_path,
        full_text_available=full_text_available,
        ocr_required=ocr_required,
        language=language,
        ingestion_status=ingestion_status,
        dedupe_key=dedupe_key,
        notes=notes,
    )

    if is_approved is not None:
        paper_staging.is_approved = is_approved
    if approval_timestamp is not None:
        paper_staging.approval_timestamp = approval_timestamp

    db.add(paper_staging)
    db.flush()
    return paper_staging


def get_papers_staging_by_idx(
    db: Session,
    *,
    idx: int,
) -> PapersStaging | None:
    return db.get(PapersStaging, idx)


def get_papers_staging_by_paper_id(
    db: Session,
    *,
    paper_id: UUID,
) -> PapersStaging | None:
    stmt = (
        select(PapersStaging)
        .where(PapersStaging.id == paper_id)
        .order_by(PapersStaging.idx.desc())
    )
    return db.execute(stmt).scalars().first()


def update_papers_staging_fields(
    db: Session,
    *,
    item: PapersStaging,
    fields: dict,
) -> PapersStaging:
    for key, value in fields.items():
        setattr(item, key, value)
    db.flush()
    return item


def _get_papers_staging(db: Session, identifier: str) -> PapersStaging | None:
    if identifier.isdigit():
        return db.get(PapersStaging, int(identifier))
    try:
        value = UUID(identifier)
    except ValueError:
        return None
    stmt = (
        select(PapersStaging)
        .where(PapersStaging.id == value)
        .order_by(PapersStaging.idx.desc())
    )
    return db.execute(stmt).scalars().first()
