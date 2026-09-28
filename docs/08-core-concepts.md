# AVENIQ — Core Concepts

## 1. Purpose

This document establishes the vocabulary and conceptual model used throughout AVENIQ.

The purpose is to prevent implementation concepts from becoming confused with product concepts.

---

# 2. Incident

An **Incident** is the primary object being investigated.

It represents an operational event or suspected operational problem requiring investigation.

An incident may originate from:

* an alert
* a monitoring anomaly
* a user report
* an engineer observation
* a manually initiated investigation

An incident does not necessarily imply that the root cause is already known.

---

# 3. Incident Context

**Incident Context** is the accumulated representation of everything currently known or relevant to an investigation.

It may contain:

```text
Incident
├── timeframe
├── symptoms
├── entities
├── evidence
├── relationships
├── hypotheses
├── questions
├── human inputs
├── actions
├── impact
├── remediation
└── resolution state
```

Incident context evolves throughout the investigation.

---

# 4. Signal

A **Signal** is an indication that something may be relevant to an incident.

Examples:

* alert
* metric anomaly
* log pattern
* trace error
* deployment event
* user report

A signal is not necessarily evidence of root cause.

---

# 5. Evidence

**Evidence** is an observed or externally supplied piece of information that can be used to support or challenge an investigative claim.

Examples:

* metric observation
* log event
* trace span
* deployment record
* configuration change
* infrastructure event
* human confirmation

Evidence should have provenance.

---

# 6. Observation

An **Observation** is what the system can directly establish from an evidence source.

Example:

> "checkout-api error rate increased from 0.2% to 18% between 14:31 and 14:34."

This is different from:

> "The deployment caused the incident."

The first is an observation.

The second is a hypothesis or conclusion.

---

# 7. Relationship

A **Relationship** connects entities or evidence.

Examples:

```text
deployment
   ↓
service

service
   ↓
database

error
   ↓
request

request
   ↓
user region
```

Relationships may be:

* explicitly provided by a source
* deterministically derived
* inferred

The distinction should be preserved where relevant.

---

# 8. Hypothesis

A **Hypothesis** is a proposed explanation for observed behavior.

A hypothesis should not automatically become the RCA.

It must be evaluated against available evidence.

---

# 9. Claim

A **Claim** is a statement made during an investigation.

Examples:

* "The checkout API began failing at 14:32."
* "A deployment occurred three minutes before the failure."
* "The deployment changed database configuration."
* "The configuration change contributed to connection exhaustion."

Claims can have different evidence strength.

---

# 10. Verification

**Verification** is the process of determining whether a claim or hypothesis is sufficiently supported by available evidence.

Verification may involve:

* retrieving additional evidence
* comparing time windows
* checking dependencies
* finding contradictory observations
* asking a human
* reproducing a condition

---

# 11. Investigation

An **Investigation** is the sequence through which AVENIQ gathers context, asks questions, evaluates hypotheses, and develops an explanation for an incident.

Conceptually:

```text
Question
   ↓
Action
   ↓
Observation
   ↓
New question
   ↓
Evidence
   ↓
Hypothesis
   ↓
Verification
   ↓
Conclusion
```

---

# 12. Evidence Graph

The **Evidence Graph** represents relationships among:

* evidence
* entities
* observations
* claims
* hypotheses
* incident context

It is a conceptual model rather than necessarily a literal graph database.

---

# 13. RCA

**Root Cause Analysis (RCA)** is the resulting explanation of why the incident occurred.

An AVENIQ RCA should ideally include:

* primary cause
* contributing factors
* evidence
* impact
* uncertainty
* remediation

---

# 14. Blast Radius

**Blast Radius** describes the scope of impact associated with an incident.

It may include:

* services
* endpoints
* regions
* users
* requests
* business capabilities

Blast radius should be evidence-derived where possible.

---

# 15. Investigation State

An investigation has a changing state.

A conceptual state model:

```text
Initialized
    ↓
Context Gathering
    ↓
Investigating
    ↓
Hypothesis Formation
    ↓
Verification
    ↓
Human Clarification ──┐
    ↓                 │
    └─────────────────┘
    ↓
RCA Candidate
    ↓
Resolution Verification
    ↓
Resolved
    ↓
Post-Incident
```

The actual state machine may evolve during implementation.

---

# 16. Agent

An **Agent** is an autonomous system component capable of deciding investigation actions within a defined responsibility and tool boundary.

An agent is not equivalent to an LLM response.

An agent can:

* inspect context
* select tools
* retrieve evidence
* evaluate results
* decide next actions
* ask questions
* update investigation state

---

# 17. Tool

A **Tool** is an operation an agent can invoke.

Examples:

* query logs
* query metrics
* retrieve traces
* inspect deployments
* inspect service metadata

MCP may provide one mechanism for exposing such tools.

---

# 18. Connector

A **Connector** provides access to an external operational system.

Examples may include:

* observability platforms
* source-control systems
* deployment systems
* incident-management systems

AVENIQ should conceptually separate the connector from the investigation logic.

---

# 19. Generative UI

**Generative UI** is the ability to dynamically construct an interface based on the current investigation context and user needs.

It should not mean arbitrary AI-generated HTML.

The intended concept is:

```text
Incident context
      +
User perspective
      +
Investigation state
      ↓
Relevant UI composition
```

---

# 20. Knowledge

**Knowledge** is reusable information derived from resolved incidents.

Examples:

* known failure patterns
* diagnostic procedures
* observability lessons
* remediation patterns
* prevention recommendations

Knowledge should preserve its relationship to the incident evidence from which it was derived.

---

# 21. Core Principle

The conceptual hierarchy of AVENIQ is:

```text
Signals
   ↓
Evidence
   ↓
Context
   ↓
Investigation
   ↓
Hypotheses
   ↓
Verification
   ↓
RCA
   ↓
Knowledge
```

AI and agents operate **within this system**.

They are not the system itself.
