# 00 — Stack and repository

## Decision summary

See [adrs/011-python-uv-workspace.md](adrs/011-python-uv-workspace.md).

| Choice | Value |
|--------|--------|
| Language | Python 3.12+ |
| Package manager | [uv](https://docs.astral.sh/uv/) workspaces |
| API framework | FastAPI (Phase 0b) |
| Validation | Pydantic v2 |
| Persistence | SQLite via repository port (see [adrs/012-sqlite-persistence.md](adrs/012-sqlite-persistence.md)) |
| HTTP contract | OpenAPI 3.1 — [api/openapi.yaml](api/openapi.yaml) |

## Rationale (project context)

Phase 0b–1 work is **schema-heavy**, **script-generated benchmarks**, and **deterministic investigation** without LLM. Python fits fixture tooling, evaluation, and rapid iteration for a solo builder. TypeScript is deferred to a future **presentation** package when GenUI is validated (product ADR-005).

Go is excluded: no local toolchain requirement; Docker-only Go adds ops cost without Phase 1 benefit.

## Repository layout (target Phase 0b)

```text
aveniq/
  pyproject.toml              # uv workspace root
  packages/
    aveniq_domain/
    aveniq_application/
    aveniq_adapters/
    aveniq_api/
  engineering/                # this tree
  scenarios/
  scripts/
  fixtures/
  tests/
  compose/
  .env.example
```

Package names use `aveniq_*` to avoid import clashes with common module names (`domain`, `api`).

## Dependency rule (hexagonal)

```text
aveniq_domain          # no I/O
    ↑
aveniq_application     # use cases + port Protocols
    ↑
aveniq_adapters        # sqlite, fixtures, otel
    ↑
aveniq_api             # FastAPI, DI wiring only
```

Forbidden:

- SQL or HTTP imports in `aveniq_domain`
- Business rules in route handlers (handlers call use cases only)

## Tooling (Phase 0b)

| Tool | Purpose |
|------|---------|
| `uv sync` | Install workspace |
| `pytest` | unit, integration, golden, contract |
| `ruff` | lint |
| `httpx` | API tests |

## Cross-references

- Containers: [hld/02-containers.md](hld/02-containers.md)
- Ports: [lld/03-ports.md](lld/03-ports.md)
- Local vs staging: [05-local-vs-staging.md](05-local-vs-staging.md)
