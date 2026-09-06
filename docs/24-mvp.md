# AVENIQ — MVP

## 1. Purpose

The MVP exists to validate the core product hypothesis with the smallest system capable of demonstrating meaningful value.

The goal is not to build a production-ready observability platform.

The goal is to prove:

> **Can an evidence-first agentic investigation system reduce the manual effort required to reach a trustworthy RCA?**

---

# 2. MVP Scenario

The MVP should focus on a controlled incident environment.

Example:

```text
Alert
 ↓
AVENIQ investigation
 ↓
Multiple telemetry sources
 ↓
Agent gathers evidence
 ↓
Evidence correlation
 ↓
Hypotheses
 ↓
Verification
 ↓
Evidence-backed RCA
 ↓
Generated incident view
```

---

# 3. MVP Data Sources

A deliberately small set is preferable.

For example:

* logs
* metrics
* deployment/change events
* service metadata

Distributed tracing can be included where useful but should not be a hard dependency.

---

# 4. MVP Agent Capabilities

The agent should be able to:

1. inspect incident context
2. identify evidence gaps
3. query available sources
4. correlate observations
5. form hypotheses
6. seek contradictory evidence
7. ask the user a targeted question
8. produce an RCA candidate

---

# 5. MVP Evidence Layer

The evidence layer should provide:

* normalized evidence objects
* provenance
* timestamps
* source metadata
* relationships
* support/contradiction links

This is more important than building a sophisticated UI early.

---

# 6. MVP Generative UI

The MVP should use a constrained component library.

Potential components:

* incident summary
* timeline
* evidence cards
* logs
* metrics
* deployment changes
* hypothesis cards
* RCA
* evidence gaps
* human question

The system dynamically chooses which components to display.

---

# 7. MVP Human Interaction

The user should be able to:

* answer questions
* redirect investigation
* inspect evidence
* challenge a hypothesis
* request deeper investigation
* accept or reject an RCA candidate

---

# 8. MVP Post-Incident Output

The MVP should generate at least:

### RCA

Evidence-backed explanation.

### Incident Report

Timeline, impact, cause, remediation.

### Observability Lesson

What telemetry or instrumentation would have made the incident easier to detect or investigate.

Knowledge article generation can initially be derived from these structured outputs.

---

# 9. Explicitly Out of MVP

The MVP should not attempt to build:

* a complete observability platform
* autonomous production remediation
* universal MCP integration
* dozens of vendor connectors
* unrestricted UI generation
* enterprise compliance suite
* fully autonomous deployment
* generalized AIOps platform

---

# 10. MVP Architecture Boundary

```text
┌──────────────────────────────────────────┐
│                  AVENIQ                  │
│                                          │
│  UI                                      │
│   ↓                                      │
│  Investigation Orchestrator              │
│   ↓                                      │
│  Evidence / Context Layer                 │
│   ↓                                      │
│  Agentic Investigation                   │
│   ↓                                      │
│  Connectors / MCP                        │
└──────────────────────────────────────────┘
                 ↓
       Controlled data sources
```

---

# 11. MVP Success

The MVP is successful if a small set of realistic benchmark incidents demonstrates that AVENIQ can:

* find relevant evidence
* connect evidence across sources
* avoid obvious false conclusions
* explain its RCA
* identify uncertainty
* reduce investigation effort
* provide a more useful incident view than a static dashboard

---

# 12. MVP Failure Is Useful

The MVP should be considered successful as an experiment even if it proves:

> "Agentic investigation does not outperform a simpler deterministic approach for these incident classes."

That result would prevent unnecessary architectural complexity.

---

# 13. Core Principle

> **Build the smallest system that can falsify or validate the core hypothesis.**
