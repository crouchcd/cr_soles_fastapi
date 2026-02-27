from __future__ import annotations

from typing import Any, Sequence

from sqlalchemy import select, literal
from sqlalchemy.orm import Session

from app.models.papers import Papers


def find_similar_papers(
    db: Session,
    *,
    embedding: Sequence[float],
    limit: int = 10,
    min_similarity: float | None = None,
) -> list[dict[str, Any]]:
    # 핵심: embedding을 문자열로 만들지 말고, "그대로" 바인딩
    embedding_vector = list(map(float, embedding))
    distance = Papers.embedding.cosine_distance(embedding_vector)
    similarity = (literal(1.0) - distance).label("similarity")

    query = (
        select(
            Papers.id,
            Papers.title,
            Papers.authors,
            Papers.journal,
            Papers.year,
            Papers.abstract,
            Papers.pdf_url,
            Papers.ingestion_source,
            Papers.ingestion_timestamp,
            similarity,
        )
        .where(Papers.embedding.isnot(None))
        .order_by(distance)
        .limit(int(limit))
    )

    if min_similarity is not None:
        query = query.where(similarity >= float(min_similarity))

    result = db.execute(query)
    return [dict(row) for row in result.mappings().all()]


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
    authors: list[str] | None = None,
    journal: str | None = None,
    year: int | None = None,
    abstract: str | None = None,
    pdf_url: str | None = None,
    ingestion_source: str | None = None,
    embedding: list[float] | None = None,
) -> Papers:
    paper = Papers(
        title=title,
        authors=authors or [],
        journal=journal,
        year=year,
        abstract=abstract,
        pdf_url=pdf_url,
        ingestion_source=ingestion_source,
        embedding=embedding,
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
