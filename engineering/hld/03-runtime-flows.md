# HLD 03 — Runtime flows

Aligns with [`docs/09-investigation-model.md`](../../docs/09-investigation-model.md).

## Flow 1 — Create investigation

```mermaid
sequenceDiagram
  participant Client
  participant API
  participant StartUC as StartInvestigation
  participant Repo as InvestigationRepository
  participant DB as SQLite

  Client->>API: POST /api/v1/investigations
  API->>StartUC: execute(CreateInvestigationCommand)
  StartUC->>Repo: create(investigation)
  Repo->>DB: INSERT investigations
  StartUC->>Repo: append_event(investigation.created)
  Repo->>DB: INSERT investigation_events
  StartUC-->>API: InvestigationAggregate
  API-->>Client: 201 InvestigationResponse
```

**Slice 0:** Persist investigation + initial signal metadata.  
**Slice 1:** Same; may pre-seed alert evidence from `signal` payload.

## Flow 2 — Run investigation (B03, Slice 1)

```mermaid
sequenceDiagram
  participant Client
  participant API
  participant RunUC as RunInvestigation
  participant Inv as DeterministicInvestigatorB03
  participant Conn as FixtureConnectors
  participant Repo as InvestigationRepository

  Client->>API: POST /api/v1/investigations/{id}/run
  API->>RunUC: execute(RunInvestigationCommand)
  RunUC->>Repo: get_aggregate(id)
  RunUC->>Inv: run(context, ports)
  loop playbook_steps
    Inv->>Conn: query_logs / query_metrics / get_deployments
    Conn-->>Inv: raw_records
    Inv->>Inv: normalize_evidence
    Inv->>Repo: append_event + persist evidence
  end
  Inv->>Repo: persist hypotheses + rca
  RunUC->>Repo: update_state(rca_candidate)
  RunUC-->>API: InvestigationAggregate
  API-->>Client: 200 InvestigationResponse
```

## Flow 3 — Get investigation aggregate

```mermaid
sequenceDiagram
  participant Client
  participant API
  participant Repo as InvestigationRepository

  Client->>API: GET /api/v1/investigations/{id}
  API->>Repo: get_aggregate(id)
  alt not_found
    API-->>Client: 404 ProblemDetail
  else found
    API-->>Client: 200 InvestigationResponse
  end
```

Aggregate includes: investigation header, `events[]`, `evidence[]`, `hypotheses[]`, `rca` (nullable until run).

## Flow 4 — Health

`GET /health` — no database required for liveness; optional readiness checks DB in Phase 0b.

## Cross-references

- Use cases: [../lld/02-application-use-cases.md](../lld/02-application-use-cases.md)
- B03 playbook: [../lld/06-deterministic-investigator-b03.md](../lld/06-deterministic-investigator-b03.md)
- API: [../api/openapi.yaml](../api/openapi.yaml)
