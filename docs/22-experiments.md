# AVENIQ — Experiments

## 1. Purpose

Experiments should validate assumptions before significant engineering effort is invested.

The project should be developed as a sequence of hypotheses rather than as a predetermined implementation.

---

# 2. Experiment 01 — Is Evidence Aggregation Useful?

### Hypothesis

Engineers can reach an RCA faster when relevant evidence from multiple sources is presented in one investigation context.

### Compare

```text
Manual multi-tool workflow
vs
Aggregated evidence view
```

### Measure

* time to useful context
* time to RCA
* number of tool switches
* subjective effort

---

# 3. Experiment 02 — Agentic vs Deterministic Investigation

### Hypothesis

Agentic investigation performs better when the next useful query cannot be predetermined.

### Compare

```text
Deterministic investigation workflow
vs
Agent-driven investigation
```

The comparison should be made across incidents with different failure patterns.

---

# 4. Experiment 03 — Evidence-First vs Answer-First AI

### Hypothesis

An evidence-first architecture produces more trustworthy RCA than asking an LLM to directly infer the root cause from retrieved context.

### Compare

```text
Evidence → structured reasoning → RCA
```

against:

```text
Retrieved context → direct LLM RCA
```

### Measure

* RCA accuracy
* unsupported claims
* evidence coverage
* false RCA rate

---

# 5. Experiment 04 — One-Shot vs Conversational Investigation

### Hypothesis

Allowing the agent to ask targeted questions improves correctness when telemetry is incomplete.

### Compare

```text
One-shot investigation
vs
Iterative human-assisted investigation
```

---

# 6. Experiment 05 — Trace-Dependent vs Multi-Signal Correlation

### Hypothesis

An investigation model that does not depend on trace IDs is more robust across observability maturity levels.

### Compare

```text
Trace-centric investigation
vs
Logs + metrics + changes + traces when available
```

---

# 7. Experiment 06 — Static Dashboard vs Generative UI

### Hypothesis

An incident-specific UI reduces the effort required to inspect relevant evidence.

### Compare

```text
Static incident dashboard
vs
Generated investigation view
```

Measure:

* time to relevant evidence
* interactions
* component relevance
* engineer preference

---

# 8. Experiment 07 — Single Agent vs Specialized Agents

### Hypothesis

Separating investigation responsibilities can improve reliability and controllability.

### Compare

```text
Single general agent
vs
Orchestrator + specialized agents
```

This should be tested rather than assumed.

---

# 9. Experiment 08 — MCP vs Direct Connectors

### Hypothesis

MCP can simplify integration of heterogeneous operational capabilities without coupling the investigation engine to individual vendors.

Evaluate:

* development effort
* tool reliability
* agent usability
* observability
* integration complexity

---

# 10. Experiment 09 — Automatic RCA vs Human Verification

### Hypothesis

Human verification materially improves reliability for ambiguous incidents without eliminating the productivity benefit.

Measure:

* correction rate
* investigation duration
* user trust
* false RCA rate

---

# 11. Experiment 10 — Generated Knowledge Articles

### Hypothesis

A knowledge article generated directly from the structured investigation context is more useful and less error-prone than one generated independently from the final RCA text.

---

# 12. Experiment Discipline

Every experiment should document:

```text
Hypothesis
Baseline
Variables
Dataset / incidents
Procedure
Metrics
Result
Conclusion
Next decision
```

---

# 13. Decision Rule

An experiment should be allowed to invalidate an architectural assumption.

The project should not preserve a feature simply because it was part of the original vision.

---

# 14. Core Principle

> **AVENIQ's architecture should emerge from validated investigation needs, not from the novelty of using agents, MCP, or Generative UI.**
