# 05 — Local development vs VPS staging

## Principle

**Same images and compose structure; different configuration.** Local optimizes feedback; VPS staging optimizes persistence and realism.

## Environments

| Environment | Purpose | Database | Fixture / connectors |
|-------------|---------|----------|----------------------|
| **local-dev** | Daily development | `./.data/aveniq.db` (gitignored) | `CONNECTOR_MODE=fixture`, `FIXTURE_ROOT=./fixtures` |
| **ci** | Jenkins / local CI | Temp file or `:memory:` per test job | `FIXTURE_ROOT` pointing at repo fixtures |
| **vps-staging** | Demo, smoke, persistent history | Volume-mounted SQLite (later Postgres) | Fixture or live stack (Slice 2+) |

**Never** point CI cleanup scripts at the VPS staging database. Staging DB **persists across deploys** unless an operator runs a documented migration/reset procedure.

## Configuration (`.env.example` targets)

| Variable | local-dev | ci | vps-staging |
|----------|-----------|-----|-------------|
| `AVENIQ_ENV` | `local` | `ci` | `staging` |
| `AVENIQ_SQLITE_PATH` | `./.data/aveniq.db` | temp path | `/var/lib/aveniq/data.db` |
| `FIXTURE_ROOT` | `./fixtures` | `$REPO_ROOT/fixtures` | `/app/fixtures` or volume |
| `CONNECTOR_MODE` | `fixture` | `fixture` | `fixture` → `live` later |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | empty (console) | empty | collector URL optional |
| `LOG_LEVEL` | `DEBUG` | `WARNING` | `INFO` |

## Compose files (Phase 0b placeholder → Slice 2+)

| File | Use |
|------|-----|
| `compose/compose.yml` | Service definitions (api, future stand-in app) |
| `compose/compose.override.yml` | Local: build, bind mounts (optional, gitignored patterns) |
| `compose/compose.staging.yml` | VPS: `image:` from Harbor, volumes, no source mounts |

## Deployment pipeline (future — not Phase 0b)

Documented in [hld/05-deployment-evolution.md](hld/05-deployment-evolution.md): Jenkins on VPS → build → push Harbor → `compose pull && up` with persistent volume for SQLite.

## Cross-references

- Persistence paths: [lld/04-persistence.md](lld/04-persistence.md)
- API base URL: staging served behind Nginx TLS; local `http://127.0.0.1:8000`
