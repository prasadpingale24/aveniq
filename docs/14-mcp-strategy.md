# AVENIQ — MCP Strategy

## 1. Purpose

Model Context Protocol (MCP) provides a potential mechanism for exposing external operational capabilities to AVENIQ's agents.

The important architectural principle is:

> **MCP should provide access to evidence and actions; it should not define AVENIQ's investigation model.**

---

# 2. Why MCP Fits the Problem

AVENIQ needs to interact with heterogeneous systems.

Examples:

```text
Logs
Metrics
Traces
Deployments
Kubernetes
Source control
Incident management
Configuration
```

Each system exposes different APIs and data models.

MCP can provide a standardized interface through which agents discover and invoke capabilities.

---

# 3. Conceptual Architecture

```text
                    AVENIQ
                       │
                Investigation Agent
                       │
                 MCP interfaces
                       │
        ┌──────────────┼──────────────┐
        ↓              ↓              ↓
      Logs           Metrics        Traces
        │              │              │
        └──────────────┼──────────────┘
                       ↓
                Existing Systems
```

---

# 4. MCP Is Not the Evidence Model

An MCP tool might return:

```text
get_logs(...)
```

The raw result is not automatically an AVENIQ evidence object.

AVENIQ should transform external responses into its own evidence representation containing relevant:

* provenance
* timestamps
* entities
* observations
* relationships

This prevents the product's conceptual model from becoming dependent on one protocol.

---

# 5. MCP Tool Categories

Potential tool categories include:

### Telemetry

* query logs
* query metrics
* retrieve traces

### Infrastructure

* inspect services
* inspect workloads
* inspect nodes
* inspect dependency metadata

### Change

* deployments
* commits
* configuration changes
* feature flags

### Incident

* alerts
* incident metadata
* previous incidents

---

# 6. Read vs Write Tools

MCP tools should initially be classified as:

```text
READ
  ↓
retrieve information

WRITE
  ↓
change external state
```

The MVP should heavily favor read-only tools.

Write tools introduce substantially higher risk and should require explicit authorization and safety controls.

---

# 7. Tool Discovery

Agents should ideally be able to determine:

* what tools are available
* what each tool does
* what parameters it accepts
* what data it can access
* what limitations exist

However, tool discovery should not imply that agents automatically have permission to invoke every tool.

---

# 8. Integration Strategy

AVENIQ should avoid requiring users to immediately connect their entire infrastructure.

A staged strategy is preferable:

### Stage 1

Purpose-built simulated or local connectors.

### Stage 2

A small number of real integrations.

### Stage 3

MCP-compatible external systems.

### Stage 4

Broader connector ecosystem.

This allows the investigation model to be validated before integration complexity dominates development.

---

# 9. Tool Reliability

External tools can fail.

Examples:

* timeout
* unavailable service
* malformed response
* stale data
* permission denied
* rate limit

AVENIQ should record these failures as investigation events rather than silently behaving as though the data did not exist.

---

# 10. MCP and Security

Each MCP integration should define:

* authentication
* authorization
* accessible resources
* allowed operations
* data sensitivity
* audit requirements

Least privilege should be the default.

---

# 11. MCP and Agent Reliability

The agent should not assume that tool output is automatically correct.

For example:

```text
Tool:
No deployment found.

Possible meanings:
- no deployment exists
- query was incorrect
- tool lacks access
- retention window insufficient
- deployment system unavailable
```

The absence of returned data should therefore not automatically become an absence of the underlying event.

---

# 12. Core Principle

> **MCP is the bridge between agents and operational systems. AVENIQ's evidence, investigation, and reliability models remain independent of that bridge.**
