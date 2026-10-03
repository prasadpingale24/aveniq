# LLD 09 — Presentation profiles

Maps to product [docs/05-user-personas.md](../../docs/05-user-personas.md) §7 (shared facts, different presentation) and FR-14 in [docs/07-requirements.md](../../docs/07-requirements.md).

## Enum: PresentationProfile

| Value | Persona alignment | UI emphasis |
|-------|-------------------|-------------|
| `engineer` | Small-team engineer, developer | Full evidence, hypotheses, RCA claims with `evidence_ids`, technical timeline |
| `lead` | Technical lead / EM | Summary, state, RCA headline, hypothesis status, reduced raw detail |
| `stakeholder` | Business stakeholder | Service, alert description, RCA summary in plain language; impact fields only when present in payload |

Extend later: `sre`, `developer` as aliases or dedicated layouts.

## Rules

1. **Single source of truth:** `InvestigationResponse` from API; profiles never invent metrics, user counts, or regions.
2. **Omission vs fabrication:** Stakeholder view may hide technical fields or show `"unknown"` for impact not in the aggregate.
3. **Slice 2 implementation:** Profile selection is **client-side** in `aveniq_web` (toggle). API may add optional `?profile=` on GET later without changing the aggregate body.
4. **GenUI (Phase 3):** Profiles become inputs to composition; this LLD defines the static mapping baseline.

## Field visibility (v1)

| Region | engineer | lead | stakeholder |
|--------|----------|------|-------------|
| Signal / service | show | show | show |
| Evidence list (full) | show | abbreviated count + top items | hide |
| Hypotheses (full) | show | status + statement | hide |
| RCA claims + evidence_ids | show | root cause + status | root cause summary only |
| Events / connector metadata | show | hide | hide |

## Cross-references

- OpenAPI: [api/openapi.yaml](../api/openapi.yaml) `InvestigationResponse`
- Playground: [10-playground-orchestration.md](10-playground-orchestration.md)
