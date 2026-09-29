# LLD 07 — Observability (AVENIQ self-telemetry)

Per product [docs/17-observability-strategy.md](../../docs/17-observability-strategy.md) and NFR-04.

## Structured logging

JSON lines to stdout (Phase 0b). Required fields on every log record:

| Field | Source |
|-------|--------|
| `timestamp` | ISO-8601 UTC |
| `level` | INFO, WARNING, ERROR |
| `message` | human short text |
| `service.name` | `aveniq-api` |
| `aveniq.env` | `AVENIQ_ENV` |
| `request_id` | `X-Request-Id` header or generated ULID |
| `investigation_id` | when in investigation context |

Optional: `http.method`, `http.route`, `http.status_code`, `duration_ms`.

## OpenTelemetry

### Resource attributes

| Attribute | Value |
|-----------|--------|
| `service.name` | `aveniq-api` |
| `service.version` | from package `__version__` |
| `deployment.environment` | `AVENIQ_ENV` |

### Span names

| Span | Parent | Attributes |
|------|--------|------------|
| `HTTP {method} {route}` | — | `http.target`, `http.status_code` |
| `aveniq.investigation.start` | HTTP | `investigation_id`, `benchmark_id` |
| `aveniq.investigation.run` | HTTP | `investigation_id` |
| `aveniq.investigator.step` | run | `step_id`, `step_name` |
| `aveniq.connector.query_logs` | step | `benchmark_id`, `service` |
| `aveniq.connector.query_metrics` | step | `metric_name` |
| `aveniq.connector.list_deployments` | step | `service` |

### Exporters

| `OTEL_EXPORTER_OTLP_ENDPOINT` | Behavior |
|-------------------------------|----------|
| unset | Console / no-op exporter (dev friendly) |
| set | OTLP HTTP to collector (Jaeger/Tempo on VPS later) |

## Metrics (stubs — register names in 0b, implement counters later)

| Metric | Type | Description |
|--------|------|-------------|
| `aveniq.investigations.created` | counter | |
| `aveniq.investigations.run.completed` | counter | labels: `benchmark_id`, `termination` |
| `aveniq.investigations.run.duration_ms` | histogram | |
| `aveniq.connector.errors` | counter | labels: `connector`, `code` |

## Investigation trace correlation

Propagate `investigation_id` on all spans inside `RunInvestigation`.  
`request_id` links HTTP access logs to trace id via `trace_id` field when OTEL logging bridge enabled (optional 0b).

## Cross-references

- Deployment: [../hld/05-deployment-evolution.md](../hld/05-deployment-evolution.md)
