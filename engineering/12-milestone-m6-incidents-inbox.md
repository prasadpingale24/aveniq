# 12 — Milestone M6 acceptance (Incidents inbox)

> **Spine:** M6 in [00-delivery-spine.md](00-delivery-spine.md)

**Goal:** `/incidents` lists investigations for the current org/environment scope; row opens M5 workspace.

## In scope

- `GET /api/v1/investigations` with `org_id`, `environment_id`, `state`, `limit`, `offset` (ADR-017 defaults)
- `scr-incidents-inbox-05`-style table: service, description, benchmark, state, updated
- Nav item enabled; empty state when no rows
- Same auth as other `/api/v1/*` routes when `AUTH_ENABLED`

## Out of scope

- Full-text search, assignee, severity from external systems
- Cross-org admin views

## Acceptance

1. `pytest` + `npm run build` pass
2. After two playground runs, inbox shows two rows (newest first)
3. Click row → `/investigations/:id` with M5 workspace
