# AVENIQ — Goals and Non-Goals

## 1. Goals

### G1 — Reduce investigation context switching

Help engineers investigate an incident without manually jumping between multiple observability surfaces for every investigative step.

---

### G2 — Aggregate incident-relevant context

Collect relevant evidence from available operational sources into a coherent incident context.

The objective is not to collect everything.

The objective is to identify and preserve what is relevant.

---

### G3 — Produce evidence-backed hypotheses

AVENIQ should be capable of generating probable explanations while explicitly connecting those explanations to supporting evidence.

---

### G4 — Make evidence inspectable

An engineer should be able to understand:

* what was observed
* where it came from
* when it occurred
* how it relates to the incident
* whether it supports or contradicts a hypothesis

---

### G5 — Support incomplete observability

The system should remain useful when:

* tracing is unavailable
* trace propagation is incomplete
* logs are sparse
* metrics are missing
* integrations provide incomplete context

It should degrade gracefully rather than assume perfect instrumentation.

---

### G6 — Enable iterative investigation

Investigation should be allowed to evolve over multiple conversational turns.

The system should be able to:

* ask questions
* revise hypotheses
* request additional evidence
* incorporate human answers
* explicitly record uncertainty

---

### G7 — Reduce post-resolution work

Where sufficient context exists, AVENIQ should assist with:

* incident reports
* RCA summaries
* timelines
* knowledge articles
* observability improvement recommendations

---

### G8 — Adapt the incident view

Generate incident views appropriate to the user's role and current investigative needs.

---

### G9 — Integrate rather than replace

AVENIQ should work with existing observability and operational systems.

---

### G10 — Evaluate reliability explicitly

The system should be evaluated on evidence quality and investigation usefulness, not merely response fluency.

---

# 2. Non-Goals

## NG1 — Replace observability platforms

AVENIQ is not intended to become a replacement for systems such as logging, metrics, tracing, APM, infrastructure monitoring, or incident management.

---

## NG2 — Build another static dashboard

The project should not simply recreate conventional observability dashboards behind a different interface.

---

## NG3 — Guarantee autonomous RCA

AVENIQ should not claim that every incident can be automatically diagnosed.

---

## NG4 — Hide uncertainty

The system should not suppress missing evidence or uncertainty to make the output appear more confident.

---

## NG5 — Automatically deploy production fixes

Production remediation automation is outside the initial scope.

The investigation system may recommend or assist with remediation, but autonomous production deployment introduces a substantially different safety boundary.

---

## NG6 — Depend exclusively on distributed tracing

Tracing is valuable but should be treated as one evidence source among many.

---

## NG7 — Collect unlimited telemetry

AVENIQ should not indiscriminately ingest or retain all available operational data.

Relevant data acquisition should be driven by investigation needs.

---

## NG8 — Become a generic AI assistant

The system should remain focused on production incident investigation and its directly related workflows.

---

## NG9 — Optimize solely for MTTR

MTTR reduction is an important outcome, but optimizing for speed at the expense of correctness is unacceptable.

A faster incorrect RCA is not a successful investigation.

---

## NG10 — Replace human judgment

The system should augment engineering judgment.

Human intervention remains an intentional part of the design when evidence is insufficient, ambiguous, contradictory, or high-risk.

---

# 3. MVP Boundary

The first MVP should primarily answer:

> **Can AVENIQ reconstruct useful incident context from multiple sources and help an engineer reach a better-supported RCA faster?**

Features that do not contribute meaningfully to this question should be deferred.

---

# 4. Success Boundary

AVENIQ should be considered successful only if experiments demonstrate measurable improvement in one or more of:

* investigation time
* context switching
* evidence coverage
* RCA correctness
* engineer effort
* post-incident documentation effort

while maintaining acceptable reliability.
