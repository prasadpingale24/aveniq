# ADR-019 — Presentation profile is not authorization

| | |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-10-03 |
| **Decides** | Relationship between UI persona toggle and RBAC (Phase 7) |

## Context

AVENIQ uses **presentation profiles** (`engineer`, `lead`, `stakeholder`) to emphasize different parts of the **same** investigation aggregate ([docs/05-user-personas.md](../../docs/05-user-personas.md) §7, [lld/09-presentation-profiles.md](../lld/09-presentation-profiles.md)). **RBAC** (roadmap Phase 7) will gate **actions and resource access** (read investigation, run playbook, connector scopes, HITL).

Confusing profile with role leads to either false security (client claims a “privileged view”) or wrong product behavior (one job title locked to one layout).

## Decision

**Option 3A — strict separation:**

1. **Presentation profile** is **client-side** for Phase 1–2 UI (toggle / URL query per [08-slice-3a-design-foundation.md](../08-slice-3a-design-foundation.md)). It is **not** sent as proof of privilege and is **not** stored as `actor` (ADR-018).
2. **Authorization** (future) evaluates **roles/permissions on API operations and resources**, not on which layout the user selected.
3. **Read access** to `InvestigationResponse` implies access to the full aggregate; profile only controls **what the UI shows**, not a separate API payload per profile in v1 ([07-application-surface.md](../07-application-surface.md)).
4. **Optional later:** API may return `suggested_profile` for UX default from role; client may still switch profile if the user already has read access.
5. **Artifact export** (Phase 6+): audience/redaction at generation time per [docs/19-security.md](../../docs/19-security.md) §12 — separate from live workspace toggle.

## Alternatives considered

| Option | Rejected because |
|--------|------------------|
| **3B — Server-capped profiles** | Defer until compliance requires display-level caps; still need read ACL |
| **3C — Profile = role** | Contradicts shared incident context; personas are views not org titles |
| **3D — Server-only profile** | Conflicts with agreed 3a client toggle; revisit for regulated export |

## Consequences

- Positive: Clear split for UI slices 3a–3c vs Phase 7 auth work; no fake RBAC in the toggle.
- Negative: Anyone with investigation read can see all fields via API/direct call—acceptable until granular field ACL is a requirement.

## Implementation phasing

This ADR is **normative documentation**. Delivery remains **per UI/security slices** (3a shell, 3c workspace, staging auth, Phase 7 RBAC)—not a mandate to implement auth in the same change set as the ADR.

## References

- ADR-006, ADR-016, ADR-018
- [docs/30-identity-access-decisions.md](../../docs/30-identity-access-decisions.md)
