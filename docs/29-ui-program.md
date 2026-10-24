# AVENIQ — UI program (Phase 1)

## Purpose

Product docs assume an **incident investigation workspace**, not API-only tooling. This page summarizes how UI is built **per slice** and where the build contract lives.

**Engineering is authoritative** for routes, tokens, and acceptance: [`engineering/07-application-surface.md`](../engineering/07-application-surface.md).

## Principles

- **Evidence-first presentation** — same investigation data for all personas; different emphasis ([docs/05-user-personas.md](05-user-personas.md) §7, [engineering/lld/09-presentation-profiles.md](../engineering/lld/09-presentation-profiles.md)).
- **Constrained components** (ADR-006) — registry v0 in [engineering/lld/13-ui-component-registry-v0.md](../engineering/lld/13-ui-component-registry-v0.md); Generative UI selects layouts in Phase 3 ([docs/15-generative-ui.md](15-generative-ui.md)).
- **Stitch reference, React implementation** — visual truth in `stitch_aveniq_incident_investigation_design_system/` (`screen.png` + `telemetry_monolith/DESIGN.md`); runtime code in `packages/aveniq_web` (ADR-016).

## Delivery order (UI)

**Schedule:** [31-delivery-spine.md](31-delivery-spine.md) — journey milestones, not fixed phase numbers.

| Milestone | UI focus | Status |
|-----------|----------|--------|
| M1 | Minimal Playground web | Done |
| **M2** | Shell, tokens, routes | Done → [08-slice-3a](../engineering/08-slice-3a-design-foundation.md) |
| **M3** | Login / session in local dev | Done |
| M4 | Playground screen E2E | Planned |
| M5 | Investigation workspace + personas | Planned |
| M6 | Incidents inbox | Planned |
| M7 | Staging preview (same app) | Planned |

## Identity

Tenancy defaults (ADR-017), event actors (ADR-018), profile ≠ role (ADR-019). **Dev sign-in** is milestone **M3**, not deferred to “Phase 7.” Granular RBAC later (spine M9+). Log: [30-identity-access-decisions.md](30-identity-access-decisions.md).

## Related

- MVP UI components: [24-mvp.md](24-mvp.md) §6  
- Roadmap Phase 1 “basic UI”: [25-roadmap.md](25-roadmap.md)  
- Implementation ADRs: [26-decisions.md](26-decisions.md) §14 (ADR-016)
