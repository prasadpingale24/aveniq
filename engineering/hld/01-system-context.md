# HLD 01 — System context

Maps to product architecture [`docs/23-architecture.md`](../../docs/23-architecture.md).

## C4 Level 1 — Context

```mermaid
flowchart TB
  Engineer[Engineer]
  AVENIQ[AVENIQ_API]
  Fixtures[FixtureStore]
  FutureApp[StandInApp_future]
  FutureObs[ObservabilityStack_future]
  Eval[EvalHarness_tests_only]

  Engineer -->|"HTTPS REST"| AVENIQ
  AVENIQ -->|"read via connectors"| Fixtures
  AVENIQ -.->|"Slice 2+"| FutureApp
  AVENIQ -.->|"Phase 4+"| FutureObs
  Eval -->|"reads ground_truth"| Fixtures
  Eval -->|"asserts via API"| AVENIQ
```

## Actors

| Actor | Interaction |
|-------|-------------|
| **Engineer** | Creates investigations, triggers run, inspects evidence and RCA via API (UI later). |
| **CI / Jenkins** | Runs pytest, contract tests; optional smoke against staging API. |

## External systems (Phase 0b–1)

| System | Role | Phase |
|--------|------|-------|
| **Fixture store** | Versioned files under `fixtures/{benchmark_id}/` produced by `scripts/build_fixture.py` | 0b–1 |
| **Ground truth** | `fixtures/{id}/ground_truth.json` — **eval only** | 0b–1 |

## External systems (deferred)

| System | Role | Phase |
|--------|------|-------|
| **Stand-in checkout stack** | Runnable app emitting logs/metrics | Slice 2 |
| **Prometheus / Loki / Grafana** | Live telemetry and alerts | Phase 4+ |
| **Harbor** | Container registry | Deploy handoff |
| **MCP servers** | Tool exposure to agents | After E2E without MCP |

## Trust boundaries

- AVENIQ treats all connector payloads as **untrusted data** (prompt injection discipline per [`docs/19-security.md`](../../docs/19-security.md)).
- Authorization is **out of scope** for Slice 0–1; `org_id` / `environment_id` are optional fields for future tenancy.

## Cross-references

- Data flows: [04-data-flows.md](04-data-flows.md)
- Containers: [02-containers.md](02-containers.md)
