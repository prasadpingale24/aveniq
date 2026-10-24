# ADR-022 — Dev session login (M3)

| | |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-10-04 |

## Decision

1. **Compose dev** enables `AUTH_ENABLED` with `AUTH_DEV_USERS` (`user:password` list)—not public sign-up.
2. **Session:** in-memory store + HttpOnly `aveniq_session` cookie; API accepts Bearer token alternatively.
3. When auth enabled, `/api/v1/*` (except `/health`, `/api/v1/auth/*`) requires session.
4. Mutations use `actor.kind=user` and username from session (ADR-018).
5. **Web:** nginx proxies `/api` to API in compose; `credentials: include`; `/login` gate when auth required.

## References

- [11-milestone-m3-dev-session.md](../11-milestone-m3-dev-session.md)
- ADR-018, ADR-021
