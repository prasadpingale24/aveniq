# 10 — Milestone M5 acceptance (Investigation workspace)

> **Spine:** M5 in [00-delivery-spine.md](00-delivery-spine.md)

**Goal:** `/investigations/:id` delivers **signal → evidence → hypotheses → RCA** per persona, using one `InvestigationResponse` payload.

## In scope

- Components per [lld/13](lld/13-ui-component-registry-v0.md): signal strip, state header, timeline, evidence/hypothesis cards, RCA panel/claims
- Profiles: `engineer`, `lead`, `stakeholder` ([lld/09](lld/09-presentation-profiles.md), ADR-019)
- States: loading skeleton, `blocked`, `inconclusive` / inconclusive RCA ([scr-states-sheet-07](lld/13-ui-component-registry-v0.md))
- Back link to Playground; persona via `?profile=` + shell toggle

## Out of scope

- Incidents inbox (M6), HITL panel (M8), GenUI
- Fabricated business-impact metrics

## Acceptance

1. `npm run build` succeeds
2. After B03 run, workspace shows engineer layout with evidence, hypotheses, RCA claims
3. Persona toggle switches layout without refetch
4. Blocked/inconclusive states render dedicated banners when `state` matches
