# 15 — Repository Planning

> **Purpose.** Define how documentation (Phase 0) and future code (Phase 1+) are organized,
> so the repository remains navigable, logically structured, and consistent with the
> repository standards established by the Master Prompt.

---

## 1. Current Documentation Structure (Phase 0)

All Phase 0 deliverables live under `/docs`, organized by concern. Every document is
numbered where it maps to a numbered deliverable, and cross-linked from the
[Documentation Index](../README.md).

```
docs/
├── README.md                         # Documentation index / navigation hub
├── executive-summary.md              # 17 — Executive summary
│
├── product/                          # Product definition
│   ├── 01-product-vision.md
│   ├── 02-mission-statement.md
│   ├── 03-value-proposition.md
│   ├── 06-product-scope.md
│   ├── 07-target-customers.md
│   ├── 08-user-personas.md
│   ├── 10-product-principles.md
│   └── 12-ai-philosophy.md
│
├── research/                         # Evidence base (cited)
│   ├── 04-market-research.md
│   └── 05-competitor-analysis.md
│
├── business/                         # Business design
│   ├── 09-business-workflow.md
│   ├── 11-success-metrics.md
│   ├── data-quality-policy.md
│   └── risk-register.md
│
├── architecture/                     # System design
│   ├── 13-agent-architecture.md
│   └── adr/                          # 16 — Architecture Decision Records
│       ├── README.md                 # ADR index + template
│       ├── 0001-decision-intelligence-not-dashboards.md
│       ├── 0002-scope-boundaries-not-an-erp.md
│       ├── 0003-human-in-the-loop-decisioning.md
│       ├── 0004-explainable-ai-mandate.md
│       ├── 0005-multi-agent-orchestration.md
│       ├── 0006-layer-over-systems-of-record.md
│       ├── 0007-ai-governance-framework.md
│       └── 0008-security-architecture.md
│
├── agents/                           # Agent specifications
│   └── agent-catalog.md
│
└── planning/                         # Delivery planning
    ├── 14-product-roadmap.md
    └── 15-repository-planning.md      # (this document)
```

### Rationale for this organization
- **By concern, not by author or date** — a reviewer can find "everything about the market"
  or "everything about architecture" in one place.
- **Numbered to match deliverables** — traceability from the Phase 0 brief to the artifact.
- **ADRs nested under architecture** — decisions live next to the design they justify.
- **Single index (`docs/README.md`)** — one navigation hub with role-based reading paths.

---

## 2. Documentation Conventions

| Convention | Rule |
| --- | --- |
| Format | Markdown (`.md`), one deliverable per file |
| Naming | `NN-kebab-case-title.md` where a deliverable number exists; kebab-case otherwise |
| Cross-references | Relative links between docs; the index links to all |
| Citations | Inline footnote-style references with source URLs in research docs |
| Diagrams | Mermaid (rendered on GitHub) with ASCII fallbacks where useful |
| Tone | Company-grade documentation; no tutorial voice, no placeholders |
| Source of truth | `docs/README.md` is the canonical index |

---

## 3. Planned Code Structure (Phase 1+ — NOT YET CREATED)

This is a **forward-looking plan only.** No code exists in Phase 0. It is recorded here so
the repository can grow coherently once Phase 1 is approved. The structure mirrors the
[Agent Architecture](../architecture/13-agent-architecture.md) layering.

```
(proposed, Phase 1+)
/
├── docs/                     # (exists) all documentation
├── services/ or src/        # engine implementation, organized by agent/layer
│   ├── integration/         # Integration Agent
│   ├── data-quality/        # Data Quality Agent
│   ├── inventory/           # Inventory Intelligence Agent
│   ├── forecast/            # Forecast Agent
│   ├── risk/                # Risk Detection Agent
│   ├── analytics/           # Analytics Agent
│   ├── recommendation/      # Recommendation Agent (contract enforcement)
│   ├── executive/           # Executive Agent
│   ├── notification/        # Notification Agent
│   ├── learning/            # Learning / Feedback Agent
│   └── orchestrator/        # Orchestrator
├── contracts/               # Shared message schemas / envelopes
├── tests/                   # Test suites (added per Phase 1 plan)
└── deploy/                  # Deployment/infra definitions
```

**Note:** Directory shapes (monorepo vs. services, language, frameworks) are intentionally
**undecided** in Phase 0 and will be settled via ADRs at the start of Phase 1. The only
commitment here is that **code organization will follow the agent/layer boundaries** so the
architecture and the codebase stay aligned.

---

## 4. Repository Hygiene Standards

- **Every significant decision → an ADR** ([ADR index](../architecture/adr/README.md)).
- **Docs stay in sync with design** — architectural changes update both the doc and any
  affected ADR.
- **The index is authoritative** — new documents are added to `docs/README.md`.
- **Phase gating** — implementation does not begin until the relevant phase is approved;
  Phase 0 is documentation-only.

---

## 5. Traceability Matrix (Deliverable → File)

| # | Deliverable | File |
| --- | --- | --- |
| 01 | Product Vision | `docs/product/01-product-vision.md` |
| 02 | Mission Statement | `docs/product/02-mission-statement.md` |
| 03 | Value Proposition | `docs/product/03-value-proposition.md` |
| 04 | Market Research | `docs/research/04-market-research.md` |
| 05 | Competitor Analysis | `docs/research/05-competitor-analysis.md` |
| 06 | Product Scope | `docs/product/06-product-scope.md` |
| 07 | Target Customers | `docs/product/07-target-customers.md` |
| 08 | User Personas | `docs/product/08-user-personas.md` |
| 09 | Business Workflow | `docs/business/09-business-workflow.md` |
| 10 | Product Principles | `docs/product/10-product-principles.md` |
| 11 | Success Metrics | `docs/business/11-success-metrics.md` |
| 12 | AI Philosophy | `docs/product/12-ai-philosophy.md` |
| 13 | Agent Architecture | `docs/architecture/13-agent-architecture.md` (+ `docs/agents/agent-catalog.md`) |
| 14 | Product Roadmap | `docs/planning/14-product-roadmap.md` |
| 15 | Repository Planning | `docs/planning/15-repository-planning.md` |
| 16 | Architecture Decision Records | `docs/architecture/adr/*` |
| 17 | Executive Summary | `docs/executive-summary.md` |

Every Phase 0 deliverable maps to exactly one primary file, satisfying the requirement that
all documents are logically organized.
