# Docker Compose

Standalone compose files per environment (`docker-compose.<type>.yml`). No override merge pattern.

## Prerequisites

- Docker Engine + Compose v2
- For dev UI: Node.js 20+ (or use pre-built web image from compose)

## Local development (`dev`)

```bash
cp compose/.env.dev.example compose/.env.dev
docker compose -f compose/docker-compose.dev.yml --env-file compose/.env.dev up --build
```

| Service | URL |
|---------|-----|
| Web (Playground) | http://127.0.0.1:5173 |
| API | http://127.0.0.1:8000/docs |
| Checkout stand-in | http://127.0.0.1:8081/health |

Investigation RCA uses **fixture** data; stand-in emits demo logs/metrics. See [engineering/lld/10-playground-orchestration.md](../engineering/lld/10-playground-orchestration.md).

## CI smoke (`test`)

```bash
docker compose -f compose/docker-compose.test.yml up --build -d
./scripts/compose_test_smoke.sh
docker compose -f compose/docker-compose.test.yml down -v
```

## Reserved (not implemented)

- `docker-compose.staging.yml` — VPS + Harbor
- `docker-compose.prod.yml` — production

Acceptance criteria: [engineering/06-slice-2-playground-compose.md](../engineering/06-slice-2-playground-compose.md).
