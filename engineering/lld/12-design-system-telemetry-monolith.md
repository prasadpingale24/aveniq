# LLD 12 — Design system: Telemetry Monolith

**Status:** Normative contract for `packages/aveniq_web`.  
**Visual reference:** [`../../stitch_aveniq_incident_investigation_design_system/telemetry_monolith/DESIGN.md`](../../stitch_aveniq_incident_investigation_design_system/telemetry_monolith/DESIGN.md) and per-screen `screen.png`.

## Implementation rules

1. **Match** layout, color, typography, and density to reference PNGs for each screen ID in [07-application-surface.md](../07-application-surface.md).
2. **Do not** copy Stitch `code.html` into the build (no Tailwind CDN dump, no Material Symbols requirement unless explicitly adopted).
3. **Tokens** in app code must map to the CSS variables / theme below; update this LLD if tokens change intentionally.
4. **No fabricated data:** omit or label “unknown” for metrics not in API (ingest eps, revenue, certainty scores in mocks).

## Aesthetic

Instrument-grade dark operations UI: flat panels, 1px borders, max radius 6px, no glassmorphism or marketing hero layouts. Default **dark mode only** for Phase 1 UI slices.

## Core color tokens (implement as CSS variables)

| Token | Hex | Use |
|-------|-----|-----|
| `--bg-canvas` | `#0B0F14` | Page background |
| `--bg-surface` | `#111822` | Panels, cards |
| `--bg-surface-raised` | `#16202E` | Popovers, dialogs |
| `--bg-surface-inset` | `#070A0E` | Logs, wells |
| `--border-subtle` | `#1E293B` | Panel borders |
| `--border-default` | `#334155` | Emphasized borders |
| `--border-focus` | `#60A5FA` | Focus ring |
| `--text-primary` | `#F1F5F9` | Primary text |
| `--text-secondary` | `#94A3B8` | Secondary |
| `--text-muted` | `#64748B` | Muted / placeholder |
| `--accent-evidence` | `#38BDF8` | Evidence, telemetry |
| `--accent-hypothesis` | `#FBBF24` | Hypotheses |
| `--accent-rca` | `#C084FC` | RCA (semantic accent, not decorative gradient) |
| `--accent-human` | `#34D399` | Human input |
| `--accent-contradiction` | `#FB7185` | Contradiction |
| `--status-probable` | `#38BDF8` | RCA probable |
| `--status-inconclusive` | `#A855F7` | Inconclusive |
| `--status-confirmed` | `#4ADE80` | Confirmed / OK |
| `--status-critical` | `#F87171` | Critical / error |

Full Material-style palette duplicate in Stitch YAML front matter; use table above for app theme unless a component spec requires an extended token from DESIGN.md.

## Typography

| Role | Family | Notes |
|------|--------|-------|
| UI prose | Inter | Headlines, body, summaries |
| IDs, logs, timestamps | JetBrains Mono | `font-variant-numeric: tabular-nums` |

Scale (compact): headline-lg 20px/600; body-md 12px/400; label-md 11px/500 mono for chips.

## Spacing & persona gutters

4px grid. Persona layout modes ([lld/09](09-presentation-profiles.md)):

| Profile | Gutter | Max width |
|---------|--------|-----------|
| engineer | 8px (`0.5rem`) | fluid to 1920px |
| lead | 12px (`0.75rem`) | 1440px centered |
| stakeholder | 16px (`1rem`) | 1080px column |

## Components (summary)

Detailed anatomy in Stitch DESIGN.md § Components. Registry IDs in [lld/13-ui-component-registry-v0.md](13-ui-component-registry-v0.md).

- Buttons: flat primary `#38BDF8`, 4px radius, 28–32px height
- Evidence / status chips: mono, 3px radius, semantic borders
- Telemetry cards: `#111822`, 1px border, optional 3px left accent by domain
- Signal strip, timeline, RCA claim grid, playground stepper — see registry

## Cross-references

- ADR-016, [08-slice-3a-design-foundation.md](../08-slice-3a-design-foundation.md)
- Product ADR-006 constrained library
