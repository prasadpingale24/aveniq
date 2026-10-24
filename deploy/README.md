# Deploy (M7 staging preview)

**Goal:** Same app as local dev on a VPS — static UI on **host nginx**, API + stand-in in **Docker**, persistent SQLite volume. Still **fixture B03** data path (realistic demo workload is a later spine revision).

## Layout

| Piece | Where |
|-------|--------|
| UI (SPA) | `/var/www/aveniq` — built with `scripts/staging-build-ui.sh` |
| TLS / HTTP | Host nginx — `deploy/nginx/aveniq.pspworks.cloud.conf.example` |
| API | Docker `aveniq-api` → `127.0.0.1:${AVENIQ_API_PORT}` (default **8010**) |
| Stand-in | Docker internal only (no host port) |

## First-time on VPS (summary)

1. DNS `A` record → VPS for `aveniq.pspworks.cloud`.
2. Clone repo; `cp compose/.env.staging.example compose/.env.staging`.
3. `bash scripts/staging-init-env.sh` (sets secrets interactively) **or** edit `.env.staging` manually.
4. `docker compose -f compose/docker-compose.staging.yml --env-file compose/.env.staging up -d --build`
5. `bash scripts/staging-build-ui.sh` (requires Node 20+ on host, or run build elsewhere and rsync `dist/`).
6. Install nginx site from `deploy/nginx/aveniq.pspworks.cloud.conf.example`; `nginx -t && systemctl reload nginx`.
7. `sudo certbot --nginx -d aveniq.pspworks.cloud`

## Updates

```bash
git pull
docker compose -f compose/docker-compose.staging.yml --env-file compose/.env.staging up -d --build
bash scripts/staging-build-ui.sh
```

Spec: [engineering/13-milestone-m7-staging-preview.md](../engineering/13-milestone-m7-staging-preview.md).
