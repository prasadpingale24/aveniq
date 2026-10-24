# 08 — Milestone M2 acceptance (application shell)

> **Spine:** [M2 in 00-delivery-spine.md](00-delivery-spine.md) · [docs/31-delivery-spine.md](../docs/31-delivery-spine.md). Legacy name: “Slice 3a.”

**Goal:** Establish **normative** UI foundation in `aveniq_web`: Telemetry Monolith tokens, app shell, client routing scaffold—without full Playground or investigation visual parity (**M4–M5**).

**Depends on:** ADR-016, [07-application-surface.md](07-application-surface.md), [lld/12](lld/12-design-system-telemetry-monolith.md), [lld/13](lld/13-ui-component-registry-v0.md).

## Preconditions

- Slice 2 complete (Playground API + minimal web)
- Stitch reference present under `stitch_aveniq_incident_investigation_design_system/`

## In scope

- CSS theme variables (or Tailwind theme) matching lld/12 core tokens
- `app-shell` component: top bar + side nav layout per Stitch Option A (nav items may be disabled placeholders except Playground)
- React Router (or equivalent) routes: `/playground`, `/investigations/:id` (stub page ok), redirect `/` → `/playground`
- `persona-toggle` present in shell; state persisted in URL query or context for investigation routes (behavior fully used in 3c)
- Typography: Inter + JetBrains Mono loaded in app (not Google CDN in production if self-hosted preferred)
- Remove or isolate pre-3a ad-hoc global CSS that conflicts with tokens

## Out of scope

- Pixel parity with Stitch PNGs for Playground or investigation (Slice 3b/3c)
- nginx `/api` proxy (optional follow-up)
- Auth, incidents inbox, HITL
- New API endpoints

## Functional acceptance

1. `npm run build` in `packages/aveniq_web` succeeds
2. App renders dark Telemetry Monolith canvas (`--bg-canvas`) and surface panels (`--bg-surface`)
3. Navigating to `/playground` shows shell + existing or placeholder Playground content inside outlet
4. Persona toggle visible in shell; switching updates client state without API call
5. No Stitch `code.html` imported or served from `aveniq_web`

## Visual acceptance (manual)

Compare shell chrome (header height, nav width, border color) to `scr_playground_01_*/screen.png` at desktop width—reasonable match, not pixel-perfect until 3b.

## Tests

| Test | Description |
|------|-------------|
| `npm run build` | CI / local |
| Optional future | Playwright smoke on shell routes |

## Done when

- Acceptance above met
- engineering/README.md lists Slice 3a complete
- Root README mentions UI program ([docs/29-ui-program.md](../docs/29-ui-program.md))

## Cross-references

- Next: **M3** dev session (spec TBD), then **M4** Playground E2E, **M5** investigation workspace
