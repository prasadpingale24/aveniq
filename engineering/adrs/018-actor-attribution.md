# ADR-018 — Actor attribution on investigation events

| | |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-10-03 |
| **Decides** | Shape of `actor` on mutating events and HTTP defaults (not login) |

## Context

Audit, HITL, and future RBAC require knowing **who or what** caused mutations ([docs/19-security.md](../../docs/19-security.md) §11). Investigation events had no standard actor field. This ADR is **not** session/JWT design (see [docs/30-identity-access-decisions.md](../../docs/30-identity-access-decisions.md) §4–5).

## Decision

**Option 2B — structured opaque actor** on mutating investigation events:

```json
{ "kind": "anonymous|user|service|system", "id": "<string>", "display": "<optional>" }
```

| Trigger | Default actor |
|---------|----------------|
| HTTP `POST /investigations` | `anonymous` / `local`; optional header `X-Actor-Id` sets `id` |
| Playground in-process orchestration | `service` / `playground-runner` |
| B03 deterministic investigator events | `service` / `investigator-b03` |
| Post-auth (future) | `user` / IdP `sub` |

Rules:

1. **Presentation profile** (`engineer` / `lead` / `stakeholder`) is never stored as `actor` and never implies permission ([lld/09](../lld/09-presentation-profiles.md)).
2. Persist envelope in `payload_json` as `{ "payload": …, "actor": … }`; legacy flat payloads remain readable.
3. OpenAPI `InvestigationEvent` exposes optional `actor`.

## Consequences

- Positive: One event shape from Playground through production; auth plugs into same model.
- Negative: Convention discipline until IdP; `X-Actor-Id` is not security (spoofable until auth).

## References

- [02-investigation-event-catalog.md](../02-investigation-event-catalog.md)
- ADR-017 (tenancy)
