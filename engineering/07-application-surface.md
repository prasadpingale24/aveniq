# 07 — Application surface (screens, routes, journeys)

Maps product journeys to **implementable routes** and Stitch reference screens. Build contract for `packages/aveniq_web`. Visual spec: [lld/12-design-system-telemetry-monolith.md](lld/12-design-system-telemetry-monolith.md).

**Stitch reference root:** [`../stitch_aveniq_incident_investigation_design_system/`](../stitch_aveniq_incident_investigation_design_system/) (reference only — see ADR-016).

## App shell (all authenticated-era screens)

| Region | Spec |
|--------|------|
| Top bar | 44px; environment badge; persona toggle `[ENG \| LEAD \| STAKEHOLDER]`; scenario/benchmark context when applicable |
| Left nav | Playground, Incidents (future), active investigation; collapsed icon rail per Stitch Option A |
| Main | Persona-dependent gutters per lld/09 / Stitch `screen_map.md` §2 |

Milestone **M2** implements shell + tokens; login (**M3**) and nav targets complete in later milestones ([31-delivery-spine.md](../docs/31-delivery-spine.md)).

## Screen catalog

| Screen ID | Stitch folder | Target route (v1 impl) | API / data | Slice |
|-----------|---------------|------------------------|------------|-------|
| `scr-playground-01` | `scr_playground_01_*` | `/playground` | `GET/POST .../playground/*` | M1 (functional), **M4** (visual E2E) |
| `scr-investigation-eng-02` | `scr_investigation_eng_02_*` | `/investigations/:id?profile=engineer` | `GET .../investigations/{id}` | **M5** |
| `scr-investigation-lead-03` | `scr_investigation_lead_03_*` | `/investigations/:id?profile=lead` | same payload | **M5** |
| `scr-investigation-stake-04` | `scr_investigation_stake_04_*` | `/investigations/:id?profile=stakeholder` | same payload | **M5** |
| `scr-incidents-inbox-05` | `scr_incidents_inbox_05_*` | `/incidents` | **List API TBD** | **M6** |
| `scr-hitl-question-06` | `scr_hitl_question_06_*` | `/investigations/:id/clarify` | Agent/HITL TBD | **M8** |
| `scr-states-sheet-07` | `scr_states_sheet_07_*` | (dev reference) | N/A | **M5** states |

`:id` is investigation ULID from API, not slug `b03-pool-exhaustion`. Stitch slugs are **mock labels only**.

## Journey mapping

| Journey step ([docs/06-user-journeys.md](../docs/06-user-journeys.md)) | Primary screen(s) |
|------------------------------------------------------------------------|-------------------|
| Incident initialization / manual investigation | Playground run → investigation detail |
| Evidence aggregation | Investigation engineer view |
| Hypothesis / RCA review | Investigation (all profiles, filtered) |
| Human clarification | HITL screen (future) |
| Post-incident artifacts | Out of scope until Phase 6 docs |

## Persona presentation

Same `InvestigationResponse` for all profiles. Client applies [lld/09-presentation-profiles.md](lld/09-presentation-profiles.md). Optional future: `GET .../investigations/{id}?profile=` returns identical body + hints; v1 is **client-only** toggle.

## API mapping (current OpenAPI)

| UI action | Operation |
|-----------|-----------|
| List playground scenarios | `GET /api/v1/playground/scenarios` |
| Run scenario | `POST /api/v1/playground/scenarios/{scenario_id}/runs` |
| Load investigation | `GET /api/v1/investigations/{investigation_id}` |
| Health (ops chrome optional) | `GET /health` |

## Out of scope by milestone

| Item | Milestone |
|------|-----------|
| Sign-up / login UI | **M3** (dev session)—not end-of-roadmap |
| Evidence Vault, live ingest sidebar | Decorative in Stitch mocks only |
| GenUI dynamic layout engine | Spine M9+ (roadmap theme) |
| `GET /incidents` list | **M6** |

## UI milestones (summary)

See [00-delivery-spine.md](00-delivery-spine.md). **M2** spec: [08-slice-3a-design-foundation.md](08-slice-3a-design-foundation.md).

## Cross-references

- Stitch screen map: [`../stitch_aveniq_incident_investigation_design_system/screen_map.md`](../stitch_aveniq_incident_investigation_design_system/screen_map.md)
- ADR-016, lld/13 component registry
