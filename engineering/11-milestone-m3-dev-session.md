# 11 — Milestone M3 acceptance (dev session & identity)

> **Spine:** [00-delivery-spine.md](00-delivery-spine.md) · [docs/31-delivery-spine.md](../docs/31-delivery-spine.md)

**Goal:** Local / compose **dev** runs the same app with **sign-in**, session cookie, and API `actor.kind=user` on mutations—not anonymous-only Playground.

## In scope

- Dev credential login (`AVENIQ_AUTH_ENABLED`, `AVENIQ_AUTH_DEV_USERS`) — not public sign-up
- `GET /api/v1/auth/config`, `POST login`, `POST logout`, `GET /me`
- HttpOnly session cookie; `credentials: include` from web
- When auth enabled: API routes under `/api/v1/` (except health + auth) require session
- Compose dev: web nginx proxies `/api` → API (same-origin cookies); optional direct `:8000` with CORS
- Login page + protected shell; sign-out in header

## Out of scope

- OIDC / Keycloak, refresh tokens, RBAC matrix (M9+)
- Staging TLS (M7)
- Scope enforcement on `GET` by org (still ADR-017 follow-up)

## Acceptance

1. With `AVENIQ_AUTH_ENABLED=true`, unauthenticated `GET /api/v1/playground/scenarios` → 401
2. Login as configured dev user → scenarios load; `investigation.created` actor is `user` + username
3. Logout clears session; 401 again
4. With auth disabled (CI/tests), behavior unchanged from pre-M3
5. `npm run build` succeeds

## Cross-references

- ADR-018 (actor), ADR-021 (spine), [docs/30-identity-access-decisions.md](../docs/30-identity-access-decisions.md) §5
