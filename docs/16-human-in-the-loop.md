# AVENIQ — Human in the Loop

## 1. Purpose

AVENIQ is intended to reduce the amount of manual investigation required during incidents while preserving human control.

The system should therefore treat humans neither as:

* a required operator for every step, nor
* an unnecessary participant after automation begins.

Instead, the human becomes an **investigation collaborator**.

---

# 2. Core Principle

> **AVENIQ should autonomously investigate where evidence is sufficient and involve a human where human context can materially improve the investigation.**

---

# 3. When Human Input Is Useful

AVENIQ may ask for human input when:

* evidence is ambiguous
* two hypotheses remain plausible
* required telemetry is unavailable
* organizational context is unavailable
* an intentional change cannot be inferred
* business impact cannot be determined automatically
* the user has knowledge unavailable to connected systems

---

# 4. Example

Suppose AVENIQ finds:

```text
Deployment occurred
        ↓
Error rate increased
```

It may ask:

> "Was this deployment intentionally limited to the affected region?"

The engineer may answer:

> "Yes. This was a regional canary."

That answer becomes an investigation input.

It may cause AVENIQ to investigate regional configuration rather than treating the deployment itself as the complete explanation.

---

# 5. Human Input as Evidence

Human responses should be represented separately from machine-observed evidence.

Conceptually:

```text
Evidence
├── Machine observation
├── Derived observation
├── External system record
└── Human-provided information
```

This distinction should remain visible.

---

# 6. Types of Human Interaction

## 6.1 Clarification

The system needs missing contextual information.

Example:

> "Which deployment was considered suspicious?"

---

## 6.2 Disambiguation

Multiple hypotheses remain plausible.

Example:

> "Should I investigate the database or deployment path first?"

---

## 6.3 Direction

The engineer explicitly changes investigation focus.

Example:

> "Ignore infrastructure for now and investigate application changes."

---

## 6.4 Validation

The system presents a conclusion for human review.

Example:

> "Does this match what you observed during the incident?"

---

## 6.5 Override

The user can reject an investigation assumption.

Example:

> "That deployment is unrelated. It was a documentation-only change."

The system should then update the investigation context accordingly.

---

# 7. Avoid Excessive Questioning

Human interaction itself has a cost.

AVENIQ should not ask questions merely because asking is easy.

A question should ideally satisfy:

> **The answer is likely to materially change the investigation.**

---

# 8. Question Quality

Good:

> "The database and deployment hypotheses are both plausible. Was the connection-pool configuration changed in this deployment?"

Poor:

> "Can you provide more information?"

Questions should be:

* specific
* contextual
* actionable
* explainable

---

# 9. Human Review

Before presenting a high-impact RCA as confirmed, AVENIQ may provide:

```text
RCA Candidate
Evidence
Contradictions
Uncertainty
```

and allow the engineer to:

* accept
* reject
* modify
* continue investigating

---

# 10. Autonomous Mode

The system should support investigations where the engineer does not continuously interact.

For example:

```text
Incident arrives
      ↓
Agent investigates
      ↓
Evidence gathered
      ↓
RCA candidate produced
      ↓
Engineer reviews when available
```

This supports the productivity goal of allowing engineers to focus on other work.

---

# 11. Interactive Mode

The engineer can also actively guide the investigation.

```text
User
 ↓
Question
 ↓
Agent investigation
 ↓
Generated UI
 ↓
User redirects investigation
 ↓
Agent continues
```

The two modes should use the same underlying investigation state.

---

# 12. Human-in-the-Loop Principle

The objective is not:

> "Keep a human in every loop."

It is:

> **"Keep a human in control of consequential uncertainty."**
