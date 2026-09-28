# AVENIQ — Reliability Model

## 1. Purpose

Reliability is a foundational product requirement for AVENIQ.

The system operates in a context where incorrect conclusions can waste engineering time or cause inappropriate remediation.

Therefore:

> **AVENIQ should optimize for trustworthy investigation rather than impressive AI answers.**

---

# 2. What Reliability Means

Reliability does not mean:

> "The AI always knows the answer."

Instead, reliability means:

> **The system behaves appropriately given the quality and availability of evidence.**

That includes knowing when it does not know.

---

# 3. Desired Reliability Behavior

```text
Strong evidence
      ↓
Strong conclusion

Partial evidence
      ↓
Probable hypothesis + explicit uncertainty

Conflicting evidence
      ↓
Multiple hypotheses + investigation

Insufficient evidence
      ↓
Question / evidence request

No useful evidence
      ↓
Inconclusive investigation
```

This behavior is preferable to generating a definitive answer in every situation.

---

# 4. Reliability Dimensions

AVENIQ should eventually evaluate reliability across several dimensions.

## 4.1 Evidence Correctness

Did the system retrieve and represent evidence correctly?

---

## 4.2 Evidence Relevance

Was the evidence actually relevant to the incident?

---

## 4.3 Evidence Coverage

Did the investigation examine enough relevant dimensions?

For example:

```text
Service
+
Dependency
+
Change
+
Telemetry
+
Impact
```

---

## 4.4 Temporal Consistency

Do the proposed causal relationships make sense chronologically?

A cause generally cannot occur after its effect.

---

## 4.5 Cross-Source Consistency

Do independent sources agree?

For example:

```text
Logs:
connection failures ↑

Metrics:
connection utilization ↑

Deployment:
configuration changed
```

Agreement increases support for a hypothesis.

---

## 4.6 Contradiction Handling

Does the system actively recognize evidence that challenges its hypothesis?

---

## 4.7 RCA Correctness

Did the final RCA correctly identify the actual cause?

---

## 4.8 Investigation Efficiency

How much time and manual effort did AVENIQ save?

Correctness without useful efficiency improvement would limit the product's value.

---

# 5. Reliability Is Not One Number

A single "AI confidence: 94%" value is insufficient.

A richer representation might look like:

```text
Evidence coverage       High
Source agreement        High
Temporal consistency    High
Contradictions          Low
Missing telemetry       Medium
RCA status              Probable
```

The exact scoring system should be determined through experimentation.

---

# 6. Evidence Quality Levels

A conceptual evidence classification:

| Level          | Meaning                            |
| -------------- | ---------------------------------- |
| Direct         | Directly observed from a source    |
| Derived        | Deterministically calculated       |
| Correlated     | Multiple observations align        |
| Inferred       | Relationship proposed by reasoning |
| Human-provided | Supplied by an operator            |

These should not be silently treated as equivalent.

---

# 7. Safe Failure

A critical reliability feature is graceful failure.

If AVENIQ cannot establish an RCA, it should still provide:

* collected evidence
* investigation timeline
* investigated hypotheses
* evidence gaps
* unresolved questions
* suggested next actions

For example:

```text
No confirmed RCA.

Most likely:
Database connection exhaustion.

Supporting evidence:
...

Missing evidence:
No deployment configuration history available.

Next recommended investigation:
Inspect database connection configuration.
```

This is still valuable.

---

# 8. Human Escalation

AVENIQ should escalate when:

* hypotheses remain indistinguishable
* evidence conflicts
* required information is unavailable
* the investigation reaches a high-risk decision
* the agent cannot confidently select the next action

The human becomes another investigation participant rather than merely an approval gate.

---

# 9. Reliability Boundary

The MVP should establish explicit boundaries around autonomous behavior.

For example:

### Allowed

* retrieve telemetry
* correlate evidence
* investigate hypotheses
* generate summaries
* ask questions

### Restricted

* modify production configuration
* deploy code
* delete resources
* execute destructive commands

The investigation system should initially remain primarily **read-oriented**.

---

# 10. Measuring Reliability

Future evaluation should include benchmark incidents where the correct RCA is known.

Potential metrics:

```text
RCA accuracy
Evidence precision
Evidence recall
False RCA rate
Unsupported claim rate
Investigation completion rate
Human intervention rate
Time to useful context
Time to correct RCA
```

---

# 11. Reliability Principle

> **When AVENIQ cannot confidently establish the truth, it should establish what is known, what is unknown, and what evidence would reduce the uncertainty.**
