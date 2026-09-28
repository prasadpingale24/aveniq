# AVENIQ — Investigation Model

## 1. Purpose

This document defines how AVENIQ conceptualizes an investigation.

The central idea is that incident investigation is not a single inference step.

It is an iterative process of:

> **question → evidence acquisition → observation → hypothesis → verification → refinement**

---

# 2. Investigation as a Loop

A simplified investigation loop is:

```text
             ┌─────────────────────┐
             │                     │
             ↓                     │
        Investigation Question    │
             ↓                     │
        Select Action / Tool       │
             ↓                     │
        Acquire Evidence          │
             ↓                     │
          Observation             │
             ↓                     │
      Update Incident Context     │
             ↓                     │
       Evaluate Hypotheses         │
             ↓                     │
     ┌───────┴────────┐            │
     │                │            │
 sufficient       insufficient     │
     │                │            │
     ↓                ↓            │
  Verify          Ask / Search ────┘
     ↓
  Conclude
```

The loop may execute many times during a single incident.

---

# 3. Starting Context

An investigation can begin with incomplete information.

For example:

```text
Alert:
checkout-api error rate > 10%
```

At this stage, AVENIQ does not know:

* root cause
* blast radius
* affected dependency
* whether a deployment is relevant
* whether the alert itself represents the primary failure

The system should therefore treat the alert as an **initial signal**, not an answer.

---

# 4. Investigation Questions

Investigation should be driven by explicit questions.

Examples:

### Symptom questions

* What changed?
* When did the anomaly begin?
* Which service exhibits the symptom?

### Causal questions

* What could explain this behavior?
* What dependency could produce this failure?
* Did a recent change contribute?

### Scope questions

* Which endpoints are affected?
* Which regions are affected?
* Which users are affected?

### Verification questions

* Does the suspected dependency show corresponding failure?
* Did the symptom begin after the suspected change?
* Does the evidence contradict the hypothesis?

---

# 5. Investigation Actions

An agent can select actions based on the current question.

Examples:

```text
Question:
Which service is failing?

Action:
Query error logs grouped by service.
```

```text
Question:
What changed before the failure?

Action:
Query deployment history for the affected service.
```

```text
Question:
Is the database responsible?

Action:
Query database connection metrics during incident window.
```

Actions should have explicit tool boundaries.

---

# 6. Investigation Depth

AVENIQ should not attempt unlimited investigation.

The desired depth is:

> **Deep enough to establish evidence across relevant components and relationships, but not so deep that the investigation becomes an uncontrolled exploration of the entire system.**

A useful stopping condition may include:

* primary hypothesis has strong evidence
* competing hypotheses have been reasonably challenged
* impact is sufficiently understood
* unresolved uncertainty is explicitly identified

---

# 7. Hypothesis Management

Multiple hypotheses should be supported.

Example:

```text
H1 — Deployment configuration caused connection exhaustion
H2 — Database infrastructure degraded
H3 — Traffic spike exhausted connections
```

Each hypothesis can accumulate:

```text
Supporting evidence
Contradicting evidence
Unknowns
Human observations
Verification status
```

The system should avoid prematurely collapsing all possibilities into one narrative.

---

# 8. Evidence-Driven Hypothesis Updates

Suppose:

```text
H1:
Deployment caused connection exhaustion.
```

New evidence:

```text
Deployment at 14:29
Connection usage increased at 14:30
Errors began at 14:32
Configuration changed connection pool size
```

H1 becomes stronger.

If instead:

```text
Database infrastructure alert began at 14:25
Deployment occurred at 14:40
```

H1 becomes weaker.

This temporal reasoning is one of the important capabilities the investigation model must support.

---

# 9. Contradiction Is First-Class

A strong investigation should actively search for contradictory evidence.

For example:

> "The deployment occurred immediately before the incident."

This establishes correlation.

But:

> "The same deployment was active in another region with no failures."

This may weaken the hypothesis or reveal a regional factor.

Contradictory evidence should therefore not be hidden.

---

# 10. Human Interaction

Human input is another evidence channel.

The system may ask:

> "Was this deployment intentionally rolled out only to Europe?"

The answer:

> "Yes, it was a canary deployment."

can materially change the investigation.

Human-provided information should be recorded separately from machine-observed evidence.

---

# 11. Investigation Termination

An investigation may terminate when:

### Resolved

Evidence sufficiently supports a root cause and remediation has been verified.

### Partially resolved

A likely cause has been identified but verification is incomplete.

### Inconclusive

Available evidence is insufficient to establish a reliable RCA.

### Blocked

Required evidence or human information cannot be obtained.

These states are preferable to forcing every investigation into a definitive RCA.

---

# 12. Investigation Quality

Investigation quality should consider:

* evidence coverage
* source diversity
* temporal consistency
* causal plausibility
* contradictory evidence
* hypothesis discrimination
* impact coverage
* uncertainty
* human validation

A fluent answer is not necessarily a high-quality investigation.

---

# 13. Investigation Record

The investigation should preserve a structured record of:

```text
Questions
Actions
Evidence
Observations
Hypotheses
Contradictions
Human inputs
Conclusions
Uncertainty
```

This record becomes the foundation for:

* RCA
* reports
* knowledge
* evaluation
* debugging AVENIQ itself

---

# 14. Core Principle

AVENIQ should behave less like:

> **"Ask AI → receive RCA."**

and more like:

> **"Give AI an investigation objective → let it gather evidence → inspect what it finds → challenge its hypotheses → involve the human when necessary → produce an evidence-backed conclusion."**
