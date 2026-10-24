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
| Web | http://127.0.0.1:5173 (sign in: `engineer` / `aveniq` when `AUTH_ENABLED=true`) |
| API | http://127.0.0.1:8000/docs |
| Checkout stand-in | http://127.0.0.1:8081/health |

Investigation RCA uses **fixture** data; stand-in emits demo logs/metrics. See [engineering/lld/10-playground-orchestration.md](../engineering/lld/10-playground-orchestration.md).

## CI smoke (`test`)

```bash
docker compose -f compose/docker-compose.test.yml up --build -d
./scripts/compose_test_smoke.sh
docker compose -f compose/docker-compose.test.yml down -v
```

## Staging preview (`staging`) — M7

Host nginx serves static UI; Docker runs API + stand-in only. See [deploy/README.md](../deploy/README.md).

```bash
cp compose/.env.staging.example compose/.env.staging
bash scripts/staging-init-env.sh   # or edit secrets manually
docker compose -f compose/docker-compose.staging.yml --env-file compose/.env.staging up -d --build
bash scripts/staging-build-ui.sh
# then install deploy/nginx/aveniq.pspworks.cloud.conf.example on host nginx + certbot
```

| Service | Reachability |
|---------|----------------|
| UI | `https://aveniq.pspworks.cloud` (host nginx → `/var/www/aveniq`) |
| API | `127.0.0.1:${AVENIQ_API_PORT}` (default 8010); browser uses `/api/` via nginx |
| Stand-in | Docker network only |

Spec: [engineering/13-milestone-m7-staging-preview.md](../engineering/13-milestone-m7-staging-preview.md).

## Reserved

- `docker-compose.prod.yml` — production

Acceptance criteria: [engineering/06-slice-2-playground-compose.md](../engineering/06-slice-2-playground-compose.md).
