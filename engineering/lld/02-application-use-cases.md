# LLD 02 — Application use cases

All use cases live in `aveniq_application`. They depend on ports only, not adapters.

## StartInvestigation

### Command

| Field | Type | Required |
|-------|------|----------|
| `benchmark_id` | str | yes |
| `signal` | Signal | yes |
| `org_id` | str? | no |
| `environment_id` | str? | no |

### Behavior

1. Validate `benchmark_id` is supported (Slice 1: only `b03` for run; create may accept `b03` only or warn on others).
2. Generate `investigation_id` (ULID).
3. Persist `Investigation` with `state=initialized`, `run_count=0`.
4. Append event `investigation.created`.
5. Return aggregate (investigation + events; evidence/hypotheses/rca empty).

### Transaction boundary

Single SQLite transaction: insert investigation + first event.

### Errors

| Condition | Exception → HTTP |
|-----------|------------------|
| Unknown benchmark (if enforced) | `UnsupportedBenchmarkError` → 422 |
| DB failure | `PersistenceError` → 500 |

## RunInvestigation

### Command

| Field | Type | Required |
|-------|------|----------|
| `investigation_id` | str | yes |
| `request_id` | str? | tracing |

### Behavior

1. Load aggregate; **404** if missing.
2. If `state` in (`rca_candidate`, `inconclusive`, `blocked`) → `InvestigationAlreadyRunError` → **409**.
3. If `state` is `initialized` or mid-run (should not happen): proceed.
4. Set `context_gathering` → emit `investigation.state_changed`.
5. Delegate to `Investigator.run(investigation_id, ports, uow)`.
6. Investigator appends events/evidence/hypotheses/rca via `UnitOfWork`.
7. On success: `run_count += 1`, `run_completed_at = now`, terminal state.
8. Return full aggregate.

### Transaction boundary

**Option A (Phase 0b):** Investigator runs in one long transaction (simple, locks DB).  
**Option B (later):** Commit per playbook step for resumability.

**Chosen for 0b:** Option A — single transaction per run.

### Errors

See [08-errors-and-idempotency.md](08-errors-and-idempotency.md).

## GetInvestigation

### Query

`investigation_id: str`

### Behavior

Load aggregate or not found.

## UnitOfWork (application port)

```text
investigations: InvestigationRepository
evidence: EvidenceRepository
hypotheses: HypothesisRepository
rca: RcaRepository
events: InvestigationEventRepository
commit() / rollback()
```

Repositories defined in [03-ports.md](03-ports.md); SQLite impl in [04-persistence.md](04-persistence.md).

## Cross-references

- Sequences: [../hld/03-runtime-flows.md](../hld/03-runtime-flows.md)
- Investigator: [06-deterministic-investigator-b03.md](06-deterministic-investigator-b03.md)
