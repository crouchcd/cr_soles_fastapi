from __future__ import annotations

import base64

import fitz  # PyMuPDF

from app.langgraph.multimodal_extraction import get_document_graph
from app.core.logger import set_log
from app.repositories.papers_staging_repository import create_papers_staging
from sqlalchemy.orm import Session


SUPPORTED_PDF_TYPES = {
    "application/pdf",
    "application/x-pdf",
    "application/acrobat",
    "applications/vnd.pdf",
    "text/pdf",
    "text/x-pdf",
}


def _ensure_supported_pdf(content_type: str | None) -> None:
    if not content_type or content_type not in SUPPORTED_PDF_TYPES:
        raise ValueError("Only PDF files are supported.")


async def run_service(
    pdf_bytes: bytes,
    ingestion_source: str,
    content_type: str | None,
    prompt: str,
    db: Session,
) -> dict:
    _ensure_supported_pdf(content_type)

    set_log("Processing document bytes")

    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    except Exception as exc:
        raise ValueError(f"Invalid PDF: {exc}") from exc

    page_images_b64: list[str] = []
    try:
        for page in doc:
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
            png_bytes = pix.tobytes("png")
            page_images_b64.append(base64.b64encode(png_bytes).decode("ascii"))
    finally:
        doc.close()

    if not page_images_b64:
        raise ValueError("PDF has no pages.")

    graph = get_document_graph()

    state = {
        "page_images_b64": page_images_b64,
        "prompt": prompt,
        "attempts": 0,
        "max_attempts": 1,
    }

    set_log("Invoking document graph")

    result = await graph.ainvoke(state)
    pages_content = result.get("ocr_pages", [])

    bibliographic_info = result.get("bibliographic_info") or {}
    missing_fields = result.get("missing_fields", [])

    title = bibliographic_info.get("title") or "Unknown title"
    abstract = bibliographic_info.get("abstract") or None
    doi = bibliographic_info.get("doi") or None
    pmid = bibliographic_info.get("pmid") or None
    year_published = bibliographic_info.get("year_published") or bibliographic_info.get("year")
    journal = bibliographic_info.get("journal") or None
    first_author = bibliographic_info.get("first_author") or None
    authors_display = bibliographic_info.get("authors_display") or None

    paper = create_papers_staging(
        db,
        title=title,
        abstract=abstract,
        doi=doi,
        pmid=pmid,
        year_published=year_published,
        journal=journal,
        first_author=first_author,
        authors_display=authors_display,
        source_type=ingestion_source,
        ingestion_status="queued",
    )

    return {
        "pages_content": pages_content,
        "bibliographic_info": bibliographic_info,
        "missing_fields": missing_fields,
        "page_count": len(pages_content),
        "paper_id": paper.id,
        "similar_documents": [],
    }
