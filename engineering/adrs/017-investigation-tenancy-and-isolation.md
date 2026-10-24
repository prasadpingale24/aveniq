# ADR-017 — Investigation tenancy and isolation (org-primary)

| | |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-10-03 |
| **Decides** | Security boundary for investigations before full RBAC (Phase 7) |

## Context

Shared staging and Phase 7 multi-tenant product require a clear rule: **what stops one principal from accessing another’s investigation data?** Product security docs describe organization → environment → investigation → evidence ([docs/19-security.md](../../docs/19-security.md) §7). The SQLite schema already has nullable `org_id` and `environment_id` on `investigations` ([lld/04-persistence.md](../lld/04-persistence.md)).

ADR-016 defers **authentication and RBAC** until staging edge gate / Phase 7 but requires **investigation isolation before wide deployment**. We need a boundary model that does not rely on ULID secrecy on shared hosts.

## Decision

Adopt **Option B leaning D** (logical boundary in the app, org-primary):

1. **`org_id` is the primary isolation key** for investigations. Every investigation row has a non-null `org_id` in the **application domain** after create (persisted in SQLite).
2. **`environment_id` is secondary** — optional in API input but defaulted for Playground/local; used to separate playground vs future live connector contexts (stand-in, staging, prod).
3. **Playground / local-dev defaults** (until auth supplies scope):
   - `org_id` → `local`
   - `environment_id` → `playground`
   Callers may override explicitly when creating investigations (e.g. tests, future multi-org demos).
4. **Repository discipline:** All investigation **writes** set scope fields. **Reads by id** remain global until an authenticated `InvestigationScope` is enforced (staging milestone); new list/query APIs must filter by `org_id` (and `environment_id` when applicable) from day one.
5. **Not in scope of this ADR:** user login, JWT vs cookies, role definitions, or enforcing scope on `GET /investigations/{id}` — see [docs/30-identity-access-decisions.md](../../docs/30-identity-access-decisions.md) (actor, auth dives).

## Alternatives considered

| Option | Why not chosen |
|--------|----------------|
| **A — Global pool, no boundary** | Unsafe on shared staging; high rework when adding auth |
| **C — Environment-first only** | Weak multi-customer story; org still needed for SaaS |
| **D alone — Required org in DB NOT NULL** | Deferred: SQLite migration/backfill for existing rows; application-layer requiredness + defaults is sufficient for Phase 1 |

## Consequences

- Positive: Auth/RBAC can attach **allowed org_ids** without redesigning rows; Playground behavior is explicit constants.
- Negative: Until scope checks on GET, shared staging still needs an **edge gate** (ADR-016); IDs alone are not authorization.
- Implementation: defaults applied in `StartInvestigation`; OpenAPI documents server defaults; LLD 04 updated.

## References

- ADR-016 (identity phasing)
- [lld/04-persistence.md](../lld/04-persistence.md) — isolation scope
- [docs/30-identity-access-decisions.md](../../docs/30-identity-access-decisions.md) — decision log
