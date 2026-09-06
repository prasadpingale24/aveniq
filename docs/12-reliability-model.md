# AVENIQ — RCA Model

## 1. Purpose

The RCA model defines how AVENIQ represents and communicates a root cause analysis.

The objective is not to produce the shortest possible explanation.

The objective is to produce an explanation that is:

* evidence-backed
* causally plausible
* inspectable
* appropriately scoped
* explicit about uncertainty

---

# 2. RCA Is a Structured Explanation

An RCA should not be treated as a single text string.

Conceptually:

```text
RCA
├── Summary
├── Root cause
├── Contributing factors
├── Timeline
├── Affected components
├── Blast radius
├── Supporting evidence
├── Contradicting evidence
├── Uncertainty
├── Remediation
└── Prevention
```

The generated narrative is a presentation of this structure.

---

# 3. Root Cause

The root cause is the most supported explanation for why the incident occurred.

It should answer:

> **What underlying condition initiated or materially contributed to the observed failure?**

The RCA should distinguish the root cause from symptoms.

Example:

```text
Symptom:
API returned 500 errors.

Intermediate failure:
Database connection acquisition failed.

Root cause:
A configuration change reduced the effective database
connection capacity during a production deployment.
```

---

# 4. Contributing Factors

Incidents may have multiple contributing factors.

Examples:

* insufficient capacity
* missing validation
* incomplete rollout safeguards
* missing alert
* inadequate timeout configuration
* incomplete tracing
* dependency degradation

Contributing factors should not automatically be promoted to root causes.

---

# 5. Causal Chain

Where sufficient evidence exists, AVENIQ should attempt to represent the causal chain.

Example:

```text
Configuration change
        ↓
Reduced connection capacity
        ↓
Connection pool exhaustion
        ↓
Database requests fail
        ↓
checkout-api errors
        ↓
Customer checkout failures
```

Each transition should ideally have supporting evidence.

---

# 6. Timeline

The RCA should establish a timeline when temporal information is available.

Example:

```text
14:25 — Configuration change
14:29 — Deployment begins
14:30 — Connection utilization increases
14:32 — Database connection errors begin
14:33 — API error rate increases
14:36 — Incident detected
14:41 — Rollback begins
14:44 — Error rate returns to baseline
```

A timeline helps distinguish:

* preceding events
* symptoms
* consequences
* remediation

---

# 7. Blast Radius

The RCA should describe what was affected.

Possible dimensions:

```text
Services
Endpoints
Regions
Versions
Requests
Users
Business capabilities
```

The system should not infer a larger blast radius than the evidence supports.

---

# 8. Evidence Attachment

Important RCA claims should reference evidence.

Example:

```text
Claim:
Connection exhaustion caused checkout failures.

Evidence:
E17 — connection utilization reached 99%
E23 — connection acquisition failures increased
E31 — checkout-api database errors increased
E44 — rollback restored connection availability
```

---

# 9. Contradictory Evidence

An RCA should include meaningful contradictory observations.

Example:

> "The same deployment was present in US-East without elevated errors."

This may indicate that the deployment alone was insufficient to cause the incident.

The investigation should therefore consider:

```text
Deployment
+
Regional configuration
```

rather than simply blaming the deployment.

---

# 10. RCA States

An RCA may have one of several states:

### Confirmed

Strong evidence supports the explanation and meaningful alternatives have been challenged.

### Probable

The explanation is strongly supported but one or more uncertainties remain.

### Possible

The explanation is plausible but evidence is insufficient.

### Inconclusive

No hypothesis has sufficient support.

The product should not force an RCA into "confirmed" simply because the user expects an answer.

---

# 11. Remediation

The RCA may include:

* immediate mitigation
* permanent fix
* rollback
* configuration correction
* capacity change
* instrumentation improvement

Remediation should be distinguished from cause.

---

# 12. Prevention

The RCA can identify measures that reduce recurrence.

Examples:

* new alert
* better trace propagation
* deployment validation
* capacity safeguards
* integration tests
* configuration validation
* runbook update

---

# 13. Observability Lessons

A special section should answer:

> **What could have made this incident easier to detect or investigate?**

Examples:

* missing metric
* missing correlation ID
* incomplete trace propagation
* insufficient deployment metadata
* missing region labels
* misleading dashboard
* alert fired too late
* no alert at all

This connects incident investigation with observability improvement.

---

# 14. RCA Quality Principle

A good AVENIQ RCA should allow an engineer to move backward:

```text
RCA
 ↓
Claim
 ↓
Evidence
 ↓
Source
 ↓
Original observation
```

If that path cannot be followed, the RCA should be treated as weaker.

---

# 15. Core Principle

> **An RCA is not merely an answer. It is an evidence-backed explanation of an incident.**
