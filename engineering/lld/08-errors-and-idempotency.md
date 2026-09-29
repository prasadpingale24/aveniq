# LLD 08 — Errors and idempotency

## Problem Details (RFC 7807)

Media type: `application/problem+json`

### ProblemDetail schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | URI string | yes | Stable type URI under `https://aveniq.dev/problems/{code}` |
| `title` | string | yes | Short title |
| `status` | int | yes | HTTP status |
| `detail` | string | no | Specific message |
| `instance` | string | no | Request path or investigation id |
| `code` | string | yes | Machine code (snake_case) |
| `errors` | object[] | no | Field-level validation |

OpenAPI: `ProblemDetail` component.

## Error code catalog (Slice 0–1)

| code | HTTP | When |
|------|------|------|
| `validation_error` | 422 | Pydantic / request body invalid |
| `investigation_not_found` | 404 | Unknown `investigation_id` |
| `investigation_already_run` | 409 | Second `POST .../run` after terminal success state |
| `unsupported_benchmark` | 422 | `benchmark_id` not supported for run |
| `investigation_run_not_implemented` | 501 | Slice 0 stub for `/run` |
| `connector_fixture_not_found` | 500 | Missing fixture dir (maps to blocked investigation if mid-run) |
| `internal_error` | 500 | Unhandled exception (no stack in response) |

## POST /api/v1/investigations/{id}/run — idempotency

**Policy (chosen):** **Not idempotent** — second successful run path is rejected.

| Investigation state before run | Result |
|-------------------------------|--------|
| `initialized` | Run proceeds (Slice 1) |
| `context_gathering`, `investigating` | 409 `investigation_run_in_progress` (if concurrent run detected) OR 500 if stuck — Phase 0b single-threaded: unlikely |
| `rca_candidate`, `inconclusive`, `blocked` | **409** `investigation_already_run` |

Client should **GET** aggregate to retrieve prior result.

**Future:** `Idempotency-Key` header for create only (optional).

## Request correlation

| Header | Required | Description |
|--------|----------|-------------|
| `X-Request-Id` | no | Client-supplied; echoed in response header; logged and traced |

## Security-related (future)

| Header | Phase |
|--------|-------|
| `Authorization` | Documented in OpenAPI as optional; enforced later |

## Cross-references

- OpenAPI responses: [../api/openapi.yaml](../api/openapi.yaml)
- Use cases: [02-application-use-cases.md](02-application-use-cases.md)
