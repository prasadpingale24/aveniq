# AVENIQ — Glossary

## A

### Agent

An AI-driven software component capable of selecting actions, using tools, interpreting results, and continuing an investigation toward an objective.

### Agentic Investigation

An investigation in which an AI system dynamically determines what information to retrieve and what to investigate next.

### Alert

A signal indicating that a system may be experiencing an abnormal condition.

---

## B

### Blast Radius

The scope of systems, components, users, regions, requests, or business capabilities affected by an incident.

---

## C

### Context

The collection of information required to understand an incident and perform meaningful investigation.

### Correlation

The process of connecting observations across time, services, telemetry sources, deployments, or other entities.

### Correlation ID

An identifier used to associate related operations or events across components.

---

## D

### Distributed Tracing

A mechanism for following a request across multiple services and recording the operations involved.

---

## E

### Evidence

An observable piece of information used to support, contradict, or contextualize an investigation hypothesis.

### Evidence Gap

Information that would materially help an investigation but is unavailable.

### Evidence Provenance

Information describing where evidence came from and how it was obtained.

---

## G

### Generative UI

An interface whose components and presentation are dynamically selected or generated based on the current context rather than being entirely predefined.

---

## H

### Human-in-the-Loop

A workflow in which a human can provide information, direction, validation, or intervention during an automated process.

### Hypothesis

A candidate explanation for observed incident behavior.

---

## I

### Incident

An event or sequence of events causing, or potentially causing, degradation of a system or business capability.

### Incident Context

The structured representation of everything currently known about an incident.

### Investigation

The process of gathering and interpreting evidence to determine what happened, why it happened, and what was affected.

### Investigation State

The current structured state of an investigation, including known evidence, hypotheses, questions, and unresolved uncertainties.

---

## M

### MCP

Model Context Protocol, a protocol for exposing tools and contextual capabilities to AI systems in a standardized manner.

### MTTR

Mean Time to Recovery or Mean Time to Repair, commonly used as a measure of how quickly an incident is resolved.

---

## O

### Observability

The ability to understand the internal state and behavior of a system through information exposed by that system.

### Observability Signal

A measurable or inspectable indication of system behavior, such as logs, metrics, traces, or events.

---

## R

### RCA

Root Cause Analysis.

A structured explanation of why an incident occurred, supported by evidence.

### Root Cause

The underlying condition that materially caused or initiated an incident.

---

## T

### Telemetry

Data emitted by a system that describes its behavior.

Common forms include:

* logs
* metrics
* traces
* events

### Trace ID

An identifier associated with a distributed trace, allowing related operations to be correlated.

---

## U

### Uncertainty

The degree to which the available evidence is insufficient to establish a conclusion with confidence.

---

## V

### Verification

The process of checking whether a hypothesis is supported by additional evidence.

---

# AVENIQ-Specific Terms

### Evidence-First

An architectural principle in which conclusions are derived from structured, inspectable evidence rather than generated independently of the underlying observations.

### Investigation Context

AVENIQ's evolving representation of the incident, including observations, relationships, hypotheses, evidence gaps, and human input.

### Investigation View

A dynamically composed UI representing the current state of an investigation.

### Evidence Aggregation

The collection and normalization of relevant observations from multiple operational systems into a unified investigation context.

### Evidence-Backed RCA

An RCA where important claims can be traced back to supporting observations.

### Observability Lesson

A post-incident finding describing how instrumentation, telemetry, correlation, or alerting could be improved to make similar incidents easier to detect or investigate.

---

# Core Vocabulary Principle

AVENIQ should prefer precise technical terminology over marketing terminology when describing the actual investigation process.

> **The system may be intelligent, but its vocabulary and evidence should remain inspectable.**
