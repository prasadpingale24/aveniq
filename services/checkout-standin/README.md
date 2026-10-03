# checkout-api stand-in

Simulated `checkout-api` for AVENIQ Playground. Independent of the AVENIQ Python workspace.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Liveness |
| POST | `/playground/reset` | Clear scenario state |
| POST | `/playground/scenarios/b03/trigger` | Simulate pool exhaustion after deployment |
| GET | `/playground/logs` | Recent structured log lines from last trigger |
| GET | `/metrics` | Prometheus text exposition (demo gauges) |

## Local run

```bash
cd services/checkout-standin
pip install .
checkout-standin
```

Or Docker: see repo root `compose/docker-compose.dev.yml`.
