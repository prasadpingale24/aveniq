# ADR-015 — Slice 2 Compose, Playground, and presentation shell

| | |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-10-02 |

## Context

Slice 1 proved B03 via `uv run` and fixtures. Phase 1 requires a repeatable outsider demo (stand-in + UI) and engineering closure for personas-as-views. Deployment to VPS is deferred; compose types must evolve without override-merge complexity.

## Decision

1. **Compose files:** `compose/docker-compose.<type>.yml` where `type` ∈ `dev`, `test`, (future) `staging`, `prod`. **No** `compose.override.yml` merge pattern.
2. **Playground:** Shared Python orchestration in `aveniq_application.playground`; thin API routes; CLI `scripts/playground_run.py`.
3. **Telemetry split (Slice 2):** Investigation RCA remains **fixture connectors**; checkout stand-in emits logs/metrics for demo realism. Live connectors deferred to Slice 2b.
4. **Presentation:** Add `packages/aveniq_web` (Vite + React + TypeScript) as a **shell UI** (Playground + static persona layouts), not Generative UI (Phase 3). Supplements ADR-011 deferral of TypeScript for **GenUI** only.

## Alternatives considered

| Option | Rejected because |
|--------|------------------|
| Compose override files | Team convention prefers explicit per-environment files |
| UI-only script (no API playground routes) | Duplicates orchestration between UI and CI |
| Live connectors in Slice 2 | Risks golden drift; fixtures remain test spine |

## Consequences

- Positive: CI smoke, demo parity, persona foundation in LLD
- Negative: Two telemetry narratives until Slice 2b; must document clearly in UI copy
- Revisit when: stand-in connectors or staging compose is implemented

## References

- [06-slice-2-playground-compose.md](../06-slice-2-playground-compose.md)
- [lld/09-presentation-profiles.md](../lld/09-presentation-profiles.md)
- [lld/10-playground-orchestration.md](../lld/10-playground-orchestration.md)
- ADR-011
