# AVENIQ — Architecture

## 1. Purpose

This document describes the conceptual architecture of AVENIQ.

The architecture is designed around one central idea:

> **Aggregate evidence from existing operational systems, use agents to investigate that evidence, and dynamically present the resulting incident context to the user.**

AVENIQ is not intended to become another observability platform.

It sits above existing systems and assists with investigation.

---

# 2. Architectural Goal

The architecture should enable this workflow:

```text
Incident Signal
      ↓
Incident Context
      ↓
Evidence Aggregation
      ↓
Agentic Investigation
      ↓
Evidence Correlation
      ↓
Hypothesis Verification
      ↓
Evidence-backed RCA
      ↓
Personalized Generative UI
      ↓
Incident Report / Knowledge
```

---

# 3. High-Level Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                         AVENIQ                              │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                    Experience Layer                   │  │
│  │                                                       │  │
│  │  Generative UI  ←→  Conversational Interface         │  │
│  └───────────────────────────┬───────────────────────────┘  │
│                              │                              │
│  ┌───────────────────────────▼───────────────────────────┐  │
│  │              Investigation Orchestrator               │  │
│  │                                                       │  │
│  │  Objective → Plan → Investigate → Verify → Conclude │  │
│  └──────────────┬────────────────────┬───────────────────┘  │
│                 │                    │                      │
│        ┌────────▼────────┐   ┌──────▼─────────────┐        │
│        │ Agent / Reasoning│   │ Human Interaction  │        │
│        │ Capabilities     │   │                    │        │
│        └────────┬────────┘   └────────────────────┘        │
│                 │                                           │
│  ┌──────────────▼────────────────────────────────────────┐  │
│  │             Investigation Context Layer              │  │
│  │                                                       │  │
│  │  Incident Context │ Evidence │ Hypotheses │ Timeline │  │
│  │  Impact           │ Gaps     │ Provenance │ History  │  │
│  └──────────────┬────────────────────────────────────────┘  │
│                 │                                           │
│  ┌──────────────▼────────────────────────────────────────┐  │
│  │                  Tool / MCP Layer                     │  │
│  │                                                       │  │
│  │ Logs │ Metrics │ Traces │ Deployments │ Infra │ SCM  │  │
│  └──────────────┬────────────────────────────────────────┘  │
└─────────────────┼───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                  Existing Engineering Systems               │
│                                                             │
│ Observability │ Cloud │ Kubernetes │ CI/CD │ Git │ Alerts │
└─────────────────────────────────────────────────────────────┘
```

---

# 4. Architectural Layers

## 4.1 Experience Layer

Responsible for how users interact with an investigation.

It contains:

* conversational interface
* generative UI
* investigation timeline
* evidence views
* hypothesis views
* RCA
* incident report

The UI should reflect investigation state rather than become the source of truth.

---

# 5. Investigation Orchestrator

The orchestrator manages the investigation lifecycle.

Conceptually:

```text
Objective
   ↓
Understand context
   ↓
Identify evidence gaps
   ↓
Select investigation action
   ↓
Retrieve evidence
   ↓
Update context
   ↓
Evaluate hypotheses
   ↓
Verify / investigate further
   ↓
Conclude
```

The orchestrator should be able to pause and resume investigations.

---

# 6. Agent Layer

Agents perform specialized investigation tasks.

Possible capabilities include:

```text
Context Analysis
Evidence Retrieval
Correlation
Hypothesis Generation
Hypothesis Verification
Impact Analysis
Observability Analysis
Report Generation
```

The MVP should avoid prematurely committing to a large number of independent agents.

Agent decomposition should be driven by experiments.

---

# 7. Investigation Context Layer

This is the architectural center of AVENIQ.

It provides a structured representation of the investigation.

Conceptually:

```text
Investigation
├── Incident
├── Time Window
├── Services
├── Dependencies
├── Changes
├── Evidence
├── Hypotheses
├── Timeline
├── Impact
├── Questions
├── Evidence Gaps
└── Conclusions
```

Agents should operate on this context rather than passing unstructured text between themselves wherever possible.

---

# 8. Evidence Layer

The evidence layer normalizes information obtained from external systems.

A conceptual evidence object:

```text
Evidence
├── ID
├── Source
├── Timestamp
├── Entity
├── Observation
├── Provenance
├── Reliability metadata
└── Relationships
```

The exact schema is defined separately in `evidence-model.md`.

---

# 9. Hypothesis Layer

The investigation should maintain multiple hypotheses when appropriate.

Example:

```text
H1 — Recent deployment caused regression
H2 — Database degradation caused downstream failures
H3 — Regional infrastructure issue caused both
```

Each hypothesis can have:

```text
Supporting evidence
Contradicting evidence
Missing evidence
Verification status
```

This reduces the tendency to lock onto the first plausible explanation.

---

# 10. Tool / MCP Layer

This layer provides access to external systems.

Potential capabilities:

```text
query_logs()
query_metrics()
query_traces()
get_deployments()
get_service_metadata()
get_alert()
get_configuration_change()
```

MCP is one mechanism for exposing these capabilities.

The investigation architecture should remain independent of MCP itself.

---

# 11. External Systems

AVENIQ should integrate with existing systems rather than duplicate them.

Examples:

```text
Observability
    Logs
    Metrics
    Traces

Infrastructure
    Kubernetes
    Cloud resources

Change
    Git
    CI/CD
    Deployments
    Configuration

Incident
    Alerts
    Incident management
```

---

# 12. Data Flow

A typical investigation might follow:

```text
Alert
 ↓
Create Investigation
 ↓
Establish Time Window
 ↓
Identify Affected Service
 ↓
Query Metrics
 ↓
Query Logs
 ↓
Inspect Changes
 ↓
Inspect Dependencies
 ↓
Correlate Evidence
 ↓
Generate Hypotheses
 ↓
Verify Hypotheses
 ↓
Determine Impact
 ↓
Produce RCA
```

Not every investigation should follow this exact sequence.

The agent should be able to adapt the investigation based on evidence.

---

# 13. Incident With Tracing

When tracing exists:

```text
Alert
 ↓
Service
 ↓
Trace
 ↓
Downstream Span
 ↓
Dependency
 ↓
Relevant Logs / Metrics
```

Trace IDs can provide strong correlation.

---

# 14. Incident Without Tracing

When tracing does not exist:

```text
Alert
 ↓
Time Window
 ↓
Service
 ↓
Metrics
 ↓
Logs
 ↓
Deployment
 ↓
Dependency
 ↓
Temporal / Entity Correlation
```

The architecture must support both.

---

# 15. Evidence Flow

A critical architectural distinction:

```text
External System
      ↓
Raw Observation
      ↓
Normalized Evidence
      ↓
Investigation Context
      ↓
Hypothesis
      ↓
RCA Claim
```

This enables the system to answer:

> "Why did AVENIQ reach this conclusion?"

by traversing backward through the evidence chain.

---

# 16. Generative UI Flow

The UI is generated from structured context.

```text
Investigation Context
        +
User Role
        +
Investigation State
        ↓
Component Selection
        ↓
Layout Composition
        ↓
Data Binding
        ↓
Investigation View
```

The UI should not invent evidence.

---

# 17. Example

Suppose the investigation discovers:

```text
Service:
checkout-api

Symptoms:
HTTP 500 ↑

Change:
Deployment 2026.09.06.4

Dependency:
PostgreSQL

Evidence:
Connection exhaustion
```

The generated UI may prioritize:

```text
Incident Summary
        ↓
Timeline
        ↓
Deployment Change
        ↓
Database Connection Metrics
        ↓
Relevant Error Logs
        ↓
Hypothesis
        ↓
Evidence
        ↓
RCA
```

A stakeholder may instead receive:

```text
Incident Summary
        ↓
Duration
        ↓
Affected Users
        ↓
Affected Region
        ↓
Business Impact
        ↓
Resolution
```

The underlying investigation context remains shared.

---

# 18. Post-Incident Flow

Once the investigation reaches a sufficient state:

```text
Investigation
      ↓
Evidence-backed RCA
      ↓
Incident Report
      ↓
Knowledge Article
      ↓
Observability Lessons
```

These outputs should be generated from structured investigation data rather than independently regenerated from scratch.

---

# 19. Storage

The MVP may require storage for:

* investigations
* evidence metadata
* hypotheses
* investigation events
* generated artifacts
* user interaction

The storage architecture should remain deliberately simple until workload characteristics are known.

---

# 20. Model Layer

LLMs should be treated as reasoning components rather than sources of truth.

Conceptually:

```text
Evidence / Context
       ↓
LLM reasoning
       ↓
Structured decision
       ↓
Evidence / Context update
```

The model should not be the authoritative storage layer for investigation state.

---

# 21. Reliability Boundary

The architecture deliberately separates:

```text
Truth / Context
        │
        ▼
Evidence Layer
        │
        ▼
Reasoning Layer
        │
        ▼
Presentation Layer
```

This separation allows the system to distinguish:

* what was observed
* what was inferred
* what was presented

---

# 22. Security Boundary

Security controls should exist outside the model.

```text
User
 ↓
Authorization
 ↓
Investigation
 ↓
Tool Permission
 ↓
External System
```

The agent cannot grant itself additional permissions.

---

# 23. Read-First MVP

The initial architecture should support:

```text
Read telemetry
Read changes
Read metadata
Analyze
Correlate
Explain
```

rather than:

```text
Analyze
 ↓
Modify production
```

Production-changing actions are a future capability requiring separate safety design.

---

# 24. Architecture Evolution

The architecture should evolve through experiments.

Early:

```text
Single orchestrator
+
Small agent capability set
+
Controlled connectors
+
Constrained UI
```

Later, if justified:

```text
Orchestrator
├── Context Agent
├── Evidence Agent
├── Hypothesis Agent
├── Impact Agent
└── Report Agent
```

Complexity should be earned through demonstrated benefit.

---

# 25. Architectural Principles

1. **Evidence before explanation**
2. **Existing tools before replacement**
3. **Tracing when available, not when mandatory**
4. **Structured context over conversational memory**
5. **Agents as investigators, not sources of truth**
6. **Generative UI as a presentation layer**
7. **Human input as contextual evidence**
8. **Read-first operational access**
9. **Explicit uncertainty**
10. **Architecture driven by experiments**

---

# 26. One-Sentence Architecture

> **AVENIQ is an evidence-centric investigation layer over existing engineering systems, where agents dynamically gather and verify operational context and Generative UI presents that context according to the incident and the person investigating it.**
