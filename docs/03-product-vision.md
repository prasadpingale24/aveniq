# AVENIQ — Product Vision

## 1. Vision

> **Make production incident investigation evidence-driven, contextual, and dramatically easier to navigate.**

AVENIQ aims to help engineers move from:

```text
"What is broken?"
```

toward:

```text
"What happened?"
        ↓
"What evidence do we have?"
        ↓
"How are the signals connected?"
        ↓
"What is the likely cause?"
        ↓
"What evidence supports or contradicts it?"
        ↓
"What was affected?"
        ↓
"Has the hypothesis been validated?"
        ↓
"What should we learn from this?"
```

The goal is not to make humans disappear from incident response.

The goal is to make humans **far more effective at investigation**.

---

## 2. Product Philosophy

### Evidence before confidence

AVENIQ should prefer:

> "Here are the observations supporting this hypothesis."

over:

> "I am 94% confident this is the root cause."

Confidence can be useful, but it should not substitute for evidence.

---

### Context before conclusions

The system should first establish enough incident context to reason meaningfully.

A single error message should not automatically become an RCA.

---

### Investigation before automation

Automation should emerge from understanding the investigation workflow.

The project should not automate a workflow merely because an agent can technically perform it.

---

### Assist existing systems

AVENIQ should consume existing operational data rather than attempt to become another all-purpose observability platform.

---

### Uncertainty is a valid result

If evidence is insufficient, the system should say so.

A partial investigation with explicit uncertainty is preferable to a fabricated certainty.

---

## 3. Product Concept

AVENIQ can be thought of as an **incident investigation workspace**.

A high-level interaction might look like:

```text
Incident / Alert
      ↓
AVENIQ builds initial context
      ↓
Agents inspect available evidence
      ↓
Evidence is correlated
      ↓
Hypotheses are formed
      ↓
Hypotheses are verified / challenged
      ↓
Human is asked when necessary
      ↓
Incident context evolves
      ↓
Evidence-backed RCA
      ↓
Impact + blast radius
      ↓
Report / knowledge
```

The interface should reflect this evolving investigation rather than presenting a static collection of dashboards.

---

## 4. The Incident as the Primary Object

AVENIQ should treat an **incident** as the primary investigation object.

An incident can contain:

* triggering alert
* timeframe
* affected services
* relevant telemetry
* observed symptoms
* entities
* changes
* hypotheses
* evidence
* contradictions
* human answers
* investigation actions
* RCA
* impact
* remediation
* resolution verification
* generated knowledge

This provides a common context across agents and UI components.

---

## 5. The Evidence Trail

Every important conclusion should ideally be traceable to evidence.

For example:

```text
RCA:
Database connection pool exhaustion

Supporting evidence:
  ├── Metric: connection utilization
  ├── Metric: rejected connections
  ├── Logs: connection acquisition failures
  ├── Service: checkout-api
  ├── Time: 14:32–14:38
  └── Deployment: checkout-api v2.8.1

Contradicting evidence:
  └── None identified

Confidence:
  └── Derived from evidence quality, not merely model probability
```

The exact implementation remains an engineering decision.

The conceptual requirement is that an engineer can inspect **why** AVENIQ reached a conclusion.

---

## 6. The Adaptive Interface

The UI should not attempt to display everything.

Instead, it should answer:

> **What does this person need to understand this incident right now?**

An engineer might receive:

```text
Timeline
Service dependency graph
Error clusters
Relevant logs
Metrics
Trace relationships
Deployment diff
Evidence
RCA hypothesis
```

A stakeholder might receive:

```text
Incident summary
Duration
Affected users
Regions
Business capability
Impact
Resolution
```

Both views should originate from the same incident context.

This is the role of the generative UI layer.

---

## 7. Agentic Behavior

AVENIQ's agents should behave more like investigators than chatbots.

An investigation might involve:

```text
Agent:
"The API error rate increased at 14:32."

Agent:
"I found a deployment at 14:29."

Agent:
"The deployment changed database connection configuration."

Agent:
"I need to determine whether connection exhaustion occurred."

Agent:
"Metric evidence confirms connection utilization reached 99%."

Agent:
"Logs show acquisition failures beginning at 14:32."

Agent:
"Evidence supports the deployment → configuration → exhaustion hypothesis."
```

If the available evidence is insufficient:

```text
Agent:
"I found two plausible causes.

I need to know whether the affected requests were
restricted to the EU region.

Can you confirm?"
```

This conversational investigation model is intentional.

---

## 8. Long-Term Vision

If the concept proves valuable, AVENIQ could evolve from an incident investigation assistant into a broader operational intelligence layer:

```text
Detection
   ↓
Investigation
   ↓
Resolution
   ↓
Verification
   ↓
Postmortem
   ↓
Knowledge
   ↓
Observability improvement
   ↓
Prevention
```

The long-term opportunity is therefore not simply reducing MTTR.

It is creating a feedback loop where incidents improve the system's future observability and engineering practices.

---

## 9. The Product North Star

The strongest north-star question is:

> **Can an engineer understand an unfamiliar production incident faster because AVENIQ reconstructed the relevant context and showed the evidence behind its conclusions?**

Everything else should support this question.

Agents, MCP, generative UI, connectors, reports, and knowledge articles are mechanisms.

They are not the product's fundamental purpose.
