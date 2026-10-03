# LLD 10 — Playground orchestration

## Purpose

One **orchestration contract** for B03 (and future scenarios): reset stand-in → trigger scenario → create investigation → run → return aggregate. Used by CLI, API route, and compose smoke script.

## Scenario registry (v1)

| `scenario_id` | `benchmark_id` | Stand-in trigger | Default signal |
|---------------|----------------|------------------|----------------|
| `b03` | `b03` | `POST /playground/scenarios/b03/trigger` | From [scenarios/b03/definition.yaml](../../scenarios/b03/definition.yaml) `alert` |

## Steps (`run_scenario`)

1. `POST {standin_base}/playground/reset`
2. `POST {standin_base}/playground/scenarios/{scenario_id}/trigger`
3. `POST {api_base}/api/v1/investigations` with body from registry
4. `POST {api_base}/api/v1/investigations/{id}/run`
5. Poll `GET {api_base}/api/v1/investigations/{id}` until `state` ∈ `{rca_candidate, inconclusive, blocked}` or timeout

**Idempotency:** Each playground run creates a **new** investigation. Stand-in reset clears trigger state.

## Configuration

| Variable | Default | Notes |
|----------|---------|-------|
| `AVENIQ_API_URL` | `http://127.0.0.1:8000` | Compose: `http://aveniq-api:8000` |
| `CHECKOUT_STANDIN_URL` | `http://127.0.0.1:8081` | Compose: `http://checkout-standin:8081` |
| `PLAYGROUND_POLL_TIMEOUT_SEC` | `60` | |
| `PLAYGROUND_POLL_INTERVAL_SEC` | `0.5` | |

## Investigation data path (Slice 2)

AVENIQ **`CONNECTOR_MODE=fixture`** during run. Stand-in provides **runtime realism** (logs/metrics) for Playground narrative only. Slice 2b may add `CONNECTOR_MODE=standin`.

## API mapping

- `POST /api/v1/playground/scenarios/{scenario_id}/runs` → invokes `run_scenario` with app-configured stand-in URL
- `GET /api/v1/playground/scenarios` → lists registry metadata (title, benchmark_id)

## Errors

| Condition | HTTP / behavior |
|-----------|-----------------|
| Unknown `scenario_id` | 404 |
| Stand-in unreachable | 502 from API playground route |
| Run timeout | 504 or 500 with `playground_timeout` |

## Cross-references

- Stand-in: [../../services/checkout-standin/README.md](../../services/checkout-standin/README.md)
- Slice acceptance: [06-slice-2-playground-compose.md](../06-slice-2-playground-compose.md)
