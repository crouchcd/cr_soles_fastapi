from __future__ import annotations

import json
from uuid import UUID
from sqlalchemy.orm import Session

from app.core.logger import set_log
from app.enums.paper_review import ReviewTableType
from app.models.papers import Papers
# from app.models.papers_staging import PapersStaging
from app.repositories.papers_repository import (
    list_papers,
    get_paper_by_id,
    update_paper_fields,
    # create_paper,
)
# from app.repositories.papers_staging_repository import (
#     list_papers_staging,
#     get_papers_staging_by_idx,
#     get_papers_staging_by_paper_id,
#     create_papers_staging,
#     update_papers_staging_fields,
# )

ALLOWED_EDIT_KEYS = (
    "title",
    "abstract",
    "doi",
    "pmid",
    "year_published",
    "journal",
    "first_author",
    "authors_display",
    "source_type",
    "ingestion_status",
    "notes",
)


def _serialize_papers(item: Papers) -> dict:
    return {
        "id": item.id,
        "title": item.title,
        "abstract": item.abstract,
        "doi": item.doi,
        "pmid": item.pmid,
        "year_published": item.year_published,
        "journal": item.journal,
        "first_author": item.first_author,
        "authors_display": item.authors_display,
        "source_type": item.source_type,
        "ingestion_status": item.ingestion_status,
        "notes": item.notes,
        "created_at": item.created_at,
    }


def fetch_review_papers(
    db: Session,
    *,
    offset: int,
    limit: int,
    table_type: ReviewTableType,
) -> dict:
    set_log(
        f"fetch_review_papers: table_type={table_type} offset={offset} limit={limit}"
    )

    # if table_type == ReviewTableType.PAPERS_STAGING:
    #     items = list_papers_staging(db, offset=offset, limit=limit)
    #     payload = [_serialize_papers_staging(item) for item in items]
    # el
    if table_type == ReviewTableType.PAPERS:
        items = list_papers(db, offset=offset, limit=limit)
        payload = [_serialize_papers(item) for item in items]
    else:
        raise ValueError(f"Unsupported table_type: {table_type}")

    return {
        "table_type": table_type,
        "offset": offset,
        "limit": limit,
        "items": payload,
    }


def _normalize_edit_payload(payload: dict) -> dict:
    cleaned: dict = {}
    for key in ALLOWED_EDIT_KEYS:
        if key not in payload:
            continue
        value = payload.get(key)
        if key == "year_published":
            if value is None or value == "":
                cleaned[key] = None
            elif isinstance(value, int):
                cleaned[key] = value
            elif isinstance(value, str) and value.strip().isdigit():
                cleaned[key] = int(value.strip())
            else:
                raise ValueError("Invalid year_published value.")
        else:
            cleaned[key] = value
    return cleaned


def _parse_payload(payload: str | dict) -> dict:
    if isinstance(payload, dict):
        return payload
    if not payload:
        return {}
    try:
        return json.loads(payload)
    except json.JSONDecodeError as exc:
        raise ValueError("payload must be valid JSON.") from exc


# def _serialize_papers_staging(item: PapersStaging) -> dict:
#     return {
#         "idx": item.idx,
#         "paper_id": item.id,
#         "is_approved": item.is_approved,
#         "approval_timestamp": item.approval_timestamp,
#         "title": item.title,
#         "abstract": item.abstract,
#         "doi": item.doi,
#         "pmid": item.pmid,
#         "year_published": item.year_published,
#         "journal": item.journal,
#         "first_author": item.first_author,
#         "authors_display": item.authors_display,
#         "source_type": item.source_type,
#         "ingestion_status": item.ingestion_status,
#         "notes": item.notes,
#         "created_at": item.created_at,
#     }


# def _get_papers_staging(db: Session, identifier: str) -> PapersStaging | None:
#     if identifier.isdigit():
#         return get_papers_staging_by_idx(db, idx=int(identifier))
#     try:
#         value = UUID(identifier)
#     except ValueError:
#         return None
#     return get_papers_staging_by_paper_id(db, paper_id=value)


# def approve_paper_staging(db: Session, idx: int) -> PapersStaging:
#     with db.begin_nested():
#         item = get_papers_staging_by_idx(db, idx=idx)
#         if item is None:
#             raise ValueError("Staging paper not found.")
#         if item.is_approved:
#             raise ValueError("Staging paper is already approved.")
#
#         paper_fields = {
#             "title": item.title,
#             "abstract": item.abstract,
#             "doi": item.doi,
#             "pmid": item.pmid,
#             "year_published": item.year_published,
#             "journal": item.journal,
#             "first_author": item.first_author,
#             "authors_display": item.authors_display,
#             "source_type": item.source_type,
#             "source_record_id": item.source_record_id,
#             "pdf_storage_path": item.pdf_storage_path,
#             "full_text_available": item.full_text_available,
#             "ocr_required": item.ocr_required,
#             "language": item.language,
#             "ingestion_status": item.ingestion_status,
#             "dedupe_key": item.dedupe_key,
#             "notes": item.notes,
#         }
#
#         if item.id is None:
#             paper = create_paper(db, **paper_fields)
#             paper_id = paper.id
#         else:
#             paper = get_paper_by_id(db, paper_id=item.id)
#             if paper is None:
#                 raise ValueError("Referenced paper not found.")
#             paper = update_paper_fields(db, item=paper, fields=paper_fields)
#             paper_id = paper.id
#
#         staging_fields = {
#             "is_approved": True,
#             "approval_timestamp": func.now(),
#         }
#         if item.id is None:
#             staging_fields["id"] = paper_id
#
#         return update_papers_staging_fields(db, item=item, fields=staging_fields)


# def update_paper_staging(
#     db: Session,
#     *,
#     identifier: str,
#     payload: str | dict,
# ) -> PapersStaging:
#     original = _get_papers_staging(db, identifier)
#     if original is None:
#         raise ValueError("Staging paper not found.")
#     if original.is_approved:
#         raise ValueError("Cannot edit an approved staging paper.")
#
#     cleaned = _normalize_edit_payload(_parse_payload(payload))
#     if not cleaned:
#         raise ValueError("No editable fields provided.")
#
#     with db.begin_nested():
#         edited_fields = {
#             "title": cleaned.get("title", original.title),
#             "abstract": cleaned.get("abstract", original.abstract),
#             "doi": cleaned.get("doi", original.doi),
#             "pmid": cleaned.get("pmid", original.pmid),
#             "year_published": cleaned.get("year_published", original.year_published),
#             "journal": cleaned.get("journal", original.journal),
#             "first_author": cleaned.get("first_author", original.first_author),
#             "authors_display": cleaned.get("authors_display", original.authors_display),
#             "source_type": cleaned.get("source_type", original.source_type),
#             "ingestion_status": cleaned.get("ingestion_status", original.ingestion_status),
#             "notes": cleaned.get("notes", original.notes),
#         }
#
#         if original.id is None:
#             paper = create_paper(db, **edited_fields)
#         else:
#             paper = get_paper_by_id(db, paper_id=original.id)
#             if paper is None:
#                 raise ValueError("Referenced paper not found.")
#             paper = update_paper_fields(db, item=paper, fields=edited_fields)
#
#         log_row = create_papers_staging(db, paper_id=paper.id, **edited_fields)
#         update_papers_staging_fields(
#             db, item=log_row, fields={"is_approved": True, "approval_timestamp": func.now()}
#         )
#         return update_papers_staging_fields(
#             db,
#             item=original,
#             fields={"id": paper.id, "is_approved": True, "approval_timestamp": func.now()},
#         )


def update_paper(
    db: Session,
    *,
    identifier: str,
    payload: str | dict,
) -> Papers:
    try:
        paper_id = UUID(identifier)
    except ValueError as exc:
        raise ValueError("Paper id must be a UUID.") from exc

    item = get_paper_by_id(db, paper_id=paper_id)
    if item is None:
        raise ValueError("Paper not found.")

    cleaned = _normalize_edit_payload(_parse_payload(payload))
    if not cleaned:
        raise ValueError("No editable fields provided.")

    return update_paper_fields(db, item=item, fields=cleaned)
