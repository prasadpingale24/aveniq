# Identity & access — decision log

Running record of **approved** identity, tenancy, and auth choices. Engineering ADRs are authoritative for implementation; this doc prevents drift during Q&A before ADRs are written.

## How this relates to slices

| Layer | Purpose |
|-------|---------|
| **This log + ADRs** | Decide and record *what* and *why* (identity, tenancy, auth phasing). |
| **Slice specs** (`08-slice-3a-…`, staging slice, Phase 7, etc.) | *When* and *acceptance* for implementation in the repo. |

Decisions here **do not** mean “implement everything now.” Some groundwork may land early in code (e.g. tenancy defaults, event `actor`); that is opportunistic alignment, not a substitute for milestone delivery. **Do not revert** early code solely to match milestone order.

**Execution order:** [31-delivery-spine.md](31-delivery-spine.md) (ADR-021). **Phasing context:** [ADR-016](../engineering/adrs/016-product-surface-and-ui-phasing.md) (auth *timing* table superseded for build order by ADR-021), [29-ui-program.md](29-ui-program.md), [19-security.md](19-security.md).

---

## 1. Tenancy & investigation isolation — **Accepted** (2026-10-03)

**Choice:** Logical boundary in the app, **org-primary** (B leaning D).

| Topic | Decision |
|-------|----------|
| Primary key | `org_id` on every investigation (non-null after create) |
| Secondary | `environment_id` defaulted for Playground; meaningful for env-separated telemetry later |
| Local defaults | `org_id = local`, `environment_id = playground` when omitted |
| Enforcement | Scope on all new list queries; GET-by-id scope check when staging auth lands |
| Rejected | Global pool (A); env-only boundary (C) as primary |

**ADR:** [017-investigation-tenancy-and-isolation.md](../engineering/adrs/017-investigation-tenancy-and-isolation.md)

---

## 2. Actor & attribution — **Accepted** (2026-10-03)

**Choice:** **2B** — structured `actor` `{ kind, id, display? }` on mutating investigation events.

| Topic | Decision |
|-------|----------|
| HTTP default | `anonymous` / `local`; optional `X-Actor-Id` (not security until auth) |
| Playground orchestration | `service` / `playground-runner` |
| B03 playbook events | `service` / `investigator-b03` |
| Storage | Wrapped `payload_json`; legacy flat payloads supported |

**ADR:** [018-actor-attribution.md](../engineering/adrs/018-actor-attribution.md)

---

## 3. Persona vs role — **Accepted** (2026-10-03)

**Choice:** **3A** — presentation profile is client-only; authorization gates API actions/resources, not layout.

| Topic | Decision |
|-------|----------|
| UI toggle / `?profile=` | Presentation only (Slices 3a–3c); not permission, not `actor` |
| API v1 | Same `InvestigationResponse` for all profiles; read access = full aggregate |
| Later | Optional `suggested_profile`; export audience separate (Phase 6+) |
| Rejected | Profile = role (3C); server-enforced profile for live UI (3D) |

**ADR:** [019-presentation-profile-not-authorization.md](../engineering/adrs/019-presentation-profile-not-authorization.md)

---

## 4. Staging exposure & auth — *scheduled by spine*

**Do not finalize as orphan ADRs.** Cover in milestone **M7** (staging preview): same session model as local dev, TLS, integrations/API keys. Draft options (OIDC at edge vs in-app) belong in `11-milestone-m7-staging-preview.md` when scheduled.

## 5. App session mechanism — **Accepted via M3** (2026-10-04)

**Choice:** Dev credential login + HttpOnly session cookie; compose web nginx `/api` proxy (same-origin); in-memory sessions; `AUTH_ENABLED` off in CI/tests.

**ADR:** [022-dev-session-m3.md](../engineering/adrs/022-dev-session-m3.md) · Spec: [11-milestone-m3-dev-session.md](../engineering/11-milestone-m3-dev-session.md)

## 6. Granular RBAC — *scheduled by spine*

**M9+** (authorization depth): org-scoped roles (see draft 6B in prior Q&A). Not “first login.” Depends on M3 principal + ADR-017 scope enforcement on list/get.
