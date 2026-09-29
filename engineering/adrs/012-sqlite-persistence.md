# ADR-012 — SQLite persistence (Phase 0b–1)

| | |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-09-28 |

## Context

Investigations require durable event logs and aggregates. Solo deployment on VPS with Docker volumes; Postgres ops not yet justified.

## Decision

- SQLite file at `AVENIQ_SQLITE_PATH`
- Repository pattern behind ports; domain has no SQL
- Schema migrations via numbered SQL files + `schema_migrations` table
- WAL mode enabled

## Alternatives considered

| Option | When to revisit |
|--------|-----------------|
| In-memory only | Rejected — breaks resume/demo on staging |
| Postgres immediately | Revisit at multi-instance API or multi-tenant product |

## Consequences

- Staging persists investigations across deploys (volume-mounted file)
- CI uses ephemeral DB paths only

## References

- [lld/04-persistence.md](../lld/04-persistence.md)
- [05-local-vs-staging.md](../05-local-vs-staging.md)
