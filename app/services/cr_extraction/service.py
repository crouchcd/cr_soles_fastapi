from __future__ import annotations

from app.langgraph.multimodal_extraction import get_document_graph
from app.core.logger import set_log
from sqlalchemy.orm import Session


async def run_service(
    payload: dict | str,
    db: Session,
) -> dict:

    set_log("Processing extraction service")

    try:
        print("frame")
    finally:
        print("finally")

    graph = get_document_graph()

    state = {
        "payload": payload,
    }

    set_log("Invoking document graph")
    # invoke the graph
    result = await graph.ainvoke(state)

    # returning results postprocessing
    # bibliographic_info = result.get("bibliographic_info") or {}
    # missing_fields = result.get("missing_fields", [])

    # DB operations here
    # ...

    return {
        # "pages": pages,
        # "bibliographic_info": bibliographic_info,
        # "page_count": len(pages),
    }
