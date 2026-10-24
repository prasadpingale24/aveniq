# 00 — Delivery spine (engineering)

**Product-facing narrative:** [../docs/31-delivery-spine.md](../docs/31-delivery-spine.md)

This file tracks **milestone status**, links to acceptance specs, and maps **legacy slice names** so older docs remain readable.

## Milestone status

| ID | Name | Status | Acceptance / spec |
|----|------|--------|-------------------|
| M0 | Evidence core | **Done** | [03-slice-0.md](03-slice-0.md), [04-slice-1-b03.md](04-slice-1-b03.md) |
| M1 | Demo stack | **Done** | [06-slice-2-playground-compose.md](06-slice-2-playground-compose.md) |
| M2 | Application shell | **Done** | [08-slice-3a-design-foundation.md](08-slice-3a-design-foundation.md) |
| M3 | Dev session & identity | **Done** | [11-milestone-m3-dev-session.md](11-milestone-m3-dev-session.md) |
| M4 | Playground journey E2E | **Done** | [09-milestone-m4-playground-ui.md](09-milestone-m4-playground-ui.md) |
| M5 | Investigation workspace E2E | **Done** | [10-milestone-m5-investigation-ui.md](10-milestone-m5-investigation-ui.md) |
| M6 | Incidents inbox journey | **Done** | [12-milestone-m6-incidents-inbox.md](12-milestone-m6-incidents-inbox.md) |
| M7 | Staging preview environment | Planned | Spec TBD; [05-local-vs-staging.md](05-local-vs-staging.md) |
| M8 | Human clarification loop | Planned | Spec TBD |
| M9+ | Roadmap themes | Backlog | [../docs/25-roadmap.md](../docs/25-roadmap.md) |

## Legacy slice ID map

| Old label | Spine milestone |
|-----------|-----------------|
| Slice 0–1 | M0 |
| Slice 2 | M1 |
| Slice 3a | M2 |
| (auth deferred to Phase 7) | **M3** (dev session)—reordered per spine |
| Slice 3b | M4 |
| Slice 3c | M5 |
| Slice 4+ inbox | M6 |
| Staging auth “edge only” | **M7** (full app on staging) |
| Slice 2b live connectors | M9+ or parallel when scheduled |

## ADR interactions

| ADR | Note under spine |
|-----|------------------|
| 016 | UI program stands; **auth phasing table superseded for delivery order** by [021](adrs/021-delivery-spine-authority.md) |
| 017–019 | Remain valid; enforcement timing tied to M3/M6/M9+ |
| 020–022 | Not written; identity §4–§6 fold into M3/M7/M9+ specs |

## Document precedence (conflicts)

1. Milestone **acceptance spec** for the milestone in flight  
2. **ADRs** for decisions  
3. **LLD/OpenAPI** for contracts  
4. Roadmap **phase** documents for hypothesis scope only  
