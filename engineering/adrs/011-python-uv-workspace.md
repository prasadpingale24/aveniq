# ADR-011 — Python 3.12+ and uv workspace

| | |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-09-28 |

## Context

AVENIQ Phase 0b–1 requires schema-heavy domain modeling, script-generated fixtures, deterministic investigation, and pytest evaluation. The builder is solo; TypeScript UI and Go are deferred.

## Decision

- **Language:** Python 3.12+
- **Packaging:** uv workspace with packages `aveniq_domain`, `aveniq_application`, `aveniq_adapters`, `aveniq_api`
- **API:** FastAPI; schemas aligned with [api/openapi.yaml](../api/openapi.yaml)

## Alternatives considered

| Option | Rejected because |
|--------|------------------|
| TypeScript monolith | Fixture/eval scripts and Phase 1 focus are backend-heavy; UI deferred |
| Go | No local toolchain; learning cost without Phase 1 benefit |
| Single flat package | Violates hexagonal boundaries and future extractability |

## Consequences

- Positive: Fast iteration, Pydantic alignment with evidence model, strong pytest story
- Negative: Future GenUI likely adds a TypeScript frontend package
- Revisit when: GenUI phase starts or performance requires native extensions

## References

- [00-stack-and-repo.md](../00-stack-and-repo.md)
- Product ADR-001 evidence-first in [docs/26-decisions.md](../../docs/26-decisions.md)
