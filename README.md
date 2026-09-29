# AVENIQ

**Evidence-first incident investigation** — an experimental system that explores whether structured, inspectable investigations can reduce the manual work of connecting alerts, logs, metrics, and changes into a trustworthy root-cause analysis.

> Make production incident investigation evidence-driven, contextual, and easier to navigate.  
> See [product vision](docs/03-product-vision.md).

## The problem

Production incidents are rarely explained by a single dashboard or log line. Engineers reconstruct what happened by correlating fragmented signals across tools. The hard part is not finding telemetry — it is **building a coherent story** and **showing which observations support each conclusion**.

AVENIQ tests a different emphasis: **evidence before confidence**. Conclusions should cite what was observed, where it came from, and how it relates to hypotheses — so humans can challenge the reasoning, not just the headline.

- Problem framing: [docs/01-problem.md](docs/01-problem.md)  
- Goals and boundaries: [docs/04-goals-and-non-goals.md](docs/04-goals-and-non-goals.md)

## How it works (conceptually)

```text
Signal (e.g. alert)
  → Investigation
  → Evidence from telemetry / change sources
  → Hypotheses
  → RCA candidate (claims linked to evidence)
```

Core ideas: [investigation model](docs/09-investigation-model.md), [evidence model](docs/10-evidence-model.md), [glossary](docs/08-core-concepts.md).

## What is in this repository

| Area | Path | Contents |
|------|------|----------|
| Product & roadmap | [`docs/`](docs/) | Vision, MVP, architecture narrative, benchmark incidents, roadmap |
| Engineering design | [`engineering/`](engineering/) | HLD/LLD, OpenAPI contract, ADRs, slice acceptance criteria |
| Application code | [`packages/`](packages/) | `aveniq_domain`, `aveniq_application`, `aveniq_adapters`, `aveniq_api` |
| Scenarios & fixtures | [`scenarios/`](scenarios/), [`fixtures/`](fixtures/) | Reproducible benchmark data (e.g. B03 checkout / DB pool exhaustion) |
| Compose (planned) | [`compose/`](compose/) | Docker Compose for local stack and staging (Slice 2+) |

## What works today

The current implementation is a **Phase 0b** vertical slice: a Python API that persists investigations in SQLite, reads **fixture-based** telemetry (no live observability backends yet), and runs a **deterministic** playbook for benchmark **B03**. There is no web UI, no LLM agent, and no MCP integrations — those are intentional later phases ([roadmap](docs/25-roadmap.md)).

| Capability | Status |
|------------|--------|
| HTTP API (`/api/v1/investigations`, run, health) | Available |
| Evidence-backed RCA for B03 | Available (deterministic investigator) |
| OpenAPI / Swagger UI | Available at `/docs` when the API is running |
| Docker Compose + stand-in app | Planned (engineering Slice 2) |
| Investigation UI | Planned (product Phase 1) |
| Agentic / LLM investigation | Later (Phase 2+) |

Implementation status detail: [engineering/README.md](engineering/README.md).

## Try it locally

**Prerequisites:** Python 3.12+, [uv](https://github.com/astral-sh/uv).

```bash
uv sync --all-packages
uv run python scripts/build_fixture.py
uv run pytest
uv run aveniq-api
```

Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for interactive API documentation. The root URL `/` is not defined; use `/health` or the API routes below.

**Example — B03** (database connection exhaustion on `checkout-api`; see [benchmark incidents](docs/21-benchmark-incidents.md)):

```bash
curl -s -X POST http://127.0.0.1:8000/api/v1/investigations \
  -H "Content-Type: application/json" \
  -d '{"benchmark_id":"b03","signal":{"kind":"alert","fired_at":"2026-09-28T14:36:00Z","service":"checkout-api","description":"checkout-api error rate high"}}'

curl -s -X POST http://127.0.0.1:8000/api/v1/investigations/<id>/run
curl -s http://127.0.0.1:8000/api/v1/investigations/<id>
```

## API contract

OpenAPI 3.1 source of truth: [`engineering/api/openapi.yaml`](engineering/api/openapi.yaml).

## For contributors

- Architecture and build contract: [`engineering/README.md`](engineering/README.md)  
- Design gate (before large implementation changes): [`engineering/DESIGN_GATE.md`](engineering/DESIGN_GATE.md)  
- Product decisions: [`docs/26-decisions.md`](docs/26-decisions.md)

## Status

Experimental research codebase — not production-ready. No license file is published yet; treat usage accordingly until one is added.
