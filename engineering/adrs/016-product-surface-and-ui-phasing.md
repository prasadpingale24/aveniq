# ADR-016 — Product surface, UI program, and identity phasing

| | |
|---|---|
| **Status** | Accepted (delivery **order** for auth/UI superseded by [021](021-delivery-spine-authority.md)) |
| **Date** | 2026-10-03 |

## Context

Product docs describe an **incident investigation workspace** with adaptive views (docs/03, 24, 15; ADR-005/006). Engineering Slices 0–2 delivered API, B03 playbook, Compose, and a **minimal** `aveniq_web` shell. Stitch exports (`stitch_aveniq_incident_investigation_design_system/`) provide a **visual reference** (“Telemetry Monolith”) but are not runtime code.

Gaps: no single decision on whether Phase 1 UI is a deliverable vs optional viewer; auth timing conflicted between docs/19-security §13 (auth early) and roadmap Phase 7; no screen map tied to OpenAPI routes.

## Decision

1. **Phase 1 product surface:** A **credible investigation workspace UI** is a first-class Phase 1 deliverable—not an afterthought to the API. MVP success (docs/24 §11) includes a useful **incident view**, not curl-only workflows.
2. **Implementation vs reference:**
   - **Normative:** `engineering/lld/12-design-system-telemetry-monolith.md`, `engineering/07-application-surface.md`, `engineering/lld/13-ui-component-registry-v0.md`.
   - **Illustrative:** Stitch `screen.png` per screen + `telemetry_monolith/DESIGN.md`. **Do not** ship Stitch `code.html` or Tailwind CDN exports in `aveniq_web`.
3. **GenUI:** Roadmap Phase 3 (dynamic component selection). Phase 1–2 use **static** layouts and registry v0 (ADR-006). Persona switching is **presentation** only ([lld/09-presentation-profiles.md](../lld/09-presentation-profiles.md)).
4. **Slice program:** UI work proceeds in **horizontal slices** (3a design foundation → 3b Playground parity → 3c investigation workspace → …) each with engineering acceptance specs, same pattern as Slices 0–2.
5. **Identity & auth phasing:**
   | Stage | Environment | Auth |
   |-------|-------------|------|
   | **3a–3c** | local-dev, Playground | None; single implicit operator |
   | **Staging (future)** | shared VPS | Gate at edge (basic auth or OIDC)—**before** multi-tenant data |
   | **Production hardening** | Phase 7 roadmap | Full RBAC, audit, tenancy |

   Reconciles docs/19 §13 (investigation isolation and actor attribution **before** wide deployment) with deferring **enterprise** auth to Phase 7: **no sign-up product** until staging; local remains open.

6. **Data honesty:** UI must not display business impact, user counts, or live ingest metrics unless present in API payload; use “unknown” / omit per lld/09.

## Alternatives considered

| Option | Rejected because |
|--------|------------------|
| API-only Phase 1 | Contradicts product MVP success and vision |
| Import Stitch HTML as app | Unmaintainable; wrong stack; fake chrome data |
| Full OIDC in Slice 3a | Blocks UI foundation; no multi-user backend yet |
| Defer all UI to Phase 3 GenUI | Leaves no static shell for Phase 1 PoC |

## Consequences

- Positive: Clear doc chain product → engineering → Stitch → `aveniq_web`; slice acceptance can require layout parity to PNGs
- Negative: Documentation upkeep when tokens change in Stitch vs lld/12
- Revisit when: staging deploy, auth provider chosen, GenUI Phase 3 starts

## References

- [07-application-surface.md](../07-application-surface.md)
- [lld/12-design-system-telemetry-monolith.md](../lld/12-design-system-telemetry-monolith.md)
- [lld/13-ui-component-registry-v0.md](../lld/13-ui-component-registry-v0.md)
- [08-slice-3a-design-foundation.md](../08-slice-3a-design-foundation.md)
- [../docs/29-ui-program.md](../docs/29-ui-program.md)
- ADR-015, product ADR-005, ADR-006
