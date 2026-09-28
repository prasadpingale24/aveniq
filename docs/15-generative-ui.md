# AVENIQ — Generative UI

## 1. Purpose

Generative UI is a central part of AVENIQ's product exploration.

The objective is not to make the interface visually novel.

The objective is to determine whether dynamically generated interfaces can make incident investigation more effective than a static dashboard or chat interface.

---

# 2. The Problem With Static Dashboards

A static dashboard defines its components before the incident.

For example:

```text
CPU
Memory
Request Rate
Error Rate
Latency
Database Connections
```

These are useful, but the relevant information differs between incidents.

An incident involving a deployment may require:

```text
Deployment timeline
Configuration diff
Affected version
Error clusters
Service dependencies
```

An incident involving regional impact may instead require:

```text
Regional error rate
Affected users
Traffic distribution
Regional dependencies
```

The optimal interface is therefore incident-dependent.

---

# 3. Generative UI Concept

AVENIQ should conceptually perform:

```text
Incident Context
       +
User Role
       +
Current Investigation State
       +
Available Evidence
       ↓
UI Composition
```

The result may include only the components relevant to the current investigation.

---

# 4. Example — Engineer View

An engineer investigating an API failure might receive:

```text
┌─────────────────────────────────────────┐
│ Incident Summary                        │
├─────────────────────────────────────────┤
│ Timeline                                │
├─────────────────────────────────────────┤
│ Service Dependency Graph                │
├─────────────────────────────────────────┤
│ Error Cluster                           │
├─────────────────────────────────────────┤
│ Deployment Change                       │
├─────────────────────────────────────────┤
│ Supporting Metrics                      │
├─────────────────────────────────────────┤
│ Relevant Logs                           │
├─────────────────────────────────────────┤
│ RCA Hypotheses                          │
├─────────────────────────────────────────┤
│ Evidence                                │
└─────────────────────────────────────────┘
```

The exact composition depends on the investigation.

---

# 5. Example — Stakeholder View

The same incident might generate:

```text
┌─────────────────────────────────────────┐
│ Checkout Incident                      │
├─────────────────────────────────────────┤
│ Status: Resolved                        │
├─────────────────────────────────────────┤
│ Duration                                │
├─────────────────────────────────────────┤
│ Affected Region                         │
├─────────────────────────────────────────┤
│ Estimated User Impact                   │
├─────────────────────────────────────────┤
│ Business Impact                         │
├─────────────────────────────────────────┤
│ Resolution                              │
└─────────────────────────────────────────┘
```

The underlying incident context remains the same.

---

# 6. UI Should Be Evidence-Aware

Generated components should originate from available evidence.

For example:

If regional evidence exists:

```text
Regional Impact Map
```

may be appropriate.

If no regional information exists:

```text
Regional Impact Map
```

should not be fabricated simply because the UI generator thinks it looks useful.

Instead:

> "Regional impact unavailable."

This is important for reliability.

---

# 7. UI Components as Views of Context

The interface should ideally be composed from reusable components.

Examples:

* timeline
* evidence panel
* hypothesis card
* dependency graph
* metric visualization
* log cluster
* deployment change
* impact summary
* question prompt
* investigation progress

Generative UI determines **which components appear and how they are arranged**.

---

# 8. Conversational + Visual Interface

AVENIQ should not choose between:

```text
Chat
```

and:

```text
Dashboard
```

The intended experience combines them.

For example:

```text
User:
"Why are checkout requests failing?"

        ↓

Generated investigation view

        ↓

Agent:
"I found two likely causes."

        ↓

UI:
[Hypothesis A]
[Hypothesis B]

        ↓

User:
"Focus on the deployment."

        ↓

UI dynamically expands:

[Deployment diff]
[Timeline]
[Relevant errors]
[Connection metrics]
[Evidence]
```

The interface evolves with the investigation.

---

# 9. Personalization

Personalization should primarily affect:

* level of detail
* terminology
* visualization
* ordering
* relevant dimensions

It should not change underlying evidence.

Conceptually:

```text
                 Incident Context
                        │
        ┌───────────────┼───────────────┐
        ↓               ↓               ↓
     Engineer          Lead        Stakeholder
        ↓               ↓               ↓
   Technical UI      Impact UI      Business UI
```

---

# 10. Generative UI Safety

Generated interfaces should use a constrained component vocabulary rather than arbitrary UI generation.

This provides:

* predictable behavior
* security
* accessibility
* consistent interaction
* easier testing

The agent can decide **what to show**, while the system controls **how components behave**.

---

# 11. Generative UI and Reliability

A generated UI should not conceal uncertainty.

For example:

```text
RCA: Probable

Evidence:
4 supporting observations

Contradictions:
1 observation

Missing:
Deployment configuration history
```

The interface itself should communicate investigation state.

---

# 12. MVP Scope

The MVP does not need a completely arbitrary UI generation system.

A more practical starting point is:

```text
Fixed component library
        +
Dynamic component selection
        +
Dynamic layout
        +
Dynamic data binding
```

This allows the project to validate whether **adaptive interfaces actually improve investigation** without solving unrestricted UI generation.

---

# 13. Core Principle

> **Generative UI should make the incident context adapt to the investigation—not make the evidence adapt to the UI.**
