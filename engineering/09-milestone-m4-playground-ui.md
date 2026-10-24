# 09 — Milestone M4 acceptance (Playground UI)

> **Spine:** M4 in [00-delivery-spine.md](00-delivery-spine.md)

**Goal:** `/playground` matches **`scr-playground-01`** layout and run journey; no investigation workspace parity (M5).

## In scope

- Components per [lld/13](lld/13-ui-component-registry-v0.md): `playground-disclaimer`, `playground-scenario-card`, `playground-runner-stepper`, execution log well, fixture drawer (static bundle labels; counts from run when available)
- 12-col grid: orchestrator (8) + fixture drawer (4) on wide viewports
- Run CTA drives API `POST .../runs`; stepper + log reflect client phases; **run completes on Playground** with optional **Open investigation workspace** (M5 owns workspace parity)
- No fabricated ingest/latency chrome; no agentic mode (disabled label only)
- Data honesty: log lines generic during run; post-run may cite real `investigation_id` / state

## Out of scope

- Investigation workspace layouts (M5)
- Step-by-step inspection / reset stand-in buttons (stub or noop)
- Extra scenarios beyond API list (placeholders disabled ok)

## Acceptance

1. `npm run build` succeeds
2. Playground shows disclaimer, scenario card, controls, 4-stage stepper, log panel, fixture drawer
3. Run completes on Playground (stepper + log + summary); user can open `/investigations/:id` explicitly
4. Visual compare to `scr_playground_01_*/screen.png` at ~1280px+ width
