from functools import lru_cache

from langgraph.graph import END, StateGraph

from app.langgraph.cr_extraction.nodes.bibliographic_info_node import (
    extract_bibliographic_info,
    prepare_retry,
    should_retry,
)
from app.langgraph.cr_extraction.nodes.ocr_node import run_ocr
from app.langgraph.cr_extraction.state import CrExtractionState


def build_cr_extraction_graph():
    graph = StateGraph(CrExtractionState)
    graph.add_node("ocr", run_ocr)

    graph.add_edge("embed", END)
    return graph.compile()


@lru_cache(maxsize=1)
def get_cr_extraction_graph():
    return build_cr_extraction_graph()
