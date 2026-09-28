# AVENIQ — Evaluation

## 1. Purpose

AVENIQ should be evaluated as an **incident investigation system**, not simply as an AI assistant.

The central question is:

> **Does AVENIQ help engineers reach a correct, evidence-backed RCA with less manual effort than the existing workflow?**

---

# 2. Evaluation Principles

Evaluation should prioritize:

1. correctness
2. evidence quality
3. investigation completeness
4. reliability under uncertainty
5. reduction in manual effort
6. time to useful context
7. usefulness of generated artifacts

A fluent response is not sufficient evidence of success.

---

# 3. Primary Metrics

## 3.1 RCA Accuracy

Did AVENIQ identify the actual root cause?

```text
Correct RCA / Total evaluated incidents
```

---

## 3.2 Evidence Support

For important RCA claims:

> Can the claim be traced back to valid evidence?

This should measure the proportion of claims that are adequately supported.

---

## 3.3 Unsupported Claim Rate

How often does AVENIQ make claims that cannot be justified by available evidence?

This is particularly important because the system explicitly prioritizes reliability.

---

## 3.4 Evidence Coverage

Did the investigation gather evidence across the relevant components?

For example:

```text
Application
Dependency
Telemetry
Change
Impact
```

---

## 3.5 False RCA Rate

How frequently does AVENIQ confidently identify an incorrect cause?

This should be treated as a critical failure metric.

---

## 3.6 Inconclusive Correctness

When the available evidence is insufficient, does AVENIQ appropriately report uncertainty rather than hallucinating an RCA?

A correct "inconclusive" outcome should count positively.

---

# 4. Efficiency Metrics

## Time to Useful Context

How long until the engineer receives a meaningful incident context?

---

## Time to RCA

How long does it take to reach a sufficiently supported RCA?

---

## Manual Investigation Steps

Compare:

```text
Traditional workflow:
Tabs → searches → dashboards → correlation → trace lookup → logs
```

against:

```text
AVENIQ:
Investigation → evidence → verification
```

---

## Context Switching

Measure the number of tool/dashboard transitions required.

The hypothesis is that AVENIQ reduces unnecessary context switching.

---

# 5. Human Intervention Metrics

Track:

* investigations requiring human input
* number of questions asked
* useful questions
* unnecessary questions
* human corrections
* rejected hypotheses
* manually completed investigations

A lower intervention rate is not automatically better.

An agent that never asks for clarification may simply be overconfident.

---

# 6. Generative UI Metrics

The GenUI component should be evaluated separately.

Potential measures:

* time to find relevant evidence
* number of UI interactions
* component relevance
* unnecessary component count
* engineer preference
* stakeholder comprehension

A generated interface is successful only if it improves investigation effectiveness.

---

# 7. Reliability Evaluation

AVENIQ should be tested against:

### Complete telemetry

Logs + metrics + traces + deployment metadata.

### Partial telemetry

One or more major sources unavailable.

### Conflicting telemetry

Sources disagree.

### Missing traces

No distributed tracing.

### Missing alerts

Incident begins without an alert.

### Ambiguous incidents

Multiple plausible root causes.

### Misleading signals

The initial alert points toward a symptom rather than the cause.

---

# 8. Baseline Comparison

The evaluation should compare AVENIQ against a baseline workflow.

Possible baselines:

### Manual

Engineer investigates using provided observability tools.

### AI-assisted

Engineer uses a conventional conversational AI interface with access to the same information.

### AVENIQ

Evidence aggregation + agentic investigation + adaptive UI.

This helps determine whether the value comes from AI alone or from the complete AVENIQ architecture.

---

# 9. Human Evaluation

Engineers should evaluate:

* usefulness
* trust
* evidence quality
* investigation completeness
* clarity
* UI usefulness
* willingness to use during incidents

Qualitative feedback is particularly important during early PoC stages.

---

# 10. Success Criteria for MVP

The MVP should demonstrate that it can:

1. gather evidence from multiple sources
2. correlate evidence across components
3. produce an evidence-backed RCA
4. expose evidence supporting the RCA
5. acknowledge missing information
6. ask useful human questions
7. reduce manual investigation effort
8. generate a context-appropriate incident view

The exact numerical thresholds should be established after baseline measurements rather than invented beforehand.
