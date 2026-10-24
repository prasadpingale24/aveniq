# AVENIQ — Engineering documentation

Implementation design for AVENIQ. Product intent lives in [`../docs/`](../docs/); this tree is the **build contract** for Phase 0b onward.

**What to build next:** [00-delivery-spine.md](00-delivery-spine.md) · [../docs/31-delivery-spine.md](../docs/31-delivery-spine.md) (ADR-021).

## Milestone status

| Milestone | Scope | Status |
|-----------|--------|--------|
| **M0** | Domain, B03, fixtures, tests | Done (legacy slices 0–1) |
| **M1** | Compose, Playground, stand-in, minimal web | Done — [06-slice-2-playground-compose.md](06-slice-2-playground-compose.md) |
| **M2** | Application shell (tokens, nav, routes) | Done — [08-slice-3a-design-foundation.md](08-slice-3a-design-foundation.md) |
| **M3** | Dev session & identity | Done — [11-milestone-m3-dev-session.md](11-milestone-m3-dev-session.md) |
| **M4** | Playground E2E | **Done** — [09-milestone-m4-playground-ui.md](09-milestone-m4-playground-ui.md) |
| **M5** | Investigation workspace E2E | **Done** — [10-milestone-m5-investigation-ui.md](10-milestone-m5-investigation-ui.md) |
| **M6** | Incidents inbox | **Done** — [12-milestone-m6-incidents-inbox.md](12-milestone-m6-incidents-inbox.md) |
| **M7–M8** | Staging, HITL | Planned — see spine |

## Document map

### Supporting specifications

| Doc | Description |
|-----|-------------|
| [00-delivery-spine.md](00-delivery-spine.md) | Journey milestones (execution order) |
| [00-stack-and-repo.md](00-stack-and-repo.md) | Python, uv workspace, package boundaries |
| [01-fixture-package-spec-v1.md](01-fixture-package-spec-v1.md) | Benchmark fixture file layout and schemas |
| [02-investigation-event-catalog.md](02-investigation-event-catalog.md) | Append-only investigation event types |
| [03-slice-0.md](03-slice-0.md) | Slice 0 acceptance criteria |
| [04-slice-1-b03.md](04-slice-1-b03.md) | Slice 1 B03 acceptance and golden expectations |
| [06-slice-2-playground-compose.md](06-slice-2-playground-compose.md) | Slice 2 Playground, Compose, persona foundation |
| [07-application-surface.md](07-application-surface.md) | Screens, routes, journeys, Stitch mapping |
| [08-slice-3a-design-foundation.md](08-slice-3a-design-foundation.md) | Slice 3a UI tokens and app shell |
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
| [lld/09-presentation-profiles.md](lld/09-presentation-profiles.md) | Persona presentation profiles (UI) |
| [lld/10-playground-orchestration.md](lld/10-playground-orchestration.md) | Playground scenario driver |
| [lld/12-design-system-telemetry-monolith.md](lld/12-design-system-telemetry-monolith.md) | UI design tokens and rules (Telemetry Monolith) |
| [lld/13-ui-component-registry-v0.md](lld/13-ui-component-registry-v0.md) | Component catalog v0 (pre-GenUI) |

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
| [adrs/015-slice-2-compose-and-playground.md](adrs/015-slice-2-compose-and-playground.md) | Compose naming, Playground, presentation shell |
| [adrs/016-product-surface-and-ui-phasing.md](adrs/016-product-surface-and-ui-phasing.md) | Product surface, UI slices, identity phasing |
| [adrs/017-investigation-tenancy-and-isolation.md](adrs/017-investigation-tenancy-and-isolation.md) | Org-primary investigation isolation |
| [adrs/018-actor-attribution.md](adrs/018-actor-attribution.md) | Actor on mutating investigation events |
| [adrs/019-presentation-profile-not-authorization.md](adrs/019-presentation-profile-not-authorization.md) | UI profile vs RBAC |
| [adrs/021-delivery-spine-authority.md](adrs/021-delivery-spine-authority.md) | Journey milestones supersede phase/slice build order |
| [adrs/022-dev-session-m3.md](adrs/022-dev-session-m3.md) | Dev login + session cookie (M3) |

Product ADRs remain in [`../docs/26-decisions.md`](../docs/26-decisions.md). UI program: [`../docs/29-ui-program.md`](../docs/29-ui-program.md). Identity Q&A log: [`../docs/30-identity-access-decisions.md`](../docs/30-identity-access-decisions.md).

## Design gate

Before Phase 0b implementation, complete the checklist in [DESIGN_GATE.md](DESIGN_GATE.md).
