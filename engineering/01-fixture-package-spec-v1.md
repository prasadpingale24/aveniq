# 01 — Fixture package specification v1

**Version:** `fixture-package/1.0`  
**ADR:** [adrs/013-fixture-format-v1.md](adrs/013-fixture-format-v1.md)

## Purpose

Define on-disk layout for benchmark **`b03`** (extensible to `b01`…`b10`). Connectors read only this layout; scenario scripts must emit conforming files.

## Directory layout

```text
fixtures/{benchmark_id}/
  manifest.json           # required: package version, benchmark_id, time anchor
  alert.json              # required: initial signal
  services.json           # required: service metadata + dependencies
  deployments.json        # required: change events
  logs/
    {service}.jsonl       # one or more NDJSON log streams
  metrics/
    {metric_name}.jsonl   # NDJSON metric points
  ground_truth.json       # EVAL ONLY — see hld/04-data-flows.md
```

**Runtime whitelist:** connectors may read `manifest.json`, `alert.json`, `services.json`, `deployments.json`, `logs/**`, `metrics/**`.  
**Forbidden at runtime:** `ground_truth.json`, `**/ground_truth.json`.

## manifest.json

```json
{
  "fixture_package_version": "1.0",
  "benchmark_id": "b03",
  "title": "Database connection exhaustion",
  "incident_window": {
    "start": "2026-09-28T14:28:00Z",
    "end": "2026-09-28T14:45:00Z"
  },
  "environment": "production",
  "primary_service": "checkout-api"
}
```

## alert.json

```json
{
  "id": "alert-b03-001",
  "fired_at": "2026-09-28T14:36:00Z",
  "name": "checkout-api error rate high",
  "condition": "error_rate > 0.10",
  "service": "checkout-api",
  "severity": "critical",
  "labels": { "team": "checkout" }
}
```

## services.json

Array of services:

```json
[
  {
    "name": "checkout-api",
    "owner": "checkout-team",
    "dependencies": ["postgresql-checkout"]
  },
  {
    "name": "postgresql-checkout",
    "type": "database"
  }
]
```

## deployments.json

```json
[
  {
    "id": "dep-b03-001",
    "service": "checkout-api",
    "version": "2.8.1",
    "started_at": "2026-09-28T14:29:00Z",
    "config_changes": [
      {
        "key": "database.pool.max_size",
        "old_value": "50",
        "new_value": "5"
      }
    ]
  }
]
```

## logs/*.jsonl

One JSON object per line:

```json
{
  "timestamp": "2026-09-28T14:32:00Z",
  "service": "checkout-api",
  "level": "ERROR",
  "message": "Failed to acquire database connection",
  "attributes": { "error_type": "PoolExhausted" }
}
```

## metrics/*.jsonl

```json
{
  "timestamp": "2026-09-28T14:30:00Z",
  "service": "checkout-api",
  "metric": "db.pool.utilization",
  "value": 0.99,
  "unit": "ratio"
}
```

## ground_truth.json (eval only)

```json
{
  "benchmark_id": "b03",
  "root_cause_summary": "Production deployment reduced database connection pool capacity, causing pool exhaustion.",
  "root_cause_category": "configuration_change",
  "expected_rca_status": "probable",
  "expected_primary_service": "checkout-api",
  "expected_dependency": "postgresql-checkout",
  "key_evidence_themes": [
    "deployment_config_change",
    "pool_utilization_spike",
    "connection_errors"
  ],
  "timeline_anchors": [
    { "at": "2026-09-28T14:29:00Z", "event": "deployment_started" },
    { "at": "2026-09-28T14:32:00Z", "event": "errors_begin" }
  ]
}
```

Golden tests assert AVENIQ output against tolerances in [04-slice-1-b03.md](04-slice-1-b03.md), not necessarily verbatim match to `root_cause_summary`.

## Scenario source

Human-editable recipe: `scenarios/b03/definition.yaml` → `scripts/build_fixture.py` → `fixtures/b03/`.

## Cross-references

- Connectors: [lld/05-fixture-connectors.md](lld/05-fixture-connectors.md)
- Product evidence model: [docs/10-evidence-model.md](../docs/10-evidence-model.md)
