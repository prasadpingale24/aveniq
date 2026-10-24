# 13 — Milestone M7 acceptance (staging preview)

> **Spine:** M7 in [00-delivery-spine.md](00-delivery-spine.md)

**Goal:** Deploy the **same app journeys** (M3–M6) on a VPS at `https://aveniq.pspworks.cloud` (or your host) with persistence and host nginx static UI.

## In scope (this milestone)

- `compose/docker-compose.staging.yml` — API + stand-in; env-driven `AVENIQ_API_BIND` / `AVENIQ_API_PORT`; no web container; stand-in **not** published on host
- `compose/.env.staging.example` + gitignored `compose/.env.staging`
- `scripts/staging-init-env.sh` — interactive secrets (no passwords in repo)
- `scripts/staging-build-ui.sh` — `VITE_API_BASE_URL=` build → `/var/www/aveniq`
- `deploy/nginx/*.conf.example` — HTTP site; certbot `--nginx` for TLS
- [deploy/README.md](../deploy/README.md)

## Out of scope (later spine revision)

- Realistic demo application + live connectors (roadmap Phase 4 / Slice 2b)
- Sign-up / OIDC product auth
- Harbor image pipeline (optional later)

## Acceptance

1. After deploy: sign in, Playground B03 run, Incidents list, investigation workspace
2. SQLite survives `docker compose ... up -d` redeploy (volume `aveniq_staging_data`)
3. No `AUTH_DEV_USERS` or session secret in git

## VPS notes (pspworks.cloud)

- API localhost port **8010** (8000 taken by other stacks on shared host)
- Do not bind stand-in to **8081** (Harbor)
