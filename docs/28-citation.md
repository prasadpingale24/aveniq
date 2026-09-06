# AVENIQ — Citation Registry

> Canonical bibliography for research, market analysis, competitive analysis, technology decisions, and pitch-deck evidence.

**Last reviewed:** September 2026

---

## 1. Purpose

This document is the canonical source registry for AVENIQ.

It exists separately from `market-analysis.md` so that:

* research claims remain traceable
* sources can be reused across documentation
* pitch-deck preparation does not require repeating research
* competitor/product claims can be verified independently
* outdated findings can be replaced without rewriting every document

This document should contain **sources, not conclusions**.

Interpretation and conclusions belong in the documents that cite these sources.

---

# 2. Citation Convention

Sources use stable identifiers.

Example:

```text
[OBS-01]
```

A document can therefore say:

> Observability complexity remains a significant concern for engineering teams. [OBS-01]

The reader can locate `[OBS-01]` in this document and inspect the original source.

---

# 3. Source Categories

| Prefix  | Category                                     |
| ------- | -------------------------------------------- |
| `OBS`   | Observability research and surveys           |
| `INC`   | Incident management / engineering operations |
| `CLOUD` | Cloud-native ecosystem research              |
| `RCA`   | Root-cause analysis research                 |
| `MCP`   | Model Context Protocol                       |
| `GENUI` | Generative UI                                |
| `COMP`  | Competitive / adjacent products              |
| `OTEL`  | OpenTelemetry                                |
| `AI`    | AI-assisted software / operations research   |

---

# 4. Observability Industry Research

## [OBS-01] — Grafana Labs Observability Survey 2026

**Organization:** Grafana Labs
**Year:** 2026
**Type:** Industry survey

### Why AVENIQ cares

This is one of the most useful current sources for establishing the broader observability environment.

It covers:

* observability adoption
* SaaS vs self-managed observability
* complexity
* signal-to-noise problems
* centralized observability
* AI in observability
* business metrics
* open standards

### Relevant findings

The 2026 survey collected **1,363 responses**.

Among the reported findings:

* 92% see value in AI surfacing anomalies and issues before downtime.
* 77% say open source/open standards are important to their observability strategy.
* 77% report saving time or money through centralized observability.
* 38% identify complexity/overhead as their biggest observability concern.
* 34% identify signal-to-noise challenges as a major concern.
* 49% use SaaS observability in some form.

### AVENIQ relevance

Strong evidence for:

```text
Observability adoption
        +
Growing telemetry
        +
Complexity
        +
AI opportunity
        +
Need for consolidation/context
```

### Caveat

Grafana Labs commissioned/conducted the survey, so it should be treated as vendor-originated industry research rather than an independent census.

**Source:**
[Grafana Labs — Observability Survey 2026](https://grafana.com/observability-survey/?utm_source=chatgpt.com)

---

## [OBS-02] — Grafana Labs: AI in Observability 2026

**Organization:** Grafana Labs
**Year:** 2026
**Type:** Survey analysis

### Why AVENIQ cares

Useful specifically for understanding how engineers view AI-assisted observability and the tension between AI usefulness and trust.

The report discusses AI use cases including:

* anomaly detection
* forecasting
* RCA assistance
* onboarding
* autonomous action

It also discusses concerns about AI operating without sufficient oversight.

### AVENIQ relevance

This directly supports the product's:

> **evidence + human verification + controlled autonomy**

positioning.

**Source:**
[Grafana Labs — AI in Observability in 2026](https://grafana.com/blog/observability-survey-AI-2026/?utm_source=chatgpt.com)

---

## [OBS-03] — Grafana Labs Observability Survey 2025

**Organization:** Grafana Labs
**Year:** 2025

### Why AVENIQ cares

Useful historical comparison for determining whether observability complexity and AI adoption are persistent trends rather than isolated 2026 findings.

Particularly relevant areas:

* alert fatigue
* unified observability
* OpenTelemetry
* MTTR
* observability maturity
* tool proliferation

**Source:**
[Grafana Labs — Observability Survey 2025](https://grafana.com/blog/observability-survey-takeaways/?utm_source=chatgpt.com)

---

## [OBS-04] — Splunk State of Observability 2025

**Organization:** Splunk
**Year:** 2025
**Sample:** 1,855 ITOps and engineering professionals

### Why AVENIQ cares

This is particularly useful for connecting observability with organizational and business outcomes.

### Relevant findings

Reported findings include:

* 74% say monitoring critical business processes is at least moderately important.
* 65% report that observability positively affects revenue.
* high-performing organizations use emerging technologies such as agentic AI more frequently.
* leading organizations report stronger observability ROI.

### AVENIQ relevance

Supports the argument that observability is moving beyond:

```text
Infrastructure health
```

toward:

```text
Business impact
+
engineering productivity
+
organizational resilience
```

**Source:**
[Splunk — State of Observability 2025](https://www.splunk.com/en_us/campaigns/state-of-observability.html?utm_source=chatgpt.com)

---

## [OBS-05] — New Relic Observability Forecast 2025

**Organization:** New Relic
**Year:** 2025
**Sample:** 1,700+ technology leaders

### Why AVENIQ cares

One of the strongest sources for the economic and operational case surrounding observability.

### Relevant findings

Reported findings include:

* high-impact outages can cost around $2M/hour
* 75% report positive ROI from observability
* 20% report 3–10x ROI
* AI monitoring adoption reached 54%
* 52% are actively consolidating observability tools

The report also identifies:

* AI-assisted troubleshooting
* automatic RCA
* predictive analytics

as important capabilities in the emerging intelligent-observability landscape.

### AVENIQ relevance

Particularly useful for pitch-deck sections covering:

```text
Why now?
Economic impact
AI adoption
Tool consolidation
RCA demand
```

### Caveat

Vendor-produced survey.

**Source:**
[New Relic — Observability Forecast 2025](https://newrelic.com/resources/report/observability-forecast/2025?utm_source=chatgpt.com)

**Report PDF:**
[New Relic — Observability Forecast 2025 PDF](https://newrelic.com/sites/default/files/2025-09/new-relic-2025-observability-forecast-report.pdf?utm_source=chatgpt.com)

---

## [OBS-06] — New Relic: Top Trends in Observability 2025

**Organization:** New Relic
**Year:** 2025

### Why AVENIQ cares

Useful companion material to OBS-05, particularly around the transition from traditional monitoring toward intelligent observability.

**Source:**
[New Relic — Top Trends in Observability: The 2025 Forecast](https://newrelic.com/blog/observability/top-trends-in-observability-the-2025-forecast-is-here?utm_source=chatgpt.com)

---

## [OBS-07] — Dynatrace State of Observability 2025

**Organization:** Dynatrace
**Year:** 2025
**Sample:** 842 senior technology leaders

### Why AVENIQ cares

Useful for understanding the enterprise observability + AI intersection.

### Relevant findings

Reported findings include:

* 70% increased observability budgets.
* 75% planned further budget increases.
* AI capabilities became a leading observability buying criterion.
* 98% reported using AI for security compliance.
* only 28% reported currently using AI to align observability data with business outcomes.

### AVENIQ relevance

The particularly interesting signal is the gap between:

```text
Large investment
        ↓
Large amounts of observability data
        ↓
AI adoption
        ↓
Still-limited connection to business outcomes
```

This supports AVENIQ's interest in contextualizing technical evidence according to the person consuming it.

### Caveat

Enterprise-focused sample and vendor-commissioned research.

**Source:**
[Dynatrace — State of Observability 2025](https://www.dynatrace.com/info/ebooks/the-state-of-observability/?utm_source=chatgpt.com)

**Announcement / findings:**
[Dynatrace — State of Observability 2025 findings](https://www.dynatrace.com/news/press-release/state-of-observability-2025/?utm_source=chatgpt.com)

---

## [OBS-08] — Elastic / Dimensional Research: Landscape of Observability 2025

**Organization:** Elastic / Dimensional Research
**Year:** 2025

### Why AVENIQ cares

Useful independent-research-partner material around observability maturity, telemetry, AI/ML, and operational practices.

**Source:**
[Elastic — Landscape of Observability in 2025](https://www.elastic.co/pdf/dimensional-research-landscape-of-observability-in-2025-futureproofing-it.pdf?utm_source=chatgpt.com)

---

## [OBS-09] — DZone + Honeycomb Intelligent Observability Trend Report 2025

**Organizations:** DZone + Honeycomb
**Year:** 2025

### Why AVENIQ cares

Relevant to:

* observability maturity
* debugging
* observability architecture
* tooling
* AI-driven observability
* collaboration between automation and human expertise

**Source:**
[DZone + Honeycomb — Intelligent Observability Trend Report 2025](https://www.honeycomb.io/resources/reports/dzone-honeycomb-2025-intelligent-observability-trend-report?utm_source=chatgpt.com)

---

## [OBS-10] — Honeycomb Research Library

**Organization:** Honeycomb

### Why AVENIQ cares

A useful collection rather than one individual survey.

Particularly relevant materials include research on:

* distributed tracing
* OpenTelemetry
* observability costs
* AI and LLM observability
* debugging
* engineering practices

**Source:**
[Honeycomb — Research & Reports](https://www.honeycomb.io/resources/reports?utm_source=chatgpt.com)

**Whitepapers:**
[Honeycomb — Whitepapers](https://www.honeycomb.io/resources/whitepapers?utm_source=chatgpt.com)

---

## [OBS-11] — LogicMonitor 2026 Observability & AI Outlook

**Organization:** LogicMonitor
**Year:** 2026
**Sample:** 100 VP+ IT decision-makers with observability budget authority

### Why AVENIQ cares

This source is particularly close to AVENIQ's problem statement.

The report explicitly discusses:

* thousands of alerts
* massive telemetry volumes
* context switching
* manual correlation across platforms
* infrastructure visibility gaps
* tool consolidation
* automated correlation
* RCA
* AI adoption

### Relevant findings

Reported findings include:

* 96% expect observability spending to hold steady or grow.
* 84% are pursuing or considering tool consolidation.
* 67% are likely to switch observability platforms within 1–2 years.
* 59% are dissatisfied with their platform's ability to deliver insights.
* only 4% are described as having reached full operational AI maturity.

### AVENIQ relevance

Potentially one of the strongest market sources for:

> "The problem isn't necessarily absence of telemetry; it is turning increasing telemetry and multiple systems into actionable insight."

### Caveat

Small sample of 100 decision-makers and vendor-originated research.

**Source:**
[LogicMonitor — 2026 Observability & AI Outlook](https://www.logicmonitor.com/resources/2026-observability-ai-trends-outlook?utm_source=chatgpt.com)

---

# 5. Cloud-Native Ecosystem Research

## [CLOUD-01] — CNCF Annual Cloud Native Survey 2026

**Organization:** Cloud Native Computing Foundation
**Year:** 2026

### Why AVENIQ cares

Provides broader evidence for the scale and maturity of the cloud-native environments in which observability complexity becomes relevant.

### Relevant finding

82% of container users reported running Kubernetes in production.

### AVENIQ relevance

Supports the environmental assumption that distributed, containerized infrastructure is now mainstream rather than an edge case.

**Source:**
[CNCF — Annual Cloud Native Survey 2026](https://www.cncf.io/reports/the-cncf-annual-cloud-native-survey/?utm_source=chatgpt.com)

---

## [CLOUD-02] — CNCF State of Cloud Native Development Q1 2025

**Organization:** CNCF + SlashData
**Year:** 2025
**Sample:** 10,000+ developers

### Why AVENIQ cares

Useful for broader developer/cloud-native adoption context.

**Source:**
[CNCF — State of Cloud Native Development Q1 2025](https://www.cncf.io/reports/state-of-cloud-native-development-q1-2025/?utm_source=chatgpt.com)

---

## [CLOUD-03] — CNCF Observability Technology Radar 2025

**Organization:** CNCF
**Year:** 2025

### Why AVENIQ cares

Useful for understanding how professional developers perceive observability technologies and related platform tooling.

**Source:**
[CNCF — Tech Radar: Observability Technologies & API Management and Dev Experience](https://www.cncf.io/reports/radar-observability-technologies-api-management-and-dev-experience/?utm_source=chatgpt.com)

---

# 6. Incident Management & Engineering Operations

## [INC-01] — PagerDuty Research

**Organization:** PagerDuty

### Why AVENIQ cares

PagerDuty maintains a substantial body of research around:

* incident response
* digital operations
* on-call
* automation
* operational efficiency
* AI in operations

This category is valuable for validating the operational side of the problem rather than relying exclusively on observability vendors.

**Source:**
[PagerDuty — Research & Reports](https://www.pagerduty.com/resources/research/?utm_source=chatgpt.com)

---

## [INC-02] — DORA / Google Cloud Research

**Organization:** Google Cloud / DORA

### Why AVENIQ cares

DORA research provides a broader engineering-performance context around:

* software delivery
* operational performance
* developer productivity
* reliability
* AI-assisted development

It is useful when connecting incident-response improvements to broader engineering outcomes.

**Source:**
[DORA — State of DevOps / Research](https://cloud.google.com/devops/state-of-devops?utm_source=chatgpt.com)

---

## [INC-03] — DORA State of AI-assisted Software Development 2025

**Organization:** DORA / Google Cloud
**Year:** 2025

### Why AVENIQ cares

Useful for understanding how AI is changing software engineering and where AI introduces or shifts operational challenges.

Honeycomb maintains access to the report as well.

**Source:**
[Honeycomb — DORA State of AI-assisted Software Development 2025](https://www.honeycomb.io/resources/reports?utm_source=chatgpt.com)

---

# 7. OpenTelemetry

## [OTEL-01] — OpenTelemetry Documentation

**Organization:** OpenTelemetry

### Why AVENIQ cares

Primary technical reference for:

* traces
* metrics
* logs
* context propagation
* semantic conventions
* instrumentation

AVENIQ should use this source when discussing the telemetry foundation rather than relying on vendor-specific terminology.

**Source:**
[OpenTelemetry Documentation](https://opentelemetry.io/docs/?utm_source=chatgpt.com)

---

## [OTEL-02] — OpenTelemetry Collector Follow-up Survey 2026

**Organization:** OpenTelemetry
**Year:** 2026

### Why AVENIQ cares

Useful evidence for the uneven adoption and collection of different telemetry signals.

This is particularly relevant to the AVENIQ decision:

> tracing should be valuable, but not mandatory.

**Source:**
[OpenTelemetry — Collector Follow-up Survey Analysis](https://opentelemetry.io/blog/2026/otel-collector-follow-up-survey-analysis/?utm_source=chatgpt.com)

---

# 8. Root Cause Analysis Research

## [RCA-01] — GALA+: Graph-Augmented LLM Agents for RCA

**Authors:** Tian et al.
**Year:** 2026

### Why AVENIQ cares

This is one of the closest academic references to AVENIQ's proposed investigation model.

The work identifies challenges including:

* heterogeneous telemetry
* complex service dependency graphs
* unconstrained exploration
* hallucination
* incomplete incident response

It proposes graph-guided agentic investigation using multimodal evidence.

### Particularly relevant concept

The paper evaluates RCA quality beyond simple text similarity using human-oriented evaluation.

### AVENIQ relevance

Strong support for exploring:

```text
Service relationships
+
Multi-modal evidence
+
Agentic investigation
+
Reliability evaluation
```

**Source:**
[GALA+ — arXiv](https://arxiv.org/abs/2608.08968?utm_source=chatgpt.com)

---

## [RCA-02] — DiagGuard

**Year:** 2026

### Why AVENIQ cares

Particularly relevant to the evidence-first philosophy.

The work challenges the assumption that merely producing a correct endpoint answer means an RCA agent performed a good investigation.

It emphasizes evaluating the **evidentiary basis and fault-propagation path** of an investigation.

### AVENIQ relevance

This maps closely to:

```text
RCA claim
    ↓
Supporting evidence
    ↓
Fault propagation
    ↓
Verification
```

rather than:

```text
LLM answer
    ↓
"confidence: 92%"
```

**Source:**
[DiagGuard — arXiv](https://arxiv.org/abs/2608.21310?utm_source=chatgpt.com)

---

## [RCA-03] — OpsHarness

**Year:** 2026

### Why AVENIQ cares

Examines how production RCA performance depends not only on the underlying model but also on the surrounding agent harness.

This is relevant to AVENIQ's architecture because the project is explicitly experimenting with:

* orchestration
* tools
* investigation state
* evidence
* specialized capabilities
* evaluation

**Source:**
[OpsHarness — arXiv](https://arxiv.org/abs/2608.25661?utm_source=chatgpt.com)

---

# 9. Model Context Protocol

## [MCP-01] — Model Context Protocol Specification

**Organization:** Model Context Protocol

### Why AVENIQ cares

Canonical technical reference for exposing tools and context to AI applications.

Relevant primitives include:

* tools
* resources
* prompts
* lifecycle
* authorization

**Source:**
[Model Context Protocol — Specification](https://modelcontextprotocol.io/specification/2025-11-25?utm_source=chatgpt.com)

---

## [MCP-02] — MCP Server Features

### Why AVENIQ cares

Particularly relevant to AVENIQ's integration layer.

MCP distinguishes:

```text
Prompts
Resources
Tools
```

with different control relationships.

This is useful when designing how agents interact with operational systems.

**Source:**
[MCP — Server Features](https://modelcontextprotocol.io/specification/2025-06-18/server/index?utm_source=chatgpt.com)

---

## [MCP-03] — MCP Repository

**Organization:** Model Context Protocol

### Why AVENIQ cares

Canonical implementation ecosystem and source for schemas/specification development.

**Source:**
[Model Context Protocol — GitHub](https://github.com/modelcontextprotocol/modelcontextprotocol?utm_source=chatgpt.com)

---

# 10. Generative UI

## [GENUI-01] — Google Research: Generative UI

**Organization:** Google Research
**Year:** 2025

### Why AVENIQ cares

Provides research grounding for interfaces that dynamically adapt to a user's prompt/context rather than always rendering the same predefined interface.

### AVENIQ relevance

Supports the fundamental UI hypothesis:

```text
User intent
+
Context
+
Available information
        ↓
Appropriate interface
```

**Source:**
[Google Research — Generative UI](https://research.google/blog/generative-ui-a-rich-custom-visual-interactive-user-experience-for-any-prompt/?utm_source=chatgpt.com)

---

## [GENUI-02] — Google Cloud: What Is Generative UI?

**Organization:** Google Cloud

### Why AVENIQ cares

Useful practical explanation of different approaches to Generative UI, from controlled component selection to more open-ended generation.

This directly informs AVENIQ's decision to begin with a constrained component library.

**Source:**
[Google Cloud — What Is Generative UI?](https://cloud.google.com/discover/generative-ui?utm_source=chatgpt.com)

---

## [GENUI-03] — Google A2UI

**Organization:** Google
**Initial public release:** 2025
**Current evolution:** 2026

### Why AVENIQ cares

A2UI is highly relevant because it addresses the communication of agent-generated interface intent to applications.

It is evidence that agent-driven UI is evolving toward standardized, portable interfaces rather than remaining only a collection of demos.

**Source:**
[Google Developers — Introducing A2UI](https://developers.googleblog.com/introducing-a2ui-an-open-project-for-agent-driven-interfaces/?utm_source=chatgpt.com)

---

## [GENUI-04] — A2UI v0.9

**Organization:** Google
**Year:** 2026

### Why AVENIQ cares

The 2026 update describes A2UI as a framework-agnostic standard for communicating UI intent while allowing applications to retain their own component catalogs.

This is especially relevant to AVENIQ's proposed:

```text
Agent
 ↓
UI intent
 ↓
Controlled component registry
 ↓
Rendered investigation view
```

architecture.

**Source:**
[Google Developers — A2UI v0.9](https://developers.googleblog.com/en/a2ui-v0-9-generative-ui/?utm_source=chatgpt.com)

---

## [GENUI-05] — Flutter GenUI

**Organization:** Flutter

### Why AVENIQ cares

Useful implementation reference for agent-generated interfaces using a controlled widget/component ecosystem.

**Source:**
[Flutter GenUI — GitHub](https://github.com/flutter/genui?utm_source=chatgpt.com)

---

## [GENUI-06] — OpenUI

### Why AVENIQ cares

Useful reference for representing and rendering interactive UI components from agent output.

**Source:**
[OpenUI — Generative UI Documentation](https://www.openui.com/docs/agent/core-concepts/generative-ui?utm_source=chatgpt.com)

---

# 11. Direct Competitive / Adjacent Product Evidence

This section is intentionally separate from industry surveys.

These sources are important because they demonstrate that parts of AVENIQ's proposed workflow are already becoming products.

---

## [COMP-01] — Google Gemini Cloud Assist

**Organization:** Google Cloud

### Why AVENIQ cares

Google positions Cloud Assist as an agentic partner for cloud operations across:

* application design
* deployment
* monitoring
* troubleshooting
* optimization

The current product direction includes multi-agent reasoning and iterative tool calls.

**Source:**
[Google Cloud — Gemini Cloud Assist](https://cloud.google.com/products/gemini/cloud-assist?utm_source=chatgpt.com)

---

## [COMP-02] — Gemini Cloud Assist Investigations

**Organization:** Google Cloud

### Why AVENIQ cares

This is a **directly adjacent product** to AVENIQ.

Google describes Investigations as an RCA capability for complex distributed infrastructure and applications.

It analyzes information such as:

* logs
* configurations
* metrics

and produces observations and probable causes.

The workflow can be initiated from operational contexts such as alerts and logs.

### Critical implication for AVENIQ

The project should **not** claim:

> "AI-powered observability RCA doesn't exist."

It clearly does.

The competitive question becomes:

> **What can AVENIQ demonstrate that existing observability-native investigation products do not?**

Potential differentiation hypotheses remain:

* cross-tool rather than single-platform investigation
* evidence-centric investigation state
* explicit evidence provenance
* reliability/evidence evaluation
* human-guided iterative investigation
* personalized Generative UI
* post-incident knowledge generation
* observability lessons

These are hypotheses, not yet validated differentiators.

**Source:**
[Google Cloud — Gemini Cloud Assist Investigations](https://docs.cloud.google.com/cloud-assist/investigations?hl=en&utm_source=chatgpt.com)

---

## [COMP-03] — Gemini Cloud Assist RCA Announcement

**Organization:** Google Cloud
**Date:** August 22, 2025

### Why AVENIQ cares

This announcement explains Google's motivation for AI-driven RCA:

* distributed systems
* high data volume
* intertwined dependencies
* ephemeral failures
* time-consuming traditional troubleshooting

It describes analysis across multiple sources and synthesis into probable root causes and next steps.

**Source:**
[Google Cloud Blog — Gemini Cloud Assist Investigations](https://cloud.google.com/blog/products/management-tools/gemini-cloud-assist-investigations-performs-root-cause-analysis/?utm_source=chatgpt.com)

---

## [COMP-04] — Gemini Cloud Assist MCP `investigate_issue`

**Organization:** Google Cloud

### Why AVENIQ cares

This is particularly significant for AVENIQ because it demonstrates the convergence of:

```text
MCP
+
Agent orchestration
+
Parallel hypothesis evaluation
+
Diagnostic runbooks
+
RCA
```

Google's MCP reference describes `investigate_issue` as an investigation orchestrator capable of multi-step investigation and parallelized hypothesis evaluation.

### AVENIQ implication

MCP + agentic RCA should be treated as an **active competitive direction**, not a novel concept by itself.

**Source:**
[Google Cloud — Investigate Issue MCP Tool](https://docs.cloud.google.com/cloud-assist/reference/mcp/tools_list/investigate_issue?utm_source=chatgpt.com)

---

## [COMP-05] — Google Cloud Assist Investigation Management

### Why AVENIQ cares

Useful for understanding investigation lifecycle concepts such as:

* creating investigations
* viewing investigations
* modifying investigations
* investigation permissions

**Source:**
[Google Cloud — Manage Cloud Assist Investigations](https://docs.cloud.google.com/gemini/docs/cloud-assist/manage-investigations?utm_source=chatgpt.com)

---

# 12. Competitive Landscape Sources

These are useful starting points for future competitive analysis.

## [COMP-06] — Gartner Magic Quadrant for Observability Platforms 2025

**Organization:** Gartner
**Year:** 2025

### Why AVENIQ cares

Useful for understanding the established observability-platform market and major vendors.

Use primarily for:

* competitive landscape
* vendor categorization
* platform capabilities
* enterprise positioning

**Source:**
[Gartner — Magic Quadrant for Observability Platforms 2025](https://www.gartner.com/en/documents/6688834?utm_source=chatgpt.com)

---

## [COMP-07] — Gartner Critical Capabilities for Observability Platforms 2025

**Organization:** Gartner
**Year:** 2025

### Why AVENIQ cares

Potentially more useful than the Magic Quadrant for capability-level analysis.

Relevant areas include:

* telemetry exploration
* actionable insights
* automated response
* SRE/platform operations

**Source:**
[Gartner — Critical Capabilities for Observability Platforms 2025](https://www.gartner.com/en/documents/6695234?utm_source=chatgpt.com)

---

# 13. Research Interpretation Matrix

The following is not a claim about the market. It is a guide for **what each source should be used to substantiate**.

| Question                                              | Strong sources                 |
| ----------------------------------------------------- | ------------------------------ |
| Is observability widely adopted?                      | OBS-01, CLOUD-01               |
| Is observability becoming more complex?               | OBS-01, OBS-05, OBS-11         |
| Is AI entering observability?                         | OBS-02, OBS-05, OBS-07         |
| Is there demand for AI-assisted RCA?                  | OBS-05, OBS-06, COMP-02        |
| Is tool consolidation occurring?                      | OBS-01, OBS-05, OBS-11         |
| Is alert/operational overload real?                   | OBS-01, OBS-03, OBS-04, OBS-11 |
| Is there economic impact from incidents?              | OBS-05, OBS-04                 |
| Is cloud-native infrastructure widespread?            | CLOUD-01, CLOUD-02             |
| Is tracing universally available?                     | OTEL-02                        |
| Is evidence-grounded RCA an active research area?     | RCA-01, RCA-02, RCA-03         |
| Is agentic investigation already commercialized?      | COMP-01, COMP-02               |
| Is MCP becoming relevant to agents/tools?             | MCP-01, MCP-03, COMP-04        |
| Is Generative UI becoming a real technical direction? | GENUI-01, GENUI-03, GENUI-04   |
| Are agent-generated interfaces becoming standardized? | GENUI-03, GENUI-04             |

---

# 14. Pitch Deck Source Shortlist

If the entire bibliography needs to be reduced to a small set for a pitch deck, start here.

### Problem

**OBS-01 — Grafana 2026**

Use for:

* complexity
* signal-to-noise
* centralized observability
* AI demand

### Operational Pain

**OBS-04 — Splunk 2025**

Use for:

* alerts
* operational collaboration
* business impact
* observability maturity

### Economic Urgency

**OBS-05 — New Relic 2025**

Use for:

* outage cost
* observability ROI
* AI-assisted troubleshooting
* tool consolidation

### Enterprise AI + Observability

**OBS-07 — Dynatrace 2025**

Use for:

* observability investment
* AI adoption
* business outcomes
* trust

### Infrastructure Scale

**CLOUD-01 — CNCF 2026**

Use for:

* Kubernetes/cloud-native adoption
* infrastructure complexity context

### Technology Timing

**MCP-01 — MCP Specification**

Use for:

* agent/tool interoperability

### Generative UI Timing

**GENUI-03 / GENUI-04 — Google A2UI**

Use for:

* agent-driven interfaces
* emerging standards
* production-oriented Generative UI

### Competitive Reality

**COMP-02 — Gemini Cloud Assist Investigations**

Use internally when positioning AVENIQ.

This source should prevent overclaiming novelty.

---

# 15. Sources That Should Be Treated Carefully

Vendor surveys are useful but have inherent limitations.

Examples include:

* Grafana
* Splunk
* New Relic
* Dynatrace
* LogicMonitor
* Honeycomb

They may have:

* vendor-specific audiences
* self-selection bias
* commercial incentives
* different definitions of observability
* different sampling methodologies

Therefore:

### Prefer

> "In Grafana Labs' 2026 survey of 1,363 respondents..."

over:

> "92% of companies want AI observability."

And:

> "New Relic reports that 52% of surveyed organizations are consolidating observability tools..."

over:

> "52% of organizations are consolidating tools."

---

# 16. Competitive Research Rule

A competitor appearing in this document does **not** automatically invalidate AVENIQ.

Instead, classify the overlap.

```text
Category 1
Same problem + same solution
        ↓
Direct competitor

Category 2
Same problem + adjacent solution
        ↓
Adjacent competitor

Category 3
Different problem + overlapping technology
        ↓
Technology precedent

Category 4
Same technology + different workflow
        ↓
Potential inspiration

Category 5
Research prototype
        ↓
Technical precedent
```

The goal is not to prove that AVENIQ has no competitors.

The goal is to understand:

> **What remains unsolved, underserved, or worth testing?**

---

# 17. AVENIQ Research Thesis

The sources collectively establish an environment in which:

```text
Cloud-native systems
        ↓
More distributed components
        ↓
More telemetry
        ↓
More operational complexity
        ↓
More pressure for faster resolution
        ↓
AI enters observability
        ↓
Agentic investigation emerges
        ↓
Adaptive interfaces emerge
```

However, this does **not** establish that AVENIQ itself is a necessary product.

The remaining product hypothesis is:

> **Can an evidence-centric, cross-source investigation layer—with explicit provenance, uncertainty handling, human collaboration, and personalized Generative UI—provide measurably better incident-investigation outcomes than existing tools and AI-assisted alternatives?**

That is the hypothesis the MVP and benchmark suite must answer.

---

# 18. Maintenance Rules

When adding a source:

1. Assign a new stable identifier.
2. Record the organization.
3. Record publication year/date when available.
4. Record sample size for surveys.
5. Explain why the source matters.
6. Record relevant findings without turning them into conclusions.
7. Include the canonical source.
8. State important methodological caveats.
9. Update the research interpretation matrix when necessary.
10. Never silently replace an existing source with a different document.

When a source becomes outdated:

```text
Keep old citation
+
mark historical
+
add newer source
```

rather than silently changing the meaning of an existing citation ID.

---

# 19. Final Principle

> **The citation registry exists to make AVENIQ's claims falsifiable.**

A strong pitch should not say:

> "The market proves our idea."

It should say:

> "The market evidence demonstrates a real and growing operational problem, existing products demonstrate that AI-assisted investigation is viable, and AVENIQ proposes a specific hypothesis about how evidence-centric investigation and adaptive interfaces could improve that workflow."
