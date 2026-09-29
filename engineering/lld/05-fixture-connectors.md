# LLD 05 — Fixture connectors

Implement `TelemetryPort`, `ChangePort`, `MetadataPort` in `aveniq_adapters.connectors.fixture`.

## Configuration

| Setting | Description |
|---------|-------------|
| `FIXTURE_ROOT` | Absolute or repo-relative path to `fixtures/` |
| `benchmark_id` | Passed per call from investigation |

Resolved path: `{FIXTURE_ROOT}/{benchmark_id}/`

## Path resolution

```python
def fixture_dir(benchmark_id: str) -> Path:
    root = settings.fixture_root.resolve()
    path = (root / benchmark_id).resolve()
    if not str(path).startswith(str(root)):
        raise ConnectorError("fixture_invalid", "path escape")
    if not path.is_dir():
        raise ConnectorError("fixture_not_found", benchmark_id)
    return path
```

## Whitelist

Allowed reads only:

- `manifest.json`
- `alert.json`
- `services.json`
- `deployments.json`
- `logs/*.jsonl`
- `metrics/*.jsonl`

**Reject** any path containing `ground_truth` (case-insensitive).

## MetadataPort

| Method | File | Behavior |
|--------|------|----------|
| `get_alert` | `alert.json` | Parse JSON object |
| `get_services` | `services.json` | Parse JSON array |

## ChangePort

| Method | File | Filter |
|--------|------|--------|
| `list_deployments` | `deployments.json` | `service == spec.service` AND overlap with `spec.window` |

Deployment overlap: `started_at` within window OR deployment active during window.

## TelemetryPort

| Method | Files | Filter |
|--------|-------|--------|
| `query_logs` | `logs/{service}.jsonl` | NDJSON; `timestamp` in window; optional `level` |
| `query_metrics` | `metrics/{metric_name}.jsonl` or scan `metrics/*.jsonl` where `metric` field matches | `timestamp` in window |

If log file missing: return **empty list** (not error) but investigator may record evidence gap.

If `manifest.json` missing: `fixture_invalid`.

## Query audit

Each query emits connector events (when called from investigator):

- `query_spec` serialized in `connector.query_started` / `completed`

## Future live connectors

Same `QuerySpec` shapes; implementation queries Prometheus/Loki HTTP instead of files. See [docs/18-integrations.md](../../docs/18-integrations.md).

## Cross-references

- Fixture spec: [../01-fixture-package-spec-v1.md](../01-fixture-package-spec-v1.md)
- Data flow: [../hld/04-data-flows.md](../hld/04-data-flows.md)
