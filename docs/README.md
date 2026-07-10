# StockSense — Documentation Index

> **Tagline:** Helping retailers make smarter inventory decisions before problems happen.
>
> **Category:** AI-Powered Retail Inventory Intelligence Platform
>
> **Phase:** 0 — Product Discovery, Architecture & Planning (documentation only)

StockSense is an **AI Decision Intelligence Platform** for retailers. It does not merely
report *what happened*; it tells retailers **what will happen, why it will happen, and
what action to take** — with evidence, confidence, and business impact attached to every
recommendation.

This directory is the complete **Phase 0 product blueprint**. It contains no production
code and no business logic. It is the source of truth for the product's vision, market
rationale, scope, principles, agent architecture, and roadmap.

---

## What StockSense Is (and Is Not)

| StockSense **IS** | StockSense **IS NOT** |
| --- | --- |
| A Decision Intelligence Engine | An ERP |
| A proactive risk-detection and forecasting system | A POS system |
| An explanation-first recommendation layer | An Inventory Management System (IMS) |
| A system that augments human decisions | A CRM |
| An insight product (not a chart product) | A dashboard project |
| — | A generic AI chatbot |

**The Decision Intelligence Engine is the product. The AI Assistant is not the product.**

---

## Documentation Map

### `/docs/product` — Product Definition
| # | Document | Description |
| --- | --- | --- |
| 01 | [Product Vision](product/01-product-vision.md) | Why StockSense exists and the problem it solves |
| 02 | [Mission Statement](product/02-mission-statement.md) | The single guiding mission |
| 03 | [Value Proposition](product/03-value-proposition.md) | Differentiation vs. IMS, ERP, dashboards, chatbots, AI assistants |
| 06 | [Product Scope](product/06-product-scope.md) | What we will and will not build |
| 07 | [Target Customers](product/07-target-customers.md) | Primary segments and future markets |
| 08 | [User Personas](product/08-user-personas.md) | Owner, Store Manager, Inventory Manager, Operations Manager |
| 10 | [Product Principles](product/10-product-principles.md) | The product philosophy and non-negotiables |
| 12 | [AI Philosophy](product/12-ai-philosophy.md) | How AI augments — never replaces — human decisions |

### `/docs/research` — Evidence Base
| # | Document | Description |
| --- | --- | --- |
| 04 | [Market Research](research/04-market-research.md) | Retail inventory problems, techniques, pain points, AI adoption (cited) |
| 05 | [Competitor Analysis](research/05-competitor-analysis.md) | Zoho, Shopify, SAP, Oracle, Dynamics, Odoo — gaps and opportunities |

### `/docs/business` — Business Design
| # | Document | Description |
| --- | --- | --- |
| 09 | [Business Workflow](business/09-business-workflow.md) | Supplier → Inventory → Sales → AI → Recommendation → Action |
| 11 | [Success Metrics & Metrics Framework](business/11-success-metrics.md) | Full framework: Business, AI, Engineering, Operational, and Adoption KPIs (definition, formula, source, target, frequency, owner, visualization) |
| — | [Data Quality Policy](business/data-quality-policy.md) | Validation pipeline, quality scoring, escalation, and the Data Quality Agent's contract |
| — | [Risk Register](business/risk-register.md) | Material risks with probability, impact, detection, mitigation, owner, and status |

### `/docs/architecture` — System Design
| # | Document | Description |
| --- | --- | --- |
| 13 | [Agent Architecture](architecture/13-agent-architecture.md) | Enterprise multi-agent design, responsibilities, communication, diagrams |
| — | [ADR Index](architecture/adr/README.md) | Architecture Decision Records for Phase 0 |

### `/docs/agents` — Agent Specifications
| Document | Description |
| --- | --- |
| [Agent Catalog](agents/agent-catalog.md) | Per-agent responsibilities, inputs, outputs, and contracts |

### `/docs/planning` — Delivery Planning
| # | Document | Description |
| --- | --- | --- |
| 14 | [Product Roadmap](planning/14-product-roadmap.md) | V1 (MVP), V2, V3 and long-term vision |
| 15 | [Repository Planning](planning/15-repository-planning.md) | Documentation and future code organization |

### Top-Level
| # | Document | Description |
| --- | --- | --- |
| 17 | [Executive Summary](executive-summary.md) | One-read overview for reviewers, contributors, and investors |

---

## Reading Paths

- **Recruiters / reviewers / investors:** start with the [Executive Summary](executive-summary.md), then [Product Vision](product/01-product-vision.md) and [Value Proposition](product/03-value-proposition.md).
- **Engineers / contributors:** read [Product Principles](product/10-product-principles.md), [Agent Architecture](architecture/13-agent-architecture.md), the [Agent Catalog](agents/agent-catalog.md), and the [ADRs](architecture/adr/README.md).
- **Product / business stakeholders:** read [Market Research](research/04-market-research.md), [Competitor Analysis](research/05-competitor-analysis.md), and the [Product Roadmap](planning/14-product-roadmap.md).

---

## Document Status

All documents in this index are **Phase 0 deliverables**. Phase 0 is complete when this
blueprint is committed and pushed. **Phase 1 (implementation) has not started and awaits
explicit approval.**

_Last updated: Phase 0 authoring. Sources are cited inline within each research document._
