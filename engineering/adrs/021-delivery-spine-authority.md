# ADR-021 — Delivery spine authority (journey-ordered milestones)

| | |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-10-04 |

## Context

Build order was split across **roadmap phases** (docs/25), **numbered slices** (engineering 03–08), and **identity Q&A** (docs/30)—often patched downstream (e.g. auth at “Phase 7,” UI slices 3a–3c, staging edge-only). That made execution feel like a sidecar on an incomplete upstream plan.

The product is validated through **end-to-end journeys** (sign-in → shell → start/open investigation → review RCA), not through anonymous API-only phases followed by login at the end.

## Decision

1. **[docs/31-delivery-spine.md](../../docs/31-delivery-spine.md)** is the **execution order** source of truth (milestones `M0`, `M1`, … with no fixed cap).
2. **[docs/25-roadmap.md](../../docs/25-roadmap.md)** remains the **hypothesis** catalog (what questions to answer); it does **not** dictate implementation sequence.
3. **Environments:**
   - **Local dev** = full application including **dev session/identity** (milestone **M3**), not anonymous-only playground.
   - **Staging preview** = same app + integrations/secrets (milestone **M7**), not a different auth model limited to HTTP basic at the edge.
4. **Supersedes for delivery order only:** ADR-016 §5 table row implying no auth through UI slices 3a–3c. UI shell (**M2**) may ship before **M3**; **M3** precedes polishing Playground/investigation E2E (**M4–M5**).
5. Legacy filenames (`08-slice-3a-…`, “Slice 3b”) remain valid **specs** until renamed; [00-delivery-spine.md](../00-delivery-spine.md) maps them to milestones.

## Alternatives considered

| Option | Rejected because |
|--------|------------------|
| Keep Phase 7 as first auth | Delays validating logged-in flows locally |
| Renumber all roadmap phases | Churn without user-visible benefit |
| Only edge auth on staging | App still anonymous; actor/RBAC story weak |

## Consequences

- Positive: Clear “what’s next” (M2 → M3 → M4…); identity ADRs attach to milestones.
- Negative: Requires updating cross-links in READMEs; some docs still mention old slice IDs until edited opportunistically.
- Identity log §4–§6: document when **M3/M7/M9+** specs are written, not as orphan Phase 7 patches.

## References

- ADR-016, 017, 018, 019
- [07-application-surface.md](../07-application-surface.md)
