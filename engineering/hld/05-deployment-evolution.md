# HLD 05 — Deployment evolution

## Phases vs deployment

| Product phase | Deployment target |
|---------------|-------------------|
| **0b–1** | Local `uv run`; CI pytest on Jenkins; **no VPS required** |
| **Slice 2** | `docker compose` local + CI integration job |
| **Deploy handoff** | VPS: Harbor + Jenkins + Nginx + persistent SQLite volume |
| **Later** | Postgres, separate OTEL backend, MCP sidecars |

## Target VPS topology (future)

```text
Internet
   → Nginx (TLS, your domain)
        → aveniq-api:8000
        → (optional) grafana.*

Same VPS:
   Jenkins  → build → push harbor.local/aveniq/api:tag
   Harbor   → store images
   Compose  → pull images, mount volumes
```

Push-based CI/CD: Jenkins **pushes** image tags; runtime **pulls** — no git on server required for app code.

## Local vs VPS parity

| Concern | Local | VPS staging |
|---------|-------|-------------|
| Image | `docker build` or `uv run` | Pull from Harbor |
| Config | `.env` | `.env.staging` on server (not in git) |
| SQLite | `./.data/` | Docker volume `/var/lib/aveniq` |
| Fixtures | Repo checkout or baked in image | Baked in image or mounted read-only volume |

## CI on VPS (Jenkins)

**Stage 1 (Phase 0b):** checkout → `uv sync` → `pytest` (no deploy).

**Stage 2 (Slice 2+):** add `docker build` → push Harbor.

**Stage 3 (deploy handoff):** SSH or local agent on VPS → `compose -f compose.staging.yml up -d` → smoke `GET /health` + one B03 run.

## Cross-references

- Env matrix: [../05-local-vs-staging.md](../05-local-vs-staging.md)
- Observability on VPS: [../lld/07-observability.md](../lld/07-observability.md)
