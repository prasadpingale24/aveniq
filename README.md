# AVENIQ

Evidence-first incident investigation (experimental). Product documentation: [`docs/`](docs/).

## Engineering status

| Phase | Description | Status |
|-------|-------------|--------|
| **0a** | HLD, LLD, OpenAPI, design gate | Complete — see [`engineering/`](engineering/) |
| **0b** | Python implementation (Slices 0–1) | **Implemented** |

## Quick start (Phase 0b)

```bash
uv sync --all-packages
uv run python scripts/build_fixture.py
uv run pytest
uv run aveniq-api
```

Create and run a B03 investigation:

```bash
curl -s -X POST http://127.0.0.1:8000/api/v1/investigations \
  -H "Content-Type: application/json" \
  -d '{"benchmark_id":"b03","signal":{"kind":"alert","fired_at":"2026-09-28T14:36:00Z","service":"checkout-api","description":"checkout-api error rate high"}}'

curl -s -X POST http://127.0.0.1:8000/api/v1/investigations/<id>/run
curl -s http://127.0.0.1:8000/api/v1/investigations/<id>
```

Start here: [`engineering/README.md`](engineering/README.md)  
Before coding: complete [`engineering/DESIGN_GATE.md`](engineering/DESIGN_GATE.md).

## API contract

OpenAPI 3.1: [`engineering/api/openapi.yaml`](engineering/api/openapi.yaml)
