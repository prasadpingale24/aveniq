# AVENIQ — Engineering documentation

Implementation design for AVENIQ. Product intent lives in [`../docs/`](../docs/); this tree is the **build contract** for Phase 0b onward.

## Status

| Phase | Scope | Status |
|-------|--------|--------|
| **0a** | HLD, LLD, OpenAPI, supporting specs, ADRs | Complete |
| **0b** | `packages/` code, fixtures, tests | Complete (Slices 0–1) |

## Document map

### Supporting specifications

| Doc | Description |
|-----|-------------|
| [00-stack-and-repo.md](00-stack-and-repo.md) | Python, uv workspace, package boundaries |
| [01-fixture-package-spec-v1.md](01-fixture-package-spec-v1.md) | Benchmark fixture file layout and schemas |
| [02-investigation-event-catalog.md](02-investigation-event-catalog.md) | Append-only investigation event types |
| [03-slice-0.md](03-slice-0.md) | Slice 0 acceptance criteria |
| [04-slice-1-b03.md](04-slice-1-b03.md) | Slice 1 B03 acceptance and golden expectations |
| [05-local-vs-staging.md](05-local-vs-staging.md) | Local dev vs VPS staging isolation |

### High-level design (HLD)

| Doc | Description |
|-----|-------------|
| [hld/01-system-context.md](hld/01-system-context.md) | C4 context |
| [hld/02-containers.md](hld/02-containers.md) | Runtime containers and packages |
| [hld/03-runtime-flows.md](hld/03-runtime-flows.md) | Sequence diagrams |
| [hld/04-data-flows.md](hld/04-data-flows.md) | Evidence normalization and ground-truth isolation |
| [hld/05-deployment-evolution.md](hld/05-deployment-evolution.md) | Local → CI → VPS |

### Low-level design (LLD)

| Doc | Description |
|-----|-------------|
| [lld/01-domain-model.md](lld/01-domain-model.md) | Entities, enums, state machine |
| [lld/02-application-use-cases.md](lld/02-application-use-cases.md) | Use cases and transactions |
| [lld/03-ports.md](lld/03-ports.md) | Port interfaces |
| [lld/04-persistence.md](lld/04-persistence.md) | SQLite DDL and repositories |
| [lld/05-fixture-connectors.md](lld/05-fixture-connectors.md) | Fixture connector behavior |
| [lld/06-deterministic-investigator-b03.md](lld/06-deterministic-investigator-b03.md) | B03 playbook |
| [lld/07-observability.md](lld/07-observability.md) | Logs, traces, metrics |
| [lld/08-errors-and-idempotency.md](lld/08-errors-and-idempotency.md) | Error model and idempotency |

### API contract

| Artifact | Description |
|----------|-------------|
| [api/openapi.yaml](api/openapi.yaml) | **Source of truth** for HTTP API v1 |
| [api/README.md](api/README.md) | Validation and contract-test workflow |

### Architecture decision records (implementation)

| ADR | Topic |
|-----|--------|
| [adrs/011-python-uv-workspace.md](adrs/011-python-uv-workspace.md) | Language and monorepo layout |
| [adrs/012-sqlite-persistence.md](adrs/012-sqlite-persistence.md) | SQLite for Phase 0b–1 |
| [adrs/013-fixture-format-v1.md](adrs/013-fixture-format-v1.md) | Fixture package v1 |
| [adrs/014-deterministic-investigator-v1.md](adrs/014-deterministic-investigator-v1.md) | B03 playbook investigator |

Product ADRs remain in [`../docs/26-decisions.md`](../docs/26-decisions.md).

## Design gate

Before Phase 0b implementation, complete the checklist in [DESIGN_GATE.md](DESIGN_GATE.md).
