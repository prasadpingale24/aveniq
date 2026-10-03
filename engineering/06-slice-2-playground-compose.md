# 06 — Slice 2 acceptance (Playground, Compose, foundation closure)

**Goal:** Deliver a **controlled, repeatable** Phase 1 demo path: stand-in checkout service, Docker Compose (`dev` / `test`), Playground orchestration (CLI + API), minimal web UI with persona preview—while keeping investigation RCA on **fixture connectors** (golden tests unchanged).

Product personas: shared incident context, different presentation — [docs/05-user-personas.md](../docs/05-user-personas.md) §7.

## Preconditions

- Slice 1 complete (B03 API + golden test)
- `fixtures/b03/` present (baked in API image or mounted)
- Docker and Docker Compose v2 available for compose workflows

## In scope

- [`compose/docker-compose.dev.yml`](../compose/docker-compose.dev.yml) — `aveniq-api`, `checkout-standin`, `aveniq-web`
- [`compose/docker-compose.test.yml`](../compose/docker-compose.test.yml) — API + stand-in; smoke via [`scripts/compose_test_smoke.sh`](../scripts/compose_test_smoke.sh)
- [`services/checkout-standin/`](../services/checkout-standin/) — health, reset, B03 trigger, logs/metrics
- Playground driver: [`aveniq_application.playground`](../packages/aveniq_application/src/aveniq_application/playground/), [`scripts/playground_run.py`](../scripts/playground_run.py)
- API: `GET /api/v1/playground/scenarios`, `POST /api/v1/playground/scenarios/{scenario_id}/runs`
- [`packages/aveniq_web/`](../packages/aveniq_web/) — Playground UI, engineer view, persona preview toggle
- LLD: [lld/09-presentation-profiles.md](lld/09-presentation-profiles.md), [lld/10-playground-orchestration.md](lld/10-playground-orchestration.md)
- ADR: [adrs/015-slice-2-compose-and-playground.md](adrs/015-slice-2-compose-and-playground.md)

## Out of scope

- `docker-compose.staging.yml` / `docker-compose.prod.yml` implementation
- `CONNECTOR_MODE=live` / stand-in telemetry into AVENIQ (Slice 2b)
- Auth, RBAC, LLM agent, MCP, full Generative UI

## Functional acceptance

1. `docker compose -f compose/docker-compose.dev.yml up --build` — all services healthy
2. Playground API `POST .../playground/scenarios/b03/runs` → **201**, investigation reaches `rca_candidate`, RCA tolerances match Slice 1 golden rules
3. Stand-in receives reset + trigger during playground run; structured logs reflect pool exhaustion theme
4. UI Playground **Run scenario** uses playground API; persona preview toggles layout without changing API facts
5. `scripts/compose_test_smoke.sh` exits 0 against `docker-compose.test.yml`
6. `uv run pytest` (no compose) — all existing tests green

## Tests (Slice 2)

| Test id | Description |
|---------|-------------|
| `test_playground_driver_b03` | Unit: mocked HTTP orchestration |
| `test_playground_api_run_b03` | Integration: TestClient playground run |
| `test_openapi_contract_paths_exist` | Includes playground paths |
| `test_b03_investigation` | Unchanged golden |
| Compose smoke | `scripts/compose_test_smoke.sh` (manual/CI) |

## CI invocation (compose smoke)

```bash
docker compose -f compose/docker-compose.test.yml up --build -d
./scripts/compose_test_smoke.sh
docker compose -f compose/docker-compose.test.yml down -v
```

## Done when

- All Slice 2 tests green
- Slice 2 docs and ADR-015 linked from [README.md](README.md) and [docs/26-decisions.md](../docs/26-decisions.md)
- [compose/README.md](../compose/README.md) documents dev/test commands

## Cross-references

- Local vs staging env matrix: [05-local-vs-staging.md](05-local-vs-staging.md)
- Deployment evolution: [hld/05-deployment-evolution.md](hld/05-deployment-evolution.md)
- Slice 1: [04-slice-1-b03.md](04-slice-1-b03.md)
