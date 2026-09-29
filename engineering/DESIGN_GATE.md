# Design gate — Phase 0a → 0b

Review this checklist before allowing `packages/` implementation.

## Contract and API

- [ ] `[api/openapi.yaml](api/openapi.yaml)` validates with OpenAPI 3.1 parser (e.g. `npx @redocly/cli lint api/openapi.yaml` or equivalent).
- [ ] Every Slice 0–1 endpoint has request/response schemas, documented errors, and at least one example where applicable.
- [ ] B03 `create` + `get after run` examples are internally consistent (IDs, timestamps, evidence refs).
- [ ] `/api/v1` prefix used; health may remain unversioned at `/health`.

## Domain and state

- [ ] Investigation state machine in `[lld/01-domain-model.md](lld/01-domain-model.md)` has no unreachable states required for Slice 0–1.
- [ ] Terminal states (`rca_candidate`, `inconclusive`, `blocked`) documented with entry conditions.
- [ ] RCA `status` enum aligns with `[docs/11-rca-model.md](../docs/11-rca-model.md)`.



## Persistence

- [ ] DDL in `[lld/04-persistence.md](lld/04-persistence.md)` supports append-only events and full aggregate read.
- [ ] Migration strategy v1 (single SQL file + `schema_migrations` table) documented.



## Investigation loop

- [ ] Event types in `[02-investigation-event-catalog.md](02-investigation-event-catalog.md)` cover B03 playbook steps in `[lld/06-deterministic-investigator-b03.md](lld/06-deterministic-investigator-b03.md)`.
- [ ] Each playbook step emits at least one catalogued event.



## Ground truth isolation

- [ ] `[hld/04-data-flows.md](hld/04-data-flows.md)` and `[lld/05-fixture-connectors.md](lld/05-fixture-connectors.md)` state: runtime never reads `ground_truth.json`.
- [ ] Eval/golden tests are the only consumers of ground truth.



## Traceability

- [ ] Path documented: RCA claim → `evidence_ids` → Evidence record → fixture source record (see `[lld/06](lld/06-deterministic-investigator-b03.md)` § Evidence ID assignment).



## Observability

- [ ] Required log fields and span names listed in `[lld/07-observability.md](lld/07-observability.md)`.



## Errors and idempotency

- [ ] `POST .../run` behavior on second call documented in `[lld/08-errors-and-idempotency.md](lld/08-errors-and-idempotency.md)`.



## Sign-off


| Role  | Name           | Date       | Notes    |
| ----- | -------------- | ---------- | -------- |
| Owner | Prasad Pingale | 29-09-2026 | Verified |


When all items are checked, proceed to **Phase 0b** per `[README.md](README.md)`.