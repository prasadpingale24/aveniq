# AVENIQ — Requirements

## 1. Purpose

This document defines the functional and non-functional requirements for AVENIQ.

Requirements are intentionally expressed independently of a specific implementation so that architecture decisions can evolve without redefining the product.

---

# 2. Functional Requirements

## FR-01 — Create an Investigation

AVENIQ shall allow an investigation to be initiated from:

* an alert
* an incident
* a manually supplied symptom
* a user question

---

## FR-02 — Establish an Investigation Context

The system shall maintain contextual information including, where available:

* incident timeframe
* environment
* services
* alerts
* telemetry
* changes
* dependencies
* affected entities
* user-provided information

---

## FR-03 — Acquire Evidence

The system shall be able to retrieve relevant evidence from connected data sources.

Evidence acquisition should be driven by investigation needs rather than indiscriminate retrieval.

---

## FR-04 — Correlate Evidence

The system shall associate evidence with relevant:

* services
* requests
* deployments
* infrastructure
* timestamps
* regions
* environments
* incidents

where such relationships can be established.

---

## FR-05 — Preserve Evidence Provenance

Evidence should retain enough provenance to determine:

* source
* retrieval context
* timestamp
* relevant entity
* original observation where appropriate

---

## FR-06 — Generate Hypotheses

The system shall be capable of generating one or more candidate explanations based on available evidence.

---

## FR-07 — Verify Hypotheses

The system shall attempt to find evidence that supports or contradicts candidate explanations.

---

## FR-08 — Represent Uncertainty

The system shall distinguish between:

* observed facts
* inferred relationships
* hypotheses
* unresolved questions
* human-provided information

---

## FR-09 — Ask Human Questions

The system shall be able to request clarification when available evidence is insufficient or ambiguous.

---

## FR-10 — Maintain Investigation History

The investigation shall retain:

* actions
* evidence
* hypotheses
* user responses
* agent reasoning artifacts appropriate for inspection
* conclusions
* unresolved questions

---

## FR-11 — Generate an RCA

AVENIQ shall produce an RCA representation containing evidence supporting the conclusion.

---

## FR-12 — Represent Impact

Where evidence permits, the system shall describe impact across relevant dimensions such as:

* services
* endpoints
* regions
* users
* business capabilities

---

## FR-13 — Generate Incident Artifacts

The system should be capable of generating:

* incident report
* timeline
* RCA summary
* knowledge article
* observability recommendations

---

## FR-14 — Generate Adaptive UI

The system shall be capable of producing an incident view based on:

* incident state
* investigation needs
* user role
* available evidence

---

## FR-15 — Support Multiple Data Sources

The system shall support data sources through connectors or MCP-compatible interfaces where appropriate.

---

# 3. Non-Functional Requirements

## NFR-01 — Reliability

The system should prioritize correctness and evidence quality over response speed.

---

## NFR-02 — Explainability

Important conclusions should be inspectable through their supporting evidence.

---

## NFR-03 — Graceful Degradation

The system should remain useful when individual evidence sources are unavailable.

---

## NFR-04 — Observability

AVENIQ itself should expose sufficient telemetry to diagnose failures in its investigation workflow.

---

## NFR-05 — Security

Connected operational data must be accessed using appropriate authentication, authorization, and least-privilege principles.

---

## NFR-06 — Data Isolation

Evidence belonging to one environment, organization, or investigation must not unintentionally leak into another context.

---

## NFR-07 — Auditability

Important agent actions and external data access should be auditable.

---

## NFR-08 — Extensibility

New data sources should be integrable without redesigning the investigation model.

---

## NFR-09 — Human Control

Users must be able to inspect, challenge, redirect, or stop an investigation.

---

## NFR-10 — Performance

The system should provide useful initial context quickly while allowing deeper investigation to continue asynchronously.

---

# 4. MVP Requirements

The first MVP should prioritize:

1. investigation creation
2. multiple evidence sources
3. evidence normalization
4. evidence provenance
5. agent-driven investigation
6. hypothesis generation
7. evidence-backed RCA
8. human questioning
9. basic adaptive incident UI

Post-incident generation can initially be simpler than the core investigation workflow.

---

# 5. Requirement Priority

| Priority | Meaning                                      |
| -------- | -------------------------------------------- |
| P0       | Essential to validate the product hypothesis |
| P1       | Important for a usable MVP                   |
| P2       | Valuable enhancement                         |
| P3       | Future exploration                           |

The priority of individual requirements should be revised as experiments produce evidence.
