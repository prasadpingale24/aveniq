# AVENIQ — Benchmark Incidents

## 1. Purpose

Benchmark incidents provide controlled scenarios for evaluating AVENIQ's investigation capabilities.

They should represent realistic operational problems rather than artificially simple questions such as:

> "Which service has an error?"

---

# 2. Benchmark Design Principles

Each benchmark should contain:

* initial signal
* system context
* telemetry
* relevant changes
* distractors
* actual root cause
* expected blast radius
* evidence required for verification

Some scenarios should intentionally contain incomplete information.

---

# 3. Incident Categories

## B01 — Deployment Regression

A deployment introduces a configuration or code-level regression.

Expected investigation:

```text
Alert
 ↓
Service
 ↓
Deployment
 ↓
Change
 ↓
Telemetry
 ↓
RCA
```

---

## B02 — Dependency Failure

An upstream dependency begins failing and causes downstream symptoms.

Purpose:

Test whether AVENIQ distinguishes the affected service from the actual source of failure.

---

## B03 — Database Connection Exhaustion

Application requests fail because database connections become exhausted.

Purpose:

Test cross-component reasoning.

Expected evidence:

* application errors
* connection metrics
* database observations
* configuration/change history

---

## B04 — Regional Failure

Only one region experiences elevated failures.

Purpose:

Test whether the system investigates dimensions such as:

* region
* deployment
* regional configuration
* regional dependency

---

## B05 — Silent Failure

The system is unhealthy but existing alerts do not fire.

Purpose:

Test manual investigation without an initial alert.

---

## B06 — Missing Trace Propagation

Logs and metrics show evidence of a distributed failure, but request-level tracing is unavailable.

Purpose:

Test whether AVENIQ can continue investigating without treating traces as mandatory.

---

## B07 — Misleading Alert

The alert identifies a downstream symptom.

Example:

```text
API latency ↑
```

while the underlying issue is dependency degradation.

Purpose:

Test whether AVENIQ can move beyond the initial signal.

---

## B08 — Conflicting Evidence

Different sources appear to indicate different causes.

Purpose:

Test contradiction handling.

---

## B09 — Recent Change Distractor

A deployment occurred shortly before the incident but is unrelated.

Purpose:

Test whether AVENIQ incorrectly assumes temporal correlation implies causation.

---

## B10 — Insufficient Evidence

The benchmark deliberately removes critical telemetry.

Expected behavior:

```text
No confirmed RCA
+
Evidence collected
+
Most plausible hypotheses
+
Evidence gaps
+
Recommended next step
```

---

# 4. Ground Truth

Each benchmark should maintain hidden ground truth containing:

* root cause
* contributing factors
* timeline
* affected components
* expected evidence
* irrelevant evidence
* known evidence gaps

Ground truth should not be exposed to the investigation agent.

---

# 5. Benchmark Difficulty

Difficulty can increase through:

### Level 1

Single service, clear evidence.

### Level 2

Multiple services and evidence sources.

### Level 3

Multiple plausible hypotheses.

### Level 4

Missing and contradictory evidence.

### Level 5

Multi-step distributed failure with misleading signals.

---

# 6. Benchmark Output

For each benchmark, AVENIQ should produce:

```text
Investigation
Evidence
Hypotheses
RCA
Confidence / uncertainty
Evidence gaps
Impact
Investigation duration
Tool usage
Human interventions
```

This creates a repeatable basis for comparison.

---

# 7. Benchmark Principle

> **A benchmark should test whether AVENIQ can discover the explanation, not whether it can recognize an explanation that was effectively handed to it.**
