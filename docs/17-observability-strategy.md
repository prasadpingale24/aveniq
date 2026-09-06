# AVENIQ — Observability Strategy

## 1. Purpose

AVENIQ is an observability-oriented system, but it is also itself a distributed application.

It therefore needs observability at two levels:

1. **Investigating the user's systems**
2. **Observing AVENIQ's own behavior**

---

# 2. Observability of the Target System

AVENIQ should work with whatever telemetry is available.

Potential sources include:

```text
Logs
Metrics
Traces
Deployments
Infrastructure events
Configuration
Alerts
Service metadata
```

The system should not assume that all three pillars—logs, metrics, and traces—exist.

---

# 3. Missing Observability Is Context

If a system has no distributed tracing, that should not simply appear as a failed investigation.

Instead:

```text
Trace evidence:
Unavailable

Reason:
No trace data available for affected service.

Investigation consequence:
Request-level causal propagation cannot be verified.
```

This is itself useful information.

---

# 4. Observability Strategy

AVENIQ should prefer cross-source correlation.

For example:

```text
Metric anomaly
      ↓
Service
      ↓
Logs
      ↓
Request / trace
      ↓
Dependency
      ↓
Deployment
```

The investigation should seek connections across sources rather than treating each source independently.

---

# 5. Trace Context

Trace IDs can be extremely useful where distributed tracing exists.

However, AVENIQ should not depend on tracing as the sole correlation mechanism.

Other correlation dimensions may include:

* timestamp
* service
* request ID
* correlation ID
* deployment version
* host
* pod
* region
* endpoint
* user/session metadata where appropriate

---

# 6. Correlation Without Tracing

A useful investigation should still be possible when tracing is incomplete.

For example:

```text
14:30 — checkout-api errors increase
14:31 — database connection utilization increases
14:29 — checkout-api deployment occurs
14:32 — checkout failures increase
```

Even without a trace ID, these observations can form an investigation context.

The resulting RCA should explicitly state the absence of request-level trace evidence.

---

# 7. AVENIQ's Own Telemetry

AVENIQ should monitor:

### Application health

* request latency
* error rate
* availability

### Investigation health

* investigation duration
* tool invocation latency
* failed tool calls
* agent loops
* evidence retrieval failures

### Reliability

* unsupported claims
* failed investigations
* human overrides
* RCA corrections

### Resource usage

* model calls
* token consumption
* external API usage
* storage

---

# 8. Investigation Trace

Each investigation should ideally have its own trace/context.

Conceptually:

```text
Investigation
   │
   ├── Agent action
   ├── MCP call
   ├── Evidence retrieval
   ├── Hypothesis update
   ├── Human interaction
   └── UI generation
```

This allows developers to debug AVENIQ's own reasoning workflow.

---

# 9. Observability Feedback Loop

An important product capability is learning from incidents.

```text
Incident
   ↓
Investigation
   ↓
Evidence gaps
   ↓
Observability weakness
   ↓
Recommendation
   ↓
Improved instrumentation
   ↓
Future investigation
```

This makes observability improvement a potential secondary outcome of AVENIQ.

---

# 10. Observability Lessons

A post-incident artifact may identify:

> "The incident was difficult to investigate because request correlation was unavailable between checkout-api and payment-service."

This can become an explicit recommendation:

> "Propagate correlation context across checkout-api → payment-service."

The recommendation should be grounded in the investigation rather than generated as generic best practice.

---

# 11. Core Principle

> **AVENIQ should investigate with the telemetry that exists while making missing telemetry visible as part of the incident context.**
