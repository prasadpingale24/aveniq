# AVENIQ — Architecture & Product Decisions

> This document records important decisions, their rationale, and what would cause them to be revisited.

---

## 1. Why This Exists

AVENIQ is an experimental project.

Some architectural decisions will eventually be proven wrong.

This document prevents the project from losing the reasoning behind those decisions.

A decision should therefore record:

* what was decided
* why it was decided
* what alternatives existed
* what assumptions it depends on
* whether it is reversible

---

# 2. Decision Status

Decisions use the following states:

| Status       | Meaning                          |
| ------------ | -------------------------------- |
| Proposed     | Under consideration              |
| Accepted     | Currently guiding implementation |
| Experimental | Being tested                     |
| Superseded   | Replaced by another decision     |
| Rejected     | Explicitly ruled out             |

---

# 3. Decision Record Format

```text
Decision:
Context:
Alternatives:
Chosen approach:
Reason:
Trade-offs:
Assumptions:
Revisit when:
Status:
```

---

# 4. ADR-001 — Evidence First

### Decision

AVENIQ will treat evidence and investigation context as first-class objects rather than generating an RCA directly from raw telemetry.

### Context

The core product requirement is reliability.

An AI-generated explanation without inspectable evidence is insufficient.

### Chosen Approach

```text
Data sources
    ↓
Evidence
    ↓
Investigation context
    ↓
Hypotheses
    ↓
RCA
```

### Alternatives

```text
Raw telemetry
    ↓
LLM
    ↓
RCA
```

### Reason

The evidence-first approach makes conclusions inspectable and allows reliability to be evaluated independently of language quality.

### Status

Accepted.

---

# 5. ADR-002 — Existing Tools Are Sources, Not Replacements

### Decision

AVENIQ will initially integrate with existing observability and operational systems rather than attempting to replace them.

### Reason

The problem being explored is context fragmentation, not the absence of observability tools.

### Status

Accepted.

---

# 6. ADR-003 — Tracing Is Valuable but Not Mandatory

### Decision

Distributed tracing should be used when available but should not be a hard dependency for investigation.

### Reason

Many environments have incomplete or absent trace propagation.

The system should still correlate:

* logs
* metrics
* deployments
* timestamps
* services
* infrastructure metadata

### Status

Accepted.

---

# 7. ADR-004 — Agentic Investigation Is an Experiment

### Decision

Agents are part of the architecture, but their superiority over deterministic investigation must be demonstrated experimentally.

### Reason

Agentic systems introduce:

* cost
* latency
* unpredictability
* additional failure modes

The project should not assume that "agentic" automatically means better.

### Status

Experimental.

---

# 8. ADR-005 — Generative UI Is a Product Hypothesis

### Decision

Generative UI will be tested as a mechanism for adaptive incident investigation rather than treated as a purely visual feature.

### Reason

The hypothesis is that different incidents and users require different views.

### Status

Experimental.

---

# 9. ADR-006 — Constrained UI Components

### Decision

The MVP will use a controlled component library rather than unrestricted UI generation.

### Reason

This provides:

* predictable behavior
* easier testing
* security boundaries
* accessibility
* consistent interaction

### Status

Accepted for MVP.

---

# 10. ADR-007 — Read-First Agent Permissions

### Decision

The MVP will prioritize read-only operational access.

### Reason

Investigation and remediation are separate risk categories.

The first objective is to prove investigation value.

### Status

Accepted.

---

# 11. ADR-008 — Human as Investigation Collaborator

### Decision

Human interaction is not limited to final approval.

The system may ask targeted questions during investigation when the answer can materially change the outcome.

### Reason

Human operators possess contextual information that may not exist in machine-accessible systems.

### Status

Accepted.

---

# 12. ADR-009 — Graceful Uncertainty

### Decision

AVENIQ must be allowed to produce:

* probable RCA
* possible RCA
* inconclusive investigation
* evidence gaps

rather than forcing a definitive answer.

### Reason

False certainty is more dangerous than acknowledged uncertainty in an incident investigation system.

### Status

Accepted.

---

# 13. ADR-010 — Synthetic Before Real

### Decision

The initial investigation workflow should be validated using controlled benchmark incidents before investing heavily in real-world integrations.

### Reason

Otherwise, integration complexity can hide whether the core investigation model actually works.

### Status

Accepted.

---

# 14. Future Decisions

Important future decisions may include:

* model/provider selection
* deterministic vs agentic routing
* agent decomposition
* evidence storage architecture
* vector search requirements
* MCP adoption strategy
* streaming architecture
* multi-tenancy
* production remediation permissions

These should be recorded when enough evidence exists to make them meaningful.

---

# 15. Decision Principle

> **Document why a decision was made, not just what was built.**
