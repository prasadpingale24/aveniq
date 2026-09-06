# AVENIQ — Problem

## 1. Problem Statement

Production incidents are often investigated through a collection of observability tools that individually expose useful signals but do not necessarily provide the complete context required to understand an incident.

An alert may identify that something is wrong. A dashboard may show that a service is healthy. A log may contain an error. A metric may show an anomaly. A trace, when available and correctly propagated, may connect part of the request path.

Yet the actual investigation frequently requires an engineer to manually connect these pieces.

The difficult part is therefore not simply **finding telemetry**.

The difficult part is **reconstructing the incident from fragmented evidence and establishing why the observed symptoms occurred**.

AVENIQ is intended to explore whether an agentic, evidence-first investigation system can reduce this investigation burden while keeping humans able to inspect and challenge the evidence behind its conclusions.

---

## 2. The Investigation Problem

A simplified production incident workflow can look like:

```text
Alert
  ↓
Identify affected service
  ↓
Open observability tools
  ↓
Inspect metrics
  ↓
Inspect logs
  ↓
Find relevant traces, if available
  ↓
Correlate timestamps / services / requests
  ↓
Investigate dependencies
  ↓
Inspect recent changes / deployments
  ↓
Determine blast radius
  ↓
Form RCA hypothesis
  ↓
Validate hypothesis against evidence
  ↓
Fix / mitigate
  ↓
Verify resolution
  ↓
Generate incident report
  ↓
Capture reusable knowledge
```

The workflow is not necessarily difficult because any individual operation is complicated.

It becomes difficult because **the context is distributed across many operations and sources**.

An engineer must repeatedly answer questions such as:

* What changed around the time the incident started?
* Which service actually exhibited the first meaningful failure?
* Is this error the cause or merely a downstream symptom?
* Which requests were affected?
* Which dependencies were involved?
* Did the problem affect all users or only a subset?
* Which region, endpoint, deployment, or version was involved?
* What evidence supports the suspected cause?
* What evidence contradicts it?
* Has the suspected cause actually disappeared after remediation?

---

## 3. The Core Problem

AVENIQ focuses on the following problem:

> **How can an engineer move from an incident signal to an evidence-backed understanding of what happened, why it happened, and what was affected, without manually reconstructing the context across disconnected observability surfaces?**

This is deliberately different from:

> "How can AI automatically tell us the root cause?"

The latter assumes that an AI-generated answer is the desired artifact.

AVENIQ instead treats the **investigation context and evidence trail** as primary artifacts, with AI assisting in navigating and reasoning over them.

---

## 4. Why a Dashboard Alone Is Insufficient

A dashboard is generally designed to present known information in a predefined structure.

That works well when the engineer already knows what they are looking for.

Incident investigation is different.

The relevant evidence can vary significantly between incidents.

For example:

```text
Incident A
  API latency
    → database saturation
      → connection pool exhaustion
        → deployment configuration

Incident B
  API errors
    → dependency timeout
      → regional network issue

Incident C
  apparently healthy service
    → incorrect feature configuration
      → subset of users affected
```

A static dashboard must anticipate these relationships in advance.

An investigation system instead needs to determine:

> **What information is relevant to this particular incident?**

This is one of the motivations for exploring generative UI.

Rather than displaying every possible dashboard component, AVENIQ can potentially construct an incident-specific workspace containing the evidence and relationships relevant to the current investigation.

---

## 5. The Context Fragmentation Problem

The investigation context may be distributed across:

* logs
* metrics
* traces
* service metadata
* deployment history
* configuration changes
* infrastructure state
* Kubernetes state
* application errors
* source-control changes
* incident alerts
* tickets
* documentation
* previous incidents

These sources may also use different identifiers and different levels of granularity.

A trace ID can be extremely useful when tracing is correctly instrumented and propagated, but AVENIQ should **not assume that a single trace ID is sufficient to reconstruct an incident**.

An incident is broader than an individual request.

The investigation may require understanding:

```text
Individual request
        ↓
Service
        ↓
Dependency
        ↓
Deployment / configuration
        ↓
Infrastructure
        ↓
Affected requests/users/regions
        ↓
Incident-wide blast radius
```

Therefore, AVENIQ's conceptual unit of investigation is the **incident context**, not merely the trace.

---

## 6. The Evidence Problem

An AI-generated RCA without inspectable evidence is not sufficient for the intended use case.

Consider:

> "The incident was caused by database connection exhaustion."

That statement may be correct.

But an engineer needs to know:

* What database?
* During what timeframe?
* What metric indicates exhaustion?
* Which service experienced the exhaustion?
* Did connection usage increase before errors?
* Was there a deployment that changed connection behavior?
* Are there logs supporting the hypothesis?
* Were affected requests actually connected to this dependency?
* What happened after remediation?

Therefore AVENIQ should aim for:

```text
Claim
  ↓
Supporting evidence
  ↓
Source
  ↓
Timestamp
  ↓
Relevant entity
  ↓
Relationship to incident
```

The system should make it possible to distinguish:

**Observed evidence**

from

**AI inference**

from

**Human-provided information**

from

**Unverified hypothesis**

This distinction is fundamental to the product.

---

## 7. The Reliability Problem

Incident response is a high-consequence environment.

An incorrect RCA can cause:

* engineers to fix the wrong component
* unnecessary deployments
* wasted investigation time
* delayed recovery
* incorrect incident reports
* incorrect knowledge articles
* repeated incidents if the real cause remains unresolved

Therefore the intended system should not optimize solely for:

> "How often did the AI produce an RCA?"

It should also evaluate:

> "How well did the system support an engineer in arriving at a correct RCA?"

A useful fallback state is therefore:

```text
Insufficient evidence
       ↓
Partial context
       ↓
Probable hypotheses
       ↓
Evidence supporting each hypothesis
       ↓
Human investigation
```

A useful incomplete investigation is preferable to a confident unsupported conclusion.

---

## 8. The Human Context Problem

Different people need different representations of the same incident.

An engineer may care about:

* affected endpoints
* services
* errors
* dependencies
* traces
* deployment versions
* infrastructure state

A technical lead may care about:

* root cause
* blast radius
* duration
* remediation
* recurrence risk

A stakeholder may care about:

* affected regions
* affected users
* business functionality
* duration
* customer impact
* SLA implications

The underlying evidence should remain consistent while the presentation can change.

This creates a second problem beyond evidence aggregation:

> **How can the same incident context be represented appropriately for different users without creating separate manually maintained dashboards?**

This is where generative UI becomes relevant to AVENIQ.

---

## 9. The Post-Incident Problem

Even after resolution, significant manual work can remain.

Engineers may need to produce:

* incident timelines
* RCA reports
* impact summaries
* remediation details
* contributing factors
* preventive actions
* observability improvements
* knowledge articles

The investigation itself has already gathered much of the necessary information.

AVENIQ therefore explores whether the accumulated incident context can become the foundation for these artifacts instead of requiring engineers to reconstruct the story again after the incident.

---

## 10. The Problem AVENIQ Is Exploring

AVENIQ is ultimately an exploration of this hypothesis:

> **If incident investigation is treated as evidence and context reconstruction rather than simply AI-generated RCA, an agentic system can help engineers investigate production incidents with less context switching while preserving inspectability, uncertainty, and human control.**

The project therefore combines four areas:

1. **Evidence aggregation**
2. **Agentic investigation**
3. **Generative incident interfaces**
4. **Evidence-backed incident knowledge**

The project does not assume that all four will necessarily prove equally valuable.

The MVP and subsequent experiments should determine which parts actually improve incident investigation.
