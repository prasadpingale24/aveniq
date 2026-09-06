# AVENIQ — User Personas

## 1. Primary Persona — Small-Team Engineer

### Profile

An engineer working in a small engineering organization where one person may simultaneously act as:

* developer
* DevOps engineer
* on-call engineer
* infrastructure operator
* incident responder

They may have access to several observability tools but do not necessarily have dedicated SRE/observability specialists.

### Typical environment

```text
Application
   ↓
Basic metrics
Basic logs
Some alerts
Limited tracing
   ↓
Engineer investigates manually
```

### Problems

* limited time during incidents
* incomplete familiarity with every service
* fragmented operational information
* manual correlation
* context switching
* uncertainty about where to investigate next
* post-incident documentation burden

### What they value

* fast understanding
* simple investigation workflow
* useful defaults
* clear evidence
* minimal configuration
* ability to intervene when the system gets stuck

### AVENIQ value

> **Give a generalist engineer the investigative leverage of a more mature observability workflow without requiring them to become an expert in every underlying tool.**

---

# 2. Secondary Persona — Senior SRE / Observability Engineer

### Profile

An experienced engineer responsible for reliability across a larger or more complex system.

### Typical environment

```text
Multiple services
Multiple environments
Centralized telemetry
Distributed tracing
Kubernetes
CI/CD
Incident management
Multiple observability tools
```

### Problems

Their problem is less likely to be basic telemetry access.

Instead:

* telemetry volume is large
* incidents cross service boundaries
* investigations require many correlations
* existing tools contain the information but require manual navigation
* repeated investigations consume senior engineering time
* AI-generated RCA may not provide sufficient evidence

### What they value

* control
* evidence quality
* explainability
* investigation depth
* integration flexibility
* deterministic behavior where appropriate
* ability to inspect and challenge agent actions

### AVENIQ value

> **Reduce repetitive investigative work while preserving the depth and inspectability expected from experienced reliability engineers.**

---

# 3. Developer

### Profile

An engineer who is pulled into an incident because their service or recent change appears relevant.

### Problems

They need to understand:

* what changed
* whether their code is involved
* which requests failed
* what dependency is affected
* whether their change is causal or merely correlated

### What they value

* precise evidence
* relevant logs
* traces where available
* deployment/change context
* reproducible timelines
* clear relationship between symptoms and code changes

### AVENIQ value

> **Move from "your service is failing" to a concrete, evidence-backed explanation of how the service became involved.**

---

# 4. Technical Lead / Engineering Manager

### Profile

A person coordinating the response rather than performing every low-level investigation step.

### Problems

They need to understand:

* severity
* blast radius
* progress
* likely cause
* mitigation
* remaining uncertainty
* recurrence risk

without consuming every raw telemetry detail.

### What they value

* concise but trustworthy summaries
* impact visualization
* investigation progress
* evidence-backed RCA
* remediation status
* generated reports

### AVENIQ value

> **Provide a trustworthy understanding of the incident without requiring the manager to reproduce the engineer's entire investigation.**

---

# 5. Stakeholder

### Profile

A product, business, support, or operational stakeholder affected by the incident but not responsible for technical diagnosis.

### Problems

They generally do not need:

* raw logs
* trace IDs
* container metrics
* stack traces

They need:

* what happened
* who was affected
* which region/functionality was affected
* duration
* current status
* business impact

### AVENIQ value

> **Translate the same underlying incident evidence into an understandable impact-oriented view.**

---

# 6. Persona Comparison

| Persona             | Primary question                             | Relevant evidence                               |
| ------------------- | -------------------------------------------- | ----------------------------------------------- |
| Small-team engineer | "What is actually broken?"                   | logs, metrics, services, changes                |
| SRE                 | "What caused this across the system?"        | telemetry, dependencies, traces, infrastructure |
| Developer           | "Is my change responsible?"                  | deployments, code, logs, traces                 |
| Technical lead      | "What happened and how large is the impact?" | RCA, timeline, blast radius                     |
| Stakeholder         | "Who/what was affected?"                     | users, regions, functionality, duration         |

---

# 7. Shared Incident Context

These personas should **not** receive different underlying facts.

Instead:

```text
                 Shared Incident Context
                         │
        ┌────────────────┼────────────────┐
        ↓                ↓                ↓
     Engineer           Lead         Stakeholder
        │                │                │
    Technical          Impact          Business
      view              view             view
```

The evidence remains shared.

The presentation changes.

This distinction is important because AVENIQ's generative UI should personalize **representation**, not manufacture different realities.

---

# 8. Initial Target Persona

The initial MVP should primarily target:

> **A small engineering team with a production application, basic-to-moderate observability, and engineers who regularly perform incident investigation themselves.**

This provides a practical validation environment.

If AVENIQ cannot demonstrate meaningful value in this relatively constrained environment, increasing complexity and enterprise integrations should not be assumed to solve the fundamental problem.

---

# 9. Persona Assumptions to Validate

The following are currently hypotheses:

* small teams experience enough investigation friction to seek assistance
* engineers will trust an agent more if evidence is inspectable
* engineers are willing to let an agent perform investigation steps autonomously
* conversational investigation is preferable to a single RCA response
* personalized incident views are useful
* generated reports materially reduce post-incident effort

These should be validated through interviews and experiments rather than treated as established facts.
