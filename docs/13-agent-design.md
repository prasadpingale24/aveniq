# AVENIQ — Agent Design

## 1. Purpose

AVENIQ uses agents to perform investigation work that would otherwise require repeated manual interaction with observability and operational tools.

Agents are therefore treated as **investigation workers**, not as the product itself.

---

# 2. Agentic Investigation

A conventional workflow might be:

```text
Engineer decides query
      ↓
Runs query
      ↓
Reads result
      ↓
Decides next query
      ↓
Runs query
```

An agent can perform this loop:

```text
Investigation objective
      ↓
Inspect context
      ↓
Determine missing information
      ↓
Select tool
      ↓
Retrieve evidence
      ↓
Interpret result
      ↓
Update context
      ↓
Select next action
```

---

# 3. Agent Responsibilities

An investigation agent may:

* inspect incident context
* identify evidence gaps
* formulate investigation questions
* select appropriate tools
* retrieve data
* correlate observations
* maintain hypotheses
* search for contradictions
* ask humans for information
* produce structured conclusions

---

# 4. Avoid One Giant Agent

The initial design should avoid creating one unrestricted "super agent."

A conceptual decomposition could be:

```text
                 Investigation Orchestrator
                          │
       ┌──────────────────┼──────────────────┐
       ↓                  ↓                  ↓
   Context Agent     Evidence Agent     Hypothesis Agent
       │                  │                  │
       ↓                  ↓                  ↓
   What matters?      What exists?      What explains it?
```

Additional specialized capabilities can be introduced when justified by experiments.

---

# 5. Context Agent

Responsibilities:

* establish incident scope
* identify affected entities
* determine timeframe
* summarize known information
* identify missing context

It answers:

> **"What do we currently know about this incident?"**

---

# 6. Evidence Agent

Responsibilities:

* determine what evidence is needed
* query appropriate sources
* normalize results
* attach provenance
* identify evidence gaps

It answers:

> **"What evidence do we need and where can we obtain it?"**

---

# 7. Hypothesis Agent

Responsibilities:

* generate candidate explanations
* compare hypotheses
* identify supporting evidence
* identify contradictory evidence
* recommend verification steps

It answers:

> **"What could explain what we are seeing?"**

---

# 8. Investigation Orchestrator

The orchestrator coordinates the overall investigation.

Conceptually:

```text
Objective
   ↓
Context
   ↓
Evidence request
   ↓
Evidence acquired
   ↓
Hypothesis update
   ↓
Verification request
   ↓
New evidence
   ↓
Decision
```

The orchestrator should also determine when to stop.

---

# 9. Human Interaction Agent / Capability

Human interaction should be treated as an explicit capability rather than an error state.

Example:

```text
Agent:
"I found two plausible explanations.

The deployment changed connection settings,
but database infrastructure metrics also degraded.

Was there a database maintenance event around 14:25?"
```

The answer becomes part of the investigation record.

---

# 10. Agent Memory

Agents should not rely solely on conversational context.

Important investigation state should live in structured storage.

For example:

```text
Incident Context
Evidence Store
Hypothesis Store
Investigation History
```

This makes investigations resumable and inspectable.

---

# 11. Tool Selection

Agents should not have unrestricted access to every available tool.

Tools should be exposed according to:

* responsibility
* permissions
* investigation stage
* data sensitivity

---

# 12. Read-First Architecture

The initial agent system should emphasize read operations.

```text
Telemetry
    ↓
Agents
    ↓
Evidence
    ↓
RCA
```

rather than:

```text
Telemetry
    ↓
Agent
    ↓
Production modification
```

Write capabilities can be explored later under explicit safety controls.

---

# 13. Agent Actions Should Be Observable

AVENIQ should record:

* which tool was selected
* what investigation question motivated it
* what data was retrieved
* what observation resulted
* how the investigation state changed

This creates an audit trail for both reliability evaluation and debugging.

---

# 14. Agent Stopping Conditions

Agents should stop when:

* sufficient evidence supports a conclusion
* evidence remains insufficient
* hypotheses cannot be distinguished
* human input is required
* investigation scope is exhausted
* investigation budget is reached

An agent that continuously searches without improving the investigation is not useful.

---

# 15. Core Principle

> **Agents should perform investigation work, while the incident context and evidence model remain the source of truth.**
