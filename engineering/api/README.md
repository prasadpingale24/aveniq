# HTTP API contract

## Source of truth

[`openapi.yaml`](openapi.yaml) is the **authoritative** contract for AVENIQ HTTP API v1.

Implementation rule (Phase 0b):

1. FastAPI routes and Pydantic models must conform to this file.
2. Served schema at `/openapi.json` must match committed `openapi.yaml` (contract test).
3. Semantic behavior is defined in [`../lld/`](../lld/) and product [`../../docs/`](../../docs/).

## Validation (local)

```bash
# Option A: Redocly CLI
npx --yes @redocly/cli lint engineering/api/openapi.yaml

# Option B: Python (Phase 0b dev dependency)
uv run openapi-spec-validator engineering/api/openapi.yaml
```

## Contract tests (Phase 0b)

Location: `tests/contract/`

| Test | Purpose |
|------|---------|
| `test_openapi_file_is_valid` | Parse YAML |
| `test_app_openapi_matches_committed` | Diff `/openapi.json` to `engineering/api/openapi.yaml` |
| `test_examples_validate_against_schema` | B03 examples in spec are consistent |

Optional: `schemathesis` against running app using this spec.

## Versioning

- Base path: `/api/v1`
- Breaking changes require `/api/v2` or explicit deprecation policy (document when introduced).

## Error responses

All documented error statuses return `application/problem+json` (`ProblemDetail`).

See [`../lld/08-errors-and-idempotency.md`](../lld/08-errors-and-idempotency.md).
