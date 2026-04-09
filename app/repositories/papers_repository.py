from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.papers import Papers


def list_papers(
    db: Session,
    *,
    offset: int = 0,
    limit: int = 100,
) -> list[Papers]:
    query = select(Papers).offset(int(offset)).limit(int(limit))
    result = db.execute(query)
    return result.scalars().all()


def create_paper(
    db: Session,
    *,
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
    ingestion_status: str = "queued",
    dedupe_key: str | None = None,
    notes: str | None = None,
    created_by=None,
) -> Papers:
    paper = Papers(
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
        created_by=created_by,
    )
    db.add(paper)
    db.flush()
    return paper


def get_paper_by_id(
    db: Session,
    *,
    paper_id,
) -> Papers | None:
    return db.get(Papers, paper_id)


def update_paper_fields(
    db: Session,
    *,
    item: Papers,
    fields: dict,
) -> Papers:
    for key, value in fields.items():
        setattr(item, key, value)
    db.flush()
    return item
