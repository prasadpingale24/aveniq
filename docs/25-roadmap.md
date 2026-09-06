# AVENIQ — Roadmap

## 1. Purpose

The roadmap describes how AVENIQ can evolve from a controlled proof of concept into a broader engineering product.

The roadmap is intentionally hypothesis-driven.

Features should advance when experiments demonstrate value.

---

# 2. Phase 0 — Foundation

### Objective

Establish the conceptual and technical foundation.

Deliver:

* documentation
* evidence model
* investigation model
* benchmark incident format
* basic repository structure
* initial architecture

---

# 3. Phase 1 — Controlled PoC

### Objective

Prove evidence-first investigation.

Capabilities:

* controlled telemetry sources
* incident creation
* evidence aggregation
* basic agent investigation
* hypothesis generation
* evidence-backed RCA
* basic UI

Success criterion:

> Demonstrate a complete investigation from signal to RCA.

---

# 4. Phase 2 — Agentic Investigation

### Objective

Determine whether agentic behavior provides measurable benefit.

Add:

* iterative investigation
* specialized investigation capabilities
* contradiction search
* human questions
* investigation history
* reliability metrics

Compare against deterministic baselines.

---

# 5. Phase 3 — Generative UI

### Objective

Validate whether adaptive interfaces improve investigation effectiveness.

Add:

* component registry
* dynamic component selection
* adaptive layouts
* role-aware views
* investigation-state-aware UI

Evaluate against static dashboards.

---

# 6. Phase 4 — Real Integrations

### Objective

Move beyond synthetic or controlled data.

Add a limited set of real integrations.

Potential categories:

* observability
* deployments
* source control
* infrastructure

The number of integrations should remain intentionally small until the core workflow is proven.

---

# 7. Phase 5 — MCP Ecosystem

### Objective

Evaluate MCP as a scalable integration mechanism.

Capabilities:

* MCP tool discovery
* MCP-based telemetry access
* tool capability metadata
* permission boundaries
* tool reliability tracking

---

# 8. Phase 6 — Post-Incident Intelligence

### Objective

Turn investigations into reusable engineering knowledge.

Add:

* automated incident reports
* knowledge articles
* observability recommendations
* recurring failure pattern detection
* historical incident comparison

---

# 9. Phase 7 — Production Hardening

Only after product value is demonstrated:

* stronger authentication
* granular authorization
* multi-tenancy
* audit systems
* data retention controls
* reliability improvements
* operational scaling
* security hardening

---

# 10. Phase 8 — Autonomous Remediation

This is intentionally a later exploration.

Potential capabilities:

```text
RCA
 ↓
Suggested remediation
 ↓
Human approval
 ↓
Staging validation
 ↓
Production action
```

Autonomous production changes should not be part of the initial product assumption.

---

# 11. Roadmap Principle

The roadmap should not be interpreted as a fixed feature commitment.

Each phase should answer a question.

```text
Phase 1:
Does evidence-first investigation work?

Phase 2:
Does agentic investigation outperform simpler approaches?

Phase 3:
Does Generative UI improve investigation?

Phase 4:
Does the concept survive real integrations?

Phase 5:
Does MCP meaningfully improve extensibility?

Phase 6:
Does investigation context create reusable knowledge?
```

---

# 12. Core Principle

> **AVENIQ should earn complexity through demonstrated value.**
