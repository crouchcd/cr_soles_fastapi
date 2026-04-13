# cr_soles_fastapi — Onboarding Guide

## What this project does (30-second version)

A FastAPI service that ingests research PDFs and extracts structured metadata about **cognitive reserve (CR) studies** using VLM-based OCR + LangGraph pipelines. Data lands in a Supabase (Postgres) database for human review. Two pipelines: (1) **multimodal_extraction** — PDF → OCR → bibliographic info; (2) **cr_extraction** — OCR text → population/instrument/operationalization extraction with validation loops. A third surface — **paper_review** — exposes a staging/approval queue.

## Quickstart

```bash
# Python 3.14 required
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync
uv pip install -r requirements.txt

# Set env vars (see app/core/config.py)
#   SUPABASE_DB_URL, VLLM_BASE_URL, VLLM_PORT, VLLM_MODEL,
#   EMBEDDING_BASE_URL, EMBEDDING_PORT, EMBEDDING_MODEL, EMBEDDING_DIMENSION
#   APP_NAME, API_PREFIX, APP_ENV

uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
# or: docker compose up
```

VLM serving (vLLM) is expected on a remote GPU (Runpod/vast.ai, A40+). See README §"VLLM Model Serving" — Qwen3-VL-8B-Instruct on port 8000, Qwen3-Embedding-0.6B on port 8008.

## Layered architecture

```
router  →  service  →  langgraph (graph+nodes)  →  vllm/embedding client
                   ↘   repository  →  SQLAlchemy model  →  Supabase Postgres
```

- **app/main.py** — mounts 3 routers under `settings.api_prefix`, CORS locked to localhost:3000 + cr-soles.cloud + Vercel.
- **app/core/config.py** — Pydantic `BaseSettings` from `.env`; `app.core.db` builds the SQLAlchemy engine + `SessionLocal` with rollback-on-error.

## The three API surfaces

### 1. Multimodal extraction — `POST /multimodal_extraction/extract`
- Multipart: `pdf` (UploadFile), `ingestion_source`, `prompt`.
- `services/multimodal_extraction.py` validates MIME, renders pages to base64 PNG via PyMuPDF, runs the `multimodal_extraction` LangGraph (`ainvoke`), writes a `Paper` row.
- **Graph**: `ocr_node` → `extract_bibliographic_info` → `should_retry?` → loop back through `prepare_retry` until `REQUIRED_FIELDS` are filled or `max_attempts` hit. (`embed_data` node exists but is commented out in `graph.py:20`.)
- **Client**: `VllmClient.stream_chat`/`chat` → vLLM `/v1/chat/completions`, 300s timeout, OpenAI-compatible.

### 2. CR extraction — `POST /cr_extraction/extract/stream`
- JSON body: `paper_id` **or** `pages_content`, optional `stream_prompt`. Returns **Server-Sent Events**.
- `services/cr_extraction.py` resolves `pages_content` from the DB if only `paper_id` is given, then streams the graph via `astream(["updates","custom"])`, emitting `event: chunk` / `event: done` with population + cr_operationalization + normalized_row.
- **Graph**: `population_node` → `validation_node` (validates population) → conditional: if `cr_operationalization` already present → `reduce_node`; else `instrument_node` → `validation_node` (validates instrument) → `reduce_node`.
- Nodes stream `VllmTaskType.CR_EXTRACTION` with prompts from `app/prompts/cr_extraction.py` and collect text via `stream_node_llm_and_collect`.

### 3. Paper review — `paper_review_route.py`
- `GET /paper_review/fetch/papers` — paginated (`offset`, `limit`, `table_type`=PAPERS_STAGING by default). Uses a row-number window to return the latest unapproved staging row per paper.
- `POST /paper_review/update/paper?id=…` — whitelisted field update (title, abstract, doi, pmid, year_published, journal, first_author, authors_display, source_type, ingestion_status, notes).

## Data model (key tables)

- **papers** — canonical record (UUID PK, doi unique, year check 1800–2100, `ingestion_status` enum, relationships to extractions/pipeline_runs/paper_files/staging_items).
- **papers_staging** — approval queue; mirrors paper columns plus `is_approved`/`approval_timestamp`. FK back to `papers`.
- **extractions** — the structured research payload: brain/cognition/moderator measures, sample size, study design, confidence, `human_review_status`. Versioned via `extraction_version` + `is_current`.
- **extraction_evidence** — per-field provenance (page, section, char offsets, confidence) — this is how you trace any extracted field back to the PDF.
- **pipeline_runs** + **pipeline_steps** — one row per graph execution; steps capture model, prompt version, tokens, cost, metrics. This is your audit/observability layer.
- **evaluations** — human/LLM quality scoring of extractions.
- **profiles** — Supabase auth mirror.

**pgvector note**: the `vector` extension is declared in `db_creation.sql`, but no pgvector columns exist in the current `public` models. `embedding_node` in the multimodal graph is wired but commented out — embeddings are not yet persisted.

## Repositories

Plain module-level functions (not classes): `create_*`, `get_*_by_id`, `list_*(offset, limit)`, `update_*_fields` (generic `setattr`). `papers_staging_repository` has the most real logic — row_number windowing to find the newest unapproved row per paper.

## Migrations — caveat

`alembic/env.py` is configured (filter: `public` schema only), but **there is no `alembic/versions/` directory checked in**. Schema is effectively tracked via `db_creation.sql` and the SQLAlchemy models. If you need to change the schema, expect to write the first real migration yourself.

## Where to start reading (in order)

1. `app/main.py` — wiring.
2. `app/core/config.py` + `app/core/db.py` — what env vars you need.
3. `app/routers/cr_extraction_route.py` → `app/services/cr_extraction.py` → `app/langgraph/cr_extraction/graph.py` — the most interesting path.
4. `app/langgraph/cr_extraction/nodes/*.py` and `app/prompts/cr_extraction.py` — the actual extraction logic.
5. `app/models/papers.py` + `extractions.py` + `extraction_evidence.py` — the output shape.

## Gotchas to know up front

- **Python 3.14** is hard-required (`pyproject.toml`). Not 3.12/3.13.
- **vLLM must be reachable** — no local fallback. Without a GPU box serving Qwen3-VL-8B, the pipelines won't run. Ollama client exists but is unused (commented out in config).
- **No alembic versions in git** — don't assume `alembic upgrade head` does anything.
- **Embedding node is wired but disabled** in the multimodal graph.
- **SSE response** on `/cr_extraction/extract/stream` — use an SSE client, not plain JSON consumer.
- **Docs disabled in prod** when `APP_ENV` is `prod`/`production`.
