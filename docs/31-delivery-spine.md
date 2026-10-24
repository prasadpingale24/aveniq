# AVENIQ — Delivery spine (execution order)

## What this document is

**Execution order** for building and validating AVENIQ: each milestone completes a **visible user journey** (screens + API behavior) so progress can be corrected early.

| Document | Role |
|----------|------|
| **[25-roadmap.md](25-roadmap.md)** | Product **hypotheses** and capability themes (“does X earn complexity?”). **Not** the implementation schedule. |
| **This spine** | **What to build next**, in journey order. |
| **[engineering/00-delivery-spine.md](../engineering/00-delivery-spine.md)** | Milestone specs, acceptance pointers, legacy slice ID map. |
| **ADRs** | Durable decisions; milestones **implement** ADRs, they do not replace them. |

Milestone IDs (`M0`, `M1`, …) are **labels only**—no fixed count. New milestones may be inserted (e.g. between shell and playground) without renumbering the roadmap’s “Phase N.”

---

## Environments (same app, different wiring)

| Environment | User expectation | Typical differences |
|-------------|------------------|---------------------|
| **Local dev** | Full **application** on the laptop: UI, API, **sign-in** (dev-friendly IdP or local accounts), fixture/stand-in data, fast reload. | Not “open anonymous API only.” Playground is a **feature inside the app**, not a separate security mode. |
| **Staging preview** | Shared **preview** for PoC/demo: same app shape as local, persistent data, **realistic integration config** (API keys, connector endpoints), stricter TLS/secrets handling. | Differences are **data and integrations**, not a different product with auth only at the edge. |
| **Production** (later) | Hardened multi-tenant operations, compliance, scale. | Granular RBAC, retention, SLOs—not “first time users log in.” |

See [engineering/05-local-vs-staging.md](../engineering/05-local-vs-staging.md) for compose/env variables; this spine **reorders when** auth and staging land relative to UI journeys.

---

## Primary journey (north star)

From [06-user-journeys.md](06-user-journeys.md) — alert-driven investigation, simplified for PoC:

```text
Sign in (session)
  → Enter app (shell)
  → Start or open investigation (Playground and/or Incidents)
  → Run / watch investigation
  → Review evidence, hypotheses, RCA (persona views)
  → (Later) Answer agent question, export artifacts
```

Milestones below are cut so each step is **demoable in the UI** before piling on agentic or live-connector breadth.

---

## Milestones

Status: **Done** | **In progress** | **Specified** | **Planned**

### M0 — Evidence core (Done)

**Journey slice:** API-only investigation for B03; golden tests.

**Outcome:** Trustworthy deterministic RCA on fixtures.

**Legacy:** Engineering slices 0–1.

---

### M1 — Demo stack (Done)

**Journey slice:** Operator runs benchmark via Compose / Playground API; minimal web.

**Outcome:** Repeatable B03 path for outsiders; stand-in + fixtures.

**Legacy:** Slice 2, [06-slice-2-playground-compose.md](../engineering/06-slice-2-playground-compose.md).

---

### M2 — Application shell (Done)

**Journey slice:** User opens the product and recognizes **one app** (nav, tokens, routes)—even before login is mandatory everywhere.

**Screens:** Shell chrome per [07-application-surface.md](../engineering/07-application-surface.md); routes scaffold (`/playground`, `/investigations/:id` stub).

**Validate:** Build passes; dark Telemetry Monolith canvas; persona toggle moves client state (ADR-019).

**Legacy spec:** [08-slice-3a-design-foundation.md](../engineering/08-slice-3a-design-foundation.md).

---

### M3 — Dev session & identity (Done)

**Journey slice:** Engineer **signs in locally** and uses the app as a identified principal—not anonymous-only API.

**Screens:** Login / callback (or dev SSO page); protected shell; sign-out.

**Backend:** Map session → `actor.kind=user` (ADR-018); optional single-org membership; coarse roles later (not full Phase-7 matrix).

**Validate:** Login → Playground or investigation → events show user actor; refresh/session behavior documented.

**Supersedes:** ADR-016 table row “no auth 3a–3c” as **delivery order** (auth follows shell, precedes full journey polish). Identity log §5 applies here.

**Not in scope:** Public sign-up product, multi-tenant admin, connector secret vault UI.

---

### M4 — Playground journey end-to-end (Done)

**Journey slice:** Signed-in user runs a scenario and **lands on the investigation** with clear progress (runner + log).

**Screens:** `scr-playground-01` visual parity.

**Validate:** Click path Playground → run B03 → open investigation id; matches Stitch layout reasonably.

**Spec:** [09-milestone-m4-playground-ui.md](../engineering/09-milestone-m4-playground-ui.md).

---

### M5 — Investigation workspace end-to-end (Done)

**Journey slice:** User reviews **signal → evidence → hypotheses → RCA** in workspace; switches persona toggle (presentation only, ADR-019).

**Screens:** `scr-investigation-eng-02`, `lead-03`, `stake-04`; error/empty states `scr-states-sheet-07`.

**Validate:** Same API payload; three profiles; loading/blocked/inconclusive states.

**Spec:** [10-milestone-m5-investigation-ui.md](../engineering/10-milestone-m5-investigation-ui.md).

**Legacy:** Was “slice 3c”.

---

### M6 — Incidents inbox journey (Done)

**Journey slice:** User opens **Incidents**, picks a row, enters workspace—not only via Playground.

**Screens:** `scr-incidents-inbox-05`.

**API:** List/filter investigations (scoped by org, ADR-017).

**Validate:** Inbox → detail → same M5 workspace.

**Spec:** [12-milestone-m6-incidents-inbox.md](../engineering/12-milestone-m6-incidents-inbox.md).

---

### M7 — Staging preview environment

**Journey slice:** Deploy **same app** to VPS preview; demo with persistence and integration configuration.

**Infra:** `docker-compose.staging.yml`, TLS, secrets; connector mode may move toward live.

**Auth:** Same session model as M3—not “anonymous app behind basic auth only” (identity log §4).

**Validate:** Staging URL: sign in, run investigation, data survives redeploy (per [05-local-vs-staging.md](../engineering/05-local-vs-staging.md)).

---

### M8 — Human clarification loop

**Journey slice:** Agent asks; human answers in UI; investigation continues.

**Screens:** `scr-hitl-question-06`.

**Depends:** Agentic investigation milestone (roadmap “Phase 2” theme)—schedule after M5 or in parallel once API exists.

---

### M9+ — Earned complexity (roadmap themes, not sequential phases)

Insert milestones when hypotheses warrant; examples:

| Theme (see 25-roadmap) | Example milestone |
|------------------------|-------------------|
| Agentic vs deterministic | Iterative investigator, reliability metrics |
| Generative UI | Dynamic layout selection (ADR-006) |
| Live connector breadth | Slice 2b stand-in → real observability |
| MCP | Tool discovery, permission boundaries |
| Post-incident knowledge | Reports, articles (audience at export time) |
| Authorization depth | Org RBAC matrix (identity log §6), audit, retention |

---

## Identity & access vs milestones

| Topic | ADR | Milestone |
|-------|-----|-----------|
| Tenancy defaults | 017 | M0+ (done); enforce on list/get with M3/M6 |
| Event actor shape | 018 | M0+ (done); `user` actors from M3 |
| Profile ≠ role | 019 | M2–M5 UI |
| Session mechanism | TBD ADR | **M3** |
| Staging exposure | TBD ADR | **M7** |
| Granular RBAC | TBD ADR | **M9+** |

Pending items in [30-identity-access-decisions.md](30-identity-access-decisions.md) §4–§6 are **scheduled by milestone**, not by old “Phase 7.”

---

## How to use this spine

1. Pick the **first incomplete milestone** top to bottom (today: **M2** implementation, then **M3**).
2. Write or refresh **one engineering milestone spec** before large coding (pattern: [08-slice-3a-design-foundation.md](../engineering/08-slice-3a-design-foundation.md)).
3. Mark milestone **Done** in [engineering/README.md](../engineering/README.md) when acceptance passes.
4. Revisit **25-roadmap** only to check hypothesis fit—not to infer build order.

---

## Related

- [29-ui-program.md](29-ui-program.md) — UI principles (points here for schedule)
- [30-identity-access-decisions.md](30-identity-access-decisions.md)
- [07-application-surface.md](../engineering/07-application-surface.md)
