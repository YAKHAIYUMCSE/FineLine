# FineLine: Design

FineLine gives the traffic rule and fine that applied on the date of an offence, with citations.
This file describes what is built so far (Week 2) and what is planned (Week 3 onward).

## Architecture (Week 2)

    client -> FastAPI app -> LLM provider (main model, optional fallback model)
                          -> cost log (logs/cost.jsonl)
              FastAPI app -> Postgres + pgvector (checked by /ready; used for search from Week 3)

Everything runs with `docker compose up --build`: an `api` container and a `db` container
(`pgvector/pgvector:pg16`) on one network. The API reaches the database by the name `db`.

## API endpoints

| Method | Path | Purpose | Response |
|---|---|---|---|
| GET | /health | Liveness: the process is up. Touches nothing. | `{"status":"ok","app":...,"environment":...}` |
| GET | /ready | Readiness: runs `SELECT 1` on Postgres (3 s timeout). | 200 `{"status":"ready","database":"ok"}`, 200 `"not configured"` when no database URL, 503 `"not ready"` when the database is unreachable |
| POST | /chat | Sends messages to the LLM and streams the answer as Server-Sent Events. | `data:` events with `{"delta": ...}`, then `event: done` with token usage and cost. A failure becomes `event: error`, not a 500. |
| GET | /usage | Calls, tokens and cost per day (UTC), read from `logs/cost.jsonl`. | `{"2026-11-01": {"calls":1,"input_tokens":2,"output_tokens":13,"cost_usd":0}}` |

`POST /chat` request body: `{"messages": [{"role": "user", "content": "..."}], "temperature": 0.2}`.

## LLM reliability

- One provider interface (`app/llm/base.py`); the app never names a provider. `LLM_PROVIDER` in `.env` picks `fake` (tests, no key) or `openai_compat` (any OpenAI-compatible endpoint).
- Timeout per call, and retries with exponential backoff and full jitter on timeouts, HTTP 429 and 5xx.
- 400, 401, 403 and 404 are never retried: retrying cannot fix them.
- No retry after text has already been streamed, so an answer is never duplicated.
- Fallback model (`LLM_FALLBACK_MODEL`): used only when the main model is unavailable after every retry and nothing has been streamed yet. A wrong key or model name is never hidden by the fallback.
- Every call writes one JSON line to `logs/cost.jsonl` with model, tokens, latency, cost, `ok` and `fallback_used`. If the provider does not report usage, tokens are estimated and marked `usage_estimated`.

## Data and tables

Source documents are collected into `data/raw/` (not in Git); every file is logged in `data/manifest.csv`
and `DATASET.md`.

**Planned for Week 3 (Postgres + pgvector, not built yet):**

| Table | Key columns | Purpose |
|---|---|---|
| documents | id, title, source_url, published_on | One row per downloaded file |
| section_versions | id, document_id, section_no, text, valid_from, valid_to, amending_act | Each section stored as dated versions, so a question can be answered for the date of the offence |
| chunks | id, section_version_id, page, text, embedding (vector) | Retrieval units with page-level citations |

Core rule (the hardest problem): a section version applies on date D when
`valid_from <= D AND (valid_to IS NULL OR valid_to > D)`. The retriever filters by this before searching.

## Configuration and secrets

Settings come from environment variables (`.env` locally, git-ignored and docker-ignored; the host's
settings in production). API keys are never committed and never baked into the Docker image.