# 03 — Slice 0 acceptance criteria

**Goal:** Prove repository skeleton, persistence, API contract, and observability hooks — **without** full B03 investigation logic.

## In scope

- uv workspace per [00-stack-and-repo.md](00-stack-and-repo.md)
- SQLite schema v1 applied on startup or via migration script
- Endpoints per [api/openapi.yaml](api/openapi.yaml):
  - `GET /health`
  - `POST /api/v1/investigations`
  - `GET /api/v1/investigations/{investigation_id}`
  - `POST /api/v1/investigations/{investigation_id}/run` → **501** or stub body with `code: not_implemented` (documented in OpenAPI)
- `investigation.created` event appended on create
- Structured logs with `investigation_id`, `request_id`
- OTEL: HTTP span + minimal resource attributes ([lld/07-observability.md](lld/07-observability.md))

## Out of scope

- Fixture connectors (Slice 1)
- Deterministic investigator (Slice 1)
- `ground_truth` or golden B03 test (Slice 1)

## Tests (Phase 0b)

| Test id | Description |
|---------|-------------|
| `test_health_returns_200` | Liveness |
| `test_create_investigation_201` | POST returns id, state `initialized` |
| `test_get_investigation_404` | Unknown id |
| `test_get_investigation_after_create` | Events include `investigation.created` |
| `test_run_returns_501_slice0` | Until Slice 1 flag enabled |
| `test_sqlite_repository_roundtrip` | Integration with temp db |
| `test_openapi_contract_paths_exist` | Contract smoke |

## Done when

- All Slice 0 tests green in CI
- OpenAPI served at `/openapi.json` matches committed [api/openapi.yaml](api/openapi.yaml) (contract test)

## Cross-references

- LLD use cases: [lld/02-application-use-cases.md](lld/02-application-use-cases.md)
- Slice 1: [04-slice-1-b03.md](04-slice-1-b03.md)
