# StockSense — Executive Summary

> **StockSense is an AI Decision Intelligence Platform for retailers.** It predicts
> inventory problems before they happen, explains why they are happening, and recommends
> the specific action to take — each with a confidence score and expected business impact —
> so retailers act before problems cost them money.
>
> **Tagline:** Helping retailers make smarter inventory decisions before problems happen.

This document is a one-read overview for recruiters, project reviewers, open-source
contributors, and potential investors. It summarizes the complete Phase 0 blueprint in
`/docs` (start at the [Documentation Index](README.md)).

---

## The Problem (and why it is worth solving)

Inventory is the largest working-capital commitment for most retailers, and it is
chronically mismanaged — not through negligence, but because the problem is hard and the
tools are backward-looking.

- Global **inventory distortion** (out-of-stocks + overstocks) is estimated at roughly
  **$1.77 trillion (2023)**, with out-of-stocks alone near **$1.2 trillion**.[^ihl]
- U.S. **retail shrink** reached about **1.6% of sales, $112.1 billion, in 2022**.[^nrf]
- Poor inventory management is estimated to cost retailers **3–8% of annual
  revenue**.[^lucent]

Existing software tells retailers *what happened*. The value has moved to the next three
questions: **what will happen, why, and what should I do?**

_Full evidence, with citations, in [Market Research](research/04-market-research.md)._

---

## The Product

StockSense is a **Decision Intelligence Engine** — the engine is the product; any
conversational assistant is only a thin window onto it. Its output is a **ranked, explained,
confidence-scored recommendation**, not a dashboard.

Traditional software says *"What happened."* StockSense says:

- **"What will happen"** — proactive demand forecasting and risk detection.
- **"Why it will happen"** — a plain-language explanation with supporting evidence.
- **"What action to take"** — a specific, prioritized recommendation the user approves.

**Every recommendation always includes:** reasoning, confidence, supporting data, and
business impact. The system **never** emits an unexplained output, and the **human always
makes the final decision** ([AI Philosophy](product/12-ai-philosophy.md)).

---

## Differentiation

StockSense is deliberately *not* an ERP, POS, IMS, CRM, dashboard tool, or generic chatbot.
Its defensible value is the **intersection of five properties** no incumbent delivers
together:

**Predictive · Explained · Prioritized by impact · Accessible to non-experts · Layered over
existing systems.**

| Category | What they do well | The gap StockSense fills |
| --- | --- | --- |
| IMS (Zoho, Shopify) | Record current stock | No prediction, no decisioning |
| ERP (SAP, Oracle, Dynamics) | Powerful enterprise planning | Too costly/complex for the target segment |
| Dashboards / BI | Visualize the past | Deliver charts, not decisions |
| Generic AI chatbots | Answer general questions | Not grounded, not proactive, not evidence-backed |
| Embedded AI copilots | Assist within a suite | AI is a feature, not the product |

_Detailed matrix in [Competitor Analysis](research/05-competitor-analysis.md) and
[Value Proposition](product/03-value-proposition.md)._

---

## Target Market

Independent and mid-sized retailers who carry physical inventory and cannot justify an
enterprise ERP: **retail stores, supermarkets, mini marts, pharmacies, and electronics
stores.** AI's inventory value is proven but **concentrated in enterprises**; this
underserved middle — blocked by cost, expertise, and integration barriers — is StockSense's
opportunity ([Target Customers](product/07-target-customers.md)).

---

## Architecture

An enterprise-grade **multi-agent Decision Intelligence Engine**. The suggested eight
agents were critically evaluated and expanded to **eleven** by adding a **Data Quality
Agent** (protects the evidence promise), a **Learning/Feedback Agent** (closes the loop),
and an **Orchestrator** (sequencing and end-to-end traceability).

```
Systems of Record → Integration → Data Quality → Inventory Intelligence
   → [Forecast · Risk Detection · Analytics] → Recommendation / Executive
   → Notification → Human (Approve / Modify / Reject) → Learning (feedback loop)
                        (Orchestrator spans all layers)
```

Explainability is **structural**: recommendations cannot be emitted without reasoning,
confidence, evidence, and impact ([Agent Architecture](architecture/13-agent-architecture.md),
[Agent Catalog](agents/agent-catalog.md)). The multi-agent rationale and orchestration
approach are finalized in [ADR-0010](architecture/adr/0010-multi-agent-architecture-rationale.md).
The engine operates under a platform-wide **AI Governance Framework**
([ADR-0007](architecture/adr/0007-ai-governance-framework.md)) and a defense-in-depth
**Security Architecture** ([ADR-0008](architecture/adr/0008-security-architecture.md)), on a
**frozen technology stack** ([ADR-0009](architecture/adr/0009-technology-stack.md)). Measurable
system qualities (availability, latency, RPO/RTO, and more) are specified in the
[Non-Functional Requirements](architecture/non-functional-requirements.md).

---

## Roadmap

- **V1 (MVP):** Prove the core loop — connect data, forecast, detect stockout/dead-stock
  risk, deliver ranked explained recommendations, human approves.
- **V2:** Advanced forecasting, more risk types (anomaly, expiry), executive summaries, the
  feedback loop, and a thin assistant interface.
- **V3:** Multi-store network optimization and strictly opt-in, reversible assisted
  execution for low-risk/high-confidence actions.

_Full plan in [Product Roadmap](planning/14-product-roadmap.md)._

---

## How Success Is Measured

Fewer stockouts, less dead stock, higher inventory turnover, freed working capital, less
time on manual analysis — with recommendation adoption, forecast accuracy, and confidence
calibration as leading indicators. Full KPI tree in
[Success Metrics](business/11-success-metrics.md).

---

## Key Decisions (ADRs)

**Ten** Architecture Decision Records capture the durable "why" behind StockSense:

| ADR | Decision |
| --- | --- |
| [ADR-0001](architecture/adr/0001-decision-intelligence-not-dashboards.md) | Decision Intelligence (not dashboards) |
| [ADR-0002](architecture/adr/0002-scope-boundaries-not-an-erp.md) | Product Scope Boundaries (not an ERP/POS/IMS/CRM) |
| [ADR-0003](architecture/adr/0003-human-in-the-loop-decisioning.md) | Human-in-the-Loop |
| [ADR-0004](architecture/adr/0004-explainable-ai-mandate.md) | Explainable AI |
| [ADR-0005](architecture/adr/0005-multi-agent-orchestration.md) | Multi-Agent Architecture |
| [ADR-0006](architecture/adr/0006-layer-over-systems-of-record.md) | Layer Over Existing Systems |
| [ADR-0007](architecture/adr/0007-ai-governance-framework.md) | AI Governance |
| [ADR-0008](architecture/adr/0008-security-architecture.md) | Security Architecture |
| [ADR-0009](architecture/adr/0009-technology-stack.md) | Technology Stack Decisions (frozen for Phase 1) |
| [ADR-0010](architecture/adr/0010-multi-agent-architecture-rationale.md) | Multi-Agent Architecture Rationale |

See the [ADR Index](architecture/adr/README.md) for summaries and full records.

---

## Status

This is **Phase 0 — documentation and planning only.** No production code or business logic
has been written. **Phase 1 (implementation) has not begun and awaits explicit approval.**

**Sources**

[^ihl]: IHL Group inventory distortion research (RetailTouchPoints / ChainStoreAge). Content rephrased for compliance. See [Market Research](research/04-market-research.md) for full citations.
[^nrf]: National Retail Federation, National Retail Security Survey 2023. Content rephrased for compliance.
[^lucent]: Lucent Innovation (citing industry research on inventory cost). Content rephrased for compliance.
