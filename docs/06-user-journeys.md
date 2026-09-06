# AVENIQ — User Journeys

## 1. Purpose

This document describes how users are expected to interact with AVENIQ during and after a production incident.

The journeys intentionally describe **user intent and system behavior**, not implementation details.

---

# 2. Primary Journey — Alert-Driven Investigation

The primary journey begins when an alert or incident signal is available.

```text
Alert
  ↓
Incident initialization
  ↓
Context discovery
  ↓
Evidence aggregation
  ↓
Investigation
  ↓
Hypothesis formation
  ↓
Verification
  ↓
RCA
  ↓
Resolution verification
  ↓
Post-incident artifacts
```

---

## 3. Step 1 — Incident Initialization

The engineer provides or selects an incident.

Possible entry points:

* alert
* incident-management event
* monitoring notification
* manually created investigation

AVENIQ establishes an initial investigation boundary:

* start time
* affected service, if known
* alert condition
* available metadata
* environment
* known severity

The initial context does not need to be complete.

---

## 4. Step 2 — Initial Context Discovery

AVENIQ investigates the initial signal.

It may search for:

* related logs
* anomalous metrics
* traces
* service relationships
* recent deployments
* configuration changes
* infrastructure events
* related alerts
* known incidents

The system should prioritize **relevance** rather than retrieving every available record.

---

## 5. Step 3 — Evidence Aggregation

Evidence from different sources is normalized into the incident context.

For example:

```text
Alert
  │
  ├── Error logs
  │
  ├── Latency anomaly
  │
  ├── Deployment
  │
  ├── Database metrics
  │
  └── Trace relationships
```

The user should not need to manually visit every source simply to establish these relationships.

---

## 6. Step 4 — Investigation

The agent determines what should be investigated next.

Example:

```text
Observed:
API errors increased.

Question:
Which component is producing the errors?

Action:
Search service-level error logs.

Result:
checkout-api shows a sharp increase.

Next question:
What changed immediately before this?

Action:
Inspect deployments.

Result:
checkout-api v2.8.1 deployed 4 minutes before anomaly.
```

Investigation is therefore a sequence of **questions, actions, observations, and conclusions**.

---

## 7. Step 5 — Hypothesis Formation

Once enough evidence exists, the system can construct candidate explanations.

Example:

```text
H1:
Recent deployment caused database connection exhaustion.

H2:
Database infrastructure degradation caused connection exhaustion.

H3:
Traffic spike independently caused connection exhaustion.
```

Multiple hypotheses should remain possible until evidence distinguishes them.

---

## 8. Step 6 — Verification

The system attempts to find evidence that:

* supports a hypothesis
* contradicts a hypothesis
* distinguishes competing hypotheses

For example:

```text
H1 support:
Deployment changed connection pool configuration.

H1 support:
Connection utilization increased immediately afterward.

H1 support:
Connection acquisition failures appeared afterward.

H2 contradiction:
Database infrastructure metrics remained normal.

H3 contradiction:
Traffic volume did not increase significantly.
```

The goal is not merely to produce the most plausible story.

The goal is to establish why one explanation is better supported.

---

## 9. Step 7 — Human Question

If investigation reaches an ambiguity that available telemetry cannot resolve, AVENIQ may ask the engineer.

Example:

> "I found two plausible causes. The affected errors appear restricted to the EU region. Was there a regional deployment or configuration change around 14:20?"

The answer becomes part of the investigation context and should be distinguishable from automatically observed evidence.

---

## 10. Step 8 — RCA

Once evidence is sufficient, AVENIQ produces an RCA candidate.

The RCA should include:

* root cause
* contributing factors
* affected components
* supporting evidence
* contradictory evidence, if relevant
* impact
* uncertainty
* remediation

The system should avoid presenting unsupported inference as established fact.

---

## 11. Step 9 — Resolution Verification

After remediation, AVENIQ should be able to compare the incident state before and after the intervention.

Potential checks:

* error rate returned to baseline
* latency returned to baseline
* affected dependency recovered
* relevant logs stopped
* affected requests succeed
* deployment/configuration state changed as expected

Resolution should therefore be treated as another verification problem.

---

# 12. Step 10 — Post-Incident Artifacts

The accumulated investigation context can be used to generate:

* incident timeline
* RCA report
* impact summary
* remediation summary
* observability recommendations
* knowledge article

These artifacts should be generated from the investigation record rather than reconstructed from memory.

---

# 13. Alternative Journey — No Alert

An important secondary entry point is:

> "Something seems wrong, but no alert fired."

The engineer can start an investigation manually.

For example:

> "Customers are reporting slow checkout in Europe."

AVENIQ then establishes an investigation timeframe and searches for anomalies around the described symptom.

This allows the product to explore whether the same investigation model can support **symptom-driven investigation**, not only alert-driven response.

---

# 14. Alternative Journey — Engineer-Led Investigation

The engineer may already know something important.

For example:

> "I suspect yesterday's deployment caused this."

AVENIQ should incorporate the hypothesis rather than restarting from zero.

The investigation becomes:

```text
Human hypothesis
       ↓
Evidence search
       ↓
Support / contradict
       ↓
Refine
       ↓
Conclusion
```

---

# 15. Post-Resolution Knowledge Journey

The investigation does not necessarily end with the RCA.

AVENIQ can identify:

```text
Incident
   ↓
Root cause
   ↓
Why observability did / did not detect it
   ↓
What signal was missing
   ↓
Recommended instrumentation
   ↓
Knowledge article
```

This creates a feedback loop between incidents and observability maturity.

---

# 16. Desired User Experience

The ideal journey should feel less like:

> "Open five tools and manually correlate information."

and more like:

> "Start an investigation, let AVENIQ gather the relevant context, inspect the evidence, answer questions when necessary, and review the resulting explanation."

The engineer remains able to intervene at any point.
