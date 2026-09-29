# LLD 06 — Deterministic investigator (B03)

**ADR:** [adrs/014-deterministic-investigator-v1.md](../adrs/014-deterministic-investigator-v1.md)

Class: `DeterministicInvestigatorB03` implements `Investigator`.  
No LLM. Steps are fixed order; evidence ids are **stable** for golden tests.

## Preconditions

- `investigation.benchmark_id == "b03"`
- Else raise `UnsupportedBenchmarkError`

## Incident window

From `manifest.incident_window` if present; else:

- `start` = `alert.fired_at` - 10 minutes  
- `end` = `alert.fired_at` + 15 minutes  

Emit: `investigation.question_raised` (category `scope`), `investigation.state_changed` → `investigating`.

## Playbook steps

### Step 1 — Record alert evidence

| Item | Value |
|------|-------|
| evidence_id | `ev_b03_alert_001` |
| source_type | `alert` |
| strength | `direct` |
| observation | Alert text from `get_alert()` |
| fixture_ref | `alert.json` |

### Step 2 — Query error logs

- `LogQuerySpec(service="checkout-api", window, level_min="ERROR")`
- Emit connector events
- For each matching line (or aggregate): evidence `ev_b03_log_errors_001`  
  - observation: e.g. "checkout-api logged database connection acquisition failures beginning at 14:32 UTC"
  - fixture_ref: `logs/checkout-api.jsonl#<n>`

### Step 3 — Query pool utilization metric

- `MetricQuerySpec(service="checkout-api", metric_name="db.pool.utilization", window)`
- evidence `ev_b03_metric_pool_util_001`  
  - strength: `derived`  
  - observation: "db.pool.utilization reached 0.99 during incident window"

### Step 4 — List deployments

- `DeploymentQuerySpec(service="checkout-api", window)`
- evidence `ev_b03_deploy_001`  
  - strength: `direct`  
  - observation: "checkout-api v2.8.1 deployed; database.pool.max_size changed from 50 to 5"

### Step 5 — Hypothesis H1

| Field | Value |
|-------|-------|
| hypothesis_id | `hyp_b03_h1` |
| statement | "Recent deployment reduced database connection pool capacity, leading to connection exhaustion and checkout-api errors." |
| supporting | all evidence ids above |
| status | `supported` |

Events: `hypothesis.created`, `hypothesis.updated`

### Step 6 — RCA

| Field | Value |
|-------|-------|
| status | `probable` |
| root_cause | "A production deployment (v2.8.1) reduced the database connection pool max size, causing connection pool exhaustion." |
| summary | Same shorter |
| causal_chain | `["Configuration change (pool max 50→5)", "Connection pool exhaustion", "DB acquisition failures", "checkout-api HTTP errors"]` |
| timeline | anchors from fixture manifest / ground truth themes |
| claims | see table below |
| evidence_gaps | `[]` for happy path B03 |
| uncertainty | "Distributed tracing not used; request-level impact not verified." |
| observability_lessons | e.g. "Alert on db.pool.utilization earlier" |

#### Claims

| claim_id | text | evidence_ids |
|----------|------|--------------|
| `claim_b03_1` | Errors increased on checkout-api during the incident window | `ev_b03_log_errors_001`, `ev_b03_alert_001` |
| `claim_b03_2` | Connection pool utilization peaked at 99% | `ev_b03_metric_pool_util_001` |
| `claim_b03_3` | Deployment changed pool configuration before errors | `ev_b03_deploy_001`, `ev_b03_log_errors_001` |

### Step 7 — Complete

- Save `Rca` via repository
- `investigation.state` → `rca_candidate`
- Events: `rca.published`, `investigation.state_changed`, `investigation.completed` (`termination: rca_candidate`)

## Traceability example

`claim_b03_2` → `ev_b03_metric_pool_util_001` → provenance `metrics/db.pool.utilization.jsonl#<line>`

## Cross-references

- Events: [../02-investigation-event-catalog.md](../02-investigation-event-catalog.md)
- Acceptance: [../04-slice-1-b03.md](../04-slice-1-b03.md)
