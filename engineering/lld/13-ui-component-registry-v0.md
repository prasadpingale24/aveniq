# LLD 13 — UI component registry v0

Pre–Generative UI catalog (ADR-006). Agents or layouts **select** from this set in Phase 3; Phase 1–2 **implement statically**.

Wire format for investigations: [api/openapi.yaml](../api/openapi.yaml) `InvestigationResponse`.

## Registry

| Component ID | Purpose | Primary OpenAPI / data source | Screens |
|--------------|---------|------------------------------|---------|
| `app-shell` | Top bar + nav + outlet | — | all |
| `persona-toggle` | ENG / LEAD / STAKEHOLDER | Client state → lld/09 | investigation |
| `playground-disclaimer` | Fixture vs stand-in boundary | Static copy + ADR-015 | scr-playground-01 |
| `playground-scenario-card` | Benchmark metadata | `PlaygroundScenarioSummary` | scr-playground-01 |
| `playground-runner-stepper` | Run phases | Playground run client state | scr-playground-01 |
| `signal-strip` | Alert / signal summary | `investigation.signal` | investigation |
| `investigation-state-header` | State machine badge | `investigation.state` | investigation |
| `timeline` | Incident window / events | `events`, `investigation.incident_window` | eng, lead |
| `evidence-card` | Single evidence item | `evidence[]` | eng (full), lead (top N) |
| `hypothesis-card` | Hypothesis + status | `hypotheses[]` | eng, lead (summary) |
| `rca-panel` | Status, root cause, summary | `rca` | all (filtered) |
| `rca-claim-row` | Claim + evidence ids | `rca.claims[]` | eng |
| `human-question-panel` | HITL prompt | future API | scr-hitl-06 |
| `states-empty` | Empty inbox | — | scr-states-07 |
| `states-loading` | Skeleton | — | scr-states-07 |
| `states-blocked` | Investigation blocked | `state=blocked` | scr-states-07 |
| `states-inconclusive` | RCA inconclusive | `rca.status` / `state` | scr-states-07 |
| `problem-banner` | API error | `ProblemDetail` | all |

## Evidence card (minimum fields)

From `Evidence` schema — engineer view shows all; lead shows `observation`, `strength`, `id`; stakeholder hidden.

| Field | Display |
|-------|---------|
| `id` | Mono chip |
| `observation` | Body |
| `source_type`, `strength` | Meta row |
| `provenance.fixture_path` | Optional mono subline |

## RCA claim row

| Field | Display |
|-------|---------|
| `text` | Claim text |
| `evidence_ids` | Linked mono tokens (navigate/highlight evidence) |

## Phase 3 note

GenUI may emit `{ "component": "evidence-card", "props": { "evidence_id": "..." } }` constrained to this registry; not implemented in Slice 3a–3c.

## Cross-references

- [lld/12-design-system-telemetry-monolith.md](12-design-system-telemetry-monolith.md)
- [07-application-surface.md](../07-application-surface.md)
- [docs/15-generative-ui.md](../../docs/15-generative-ui.md)
