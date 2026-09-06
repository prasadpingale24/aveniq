# AVENIQ — Integrations

## 1. Purpose

AVENIQ is intended to assist existing engineering workflows rather than replace the observability and operational tools already used by teams.

Integrations therefore represent a core boundary of the product.

---

# 2. Integration Philosophy

The target architecture is:

```text
Existing Tools
      ↓
AVENIQ
      ↓
Unified Investigation Context
      ↓
Evidence-backed Investigation
```

rather than:

```text
Existing Tools
      ↓
AVENIQ replacement
```

---

# 3. Integration Categories

Potential integration categories include:

### Observability

* logs
* metrics
* traces
* application performance monitoring

### Infrastructure

* Kubernetes
* cloud infrastructure
* service discovery

### Change Management

* source control
* CI/CD
* deployment platforms
* configuration systems

### Incident Management

* alerting
* incident-management platforms
* ticketing

---

# 4. Integration Interface

AVENIQ should conceptually expose a common internal interface.

For example:

```text
query_logs()
query_metrics()
query_traces()
get_deployments()
get_service()
get_incident()
```

External systems can implement these capabilities differently.

The investigation engine should not need to understand every vendor-specific API.

---

# 5. MCP as an Integration Mechanism

MCP may be used to expose external capabilities to agents.

However, integrations should remain conceptually separate from MCP.

Possible implementations include:

```text
Native connector
MCP server
API adapter
Simulated connector
```

The evidence model should remain the common abstraction.

---

# 6. MVP Integration Strategy

The MVP should avoid attempting to integrate every major observability platform.

A practical progression is:

### Phase 1

Controlled local/simulated data sources.

### Phase 2

One realistic observability stack.

### Phase 3

Multiple heterogeneous sources.

### Phase 4

External MCP-compatible ecosystem.

The purpose of Phase 1 is to validate the investigation model rather than integration breadth.

---

# 7. Connector Contract

A connector should ideally provide:

* capability description
* query interface
* authentication mechanism
* source metadata
* returned evidence
* errors
* limitations

---

# 8. Failure Handling

An unavailable integration should not silently disappear.

For example:

```text
Metrics source
Status: unavailable
Reason: authentication failure
Impact:
Metric verification could not be completed.
```

This becomes an evidence gap.

---

# 9. Data Normalization

Different systems may represent the same concept differently.

For example:

```text
service_name
app
application
workload
```

AVENIQ may normalize these into a common entity model while retaining source-specific metadata.

---

# 10. Integration Independence

The investigation engine should be able to reason over normalized evidence without knowing whether it originated from:

* vendor A
* vendor B
* local logs
* a simulated environment

This makes the architecture extensible.

---

# 11. Core Principle

> **Integrations should bring existing operational context into AVENIQ; AVENIQ should not require teams to replace their existing tooling.**
