# AVENIQ — Evidence Model

## 1. Purpose

Evidence is the foundation of AVENIQ.

The system's central reliability principle is:

> **A conclusion should be traceable to the evidence that supports it.**

This document defines the conceptual structure of evidence and how it should relate to observations, claims, hypotheses, and RCA.

---

# 2. What Counts as Evidence?

Evidence is information that can materially contribute to an investigation.

Potential sources include:

* logs
* metrics
* traces
* alerts
* deployments
* configuration changes
* infrastructure events
* service metadata
* source-control events
* incident records
* human responses

Evidence does not automatically mean "proof."

A log line can be relevant without proving causality.

---

# 3. Evidence Types

## 3.1 Telemetry Evidence

Examples:

* log records
* metric observations
* trace spans
* profiles

---

## 3.2 Change Evidence

Examples:

* deployment
* configuration change
* feature-flag change
* infrastructure modification
* code change

---

## 3.3 Context Evidence

Examples:

* service ownership
* dependency relationships
* environment
* region
* version
* topology

---

## 3.4 Human Evidence

Information supplied by an engineer or operator.

Example:

> "The database migration was intentionally paused at 14:20."

Human evidence can be highly valuable but should remain distinguishable from automatically observed telemetry.

---

# 4. Evidence Provenance

Each evidence item should ideally contain:

```text
Evidence
├── source
├── source type
├── timestamp
├── entity
├── observation
├── query / retrieval context
├── environment
└── provenance metadata
```

The exact schema can evolve.

The important property is **inspectability**.

---

# 5. Evidence Strength

Not all evidence has equal strength.

A conceptual scale could include:

### Direct

The source directly records the observed event.

Example:

> Deployment system reports version 2.8.1 deployed at 14:29.

### Derived

The observation is deterministically calculated from source data.

Example:

> Error rate increased 18× compared with baseline.

### Correlated

Two independently observed events occur in a relevant relationship.

Example:

> Deployment occurred four minutes before error increase.

### Inferred

The system derives a relationship that is not directly recorded.

Example:

> Deployment likely contributed to connection exhaustion.

The distinction should remain visible where practical.

---

# 6. Evidence and Claims

Claims should reference supporting evidence.

Example:

```text
Claim:
"checkout-api began experiencing database connection failures at 14:32."

Evidence:
  E1 — application log errors
  E2 — connection utilization metric
  E3 — database connection rejection metric
```

A claim may have multiple evidence items.

---

# 7. Evidence Supporting and Contradicting

Evidence should be usable in both directions.

```text
Hypothesis:
Deployment caused connection exhaustion.

Supporting:
  E1 — configuration changed
  E2 — connection pool increased
  E3 — exhaustion began afterward

Contradicting:
  E4 — identical deployment in another region did not fail
```

This creates a more realistic investigation model than simply collecting evidence that agrees with the first hypothesis.

---

# 8. Evidence Relationships

Potential relationships include:

```text
supports
contradicts
precedes
follows
causes? 
affects
belongs_to
originates_from
correlates_with
```

Importantly, the system should distinguish **observed relationships** from **inferred causal relationships**.

For example:

```text
deployment
   ──occurred_before──>
error spike
```

is different from:

```text
deployment
   ──caused──>
error spike
```

The latter requires stronger evidence.

---

# 9. Evidence Graph

Conceptually:

```text
                    Incident
                       │
            ┌──────────┼──────────┐
            ↓          ↓          ↓
          Alert      Service    Timeframe
                       │
             ┌─────────┼─────────┐
             ↓         ↓         ↓
           Logs      Metrics    Traces
             │         │         │
             └─────────┼─────────┘
                       ↓
                  Observations
                       ↓
                   Hypotheses
                       ↓
                    Claims
                       ↓
                      RCA
```

This does not require a graph database.

It represents the logical relationships required by the product.

---

# 10. Evidence Coverage

An RCA should ideally have evidence covering multiple relevant dimensions.

For example:

```text
Temporal evidence
    +
Service evidence
    +
Telemetry evidence
    +
Change evidence
    +
Impact evidence
```

A single error log should generally not be treated as sufficient evidence for a system-level RCA.

---

# 11. Evidence Gaps

The absence of evidence should be represented explicitly.

Examples:

> "Distributed tracing unavailable for this service."

> "No deployment metadata available."

> "User-region information unavailable."

Evidence gaps are themselves valuable because they identify limitations in the investigation.

---

# 12. Evidence Freshness

Evidence may change in relevance over time.

The model should preserve:

* event time
* retrieval time
* source update time where applicable

This matters because an investigation may continue after an incident has been resolved.

---

# 13. Evidence Confidence vs Model Confidence

AVENIQ should avoid reducing evidence quality to a single model confidence score.

Instead:

```text
Evidence quality
    +
Evidence coverage
    +
Source reliability
    +
Temporal consistency
    +
Cross-source agreement
    +
Contradictions
```

can contribute to an overall assessment of how strongly a conclusion is supported.

The exact scoring model should be established experimentally.

---

# 14. Evidence as the Foundation of Generated Artifacts

The same evidence model should support:

```text
Evidence
   ↓
Investigation
   ↓
RCA
   ↓
Incident report
   ↓
Knowledge article
```

This avoids a situation where the RCA is generated from one context and the postmortem is separately generated from another.

---

# 15. Core Principle

The desired relationship is:

> **Every important conclusion should have an inspectable path back to the evidence from which it was derived.**

AVENIQ should make it possible for an engineer to ask:

> **"Why does the system believe this?"**

and receive not merely a confidence score, but the relevant evidence and relationships.
