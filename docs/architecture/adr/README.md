# Architecture Decision Records (ADRs)

> **Purpose.** Record the significant decisions made during Phase 0, each with its context,
> the decision, the rationale, and the trade-offs and alternatives considered. ADRs make the
> *why* behind StockSense durable and reviewable.

An ADR captures a decision at a point in time. Decisions can be **superseded** later by a
new ADR, but existing ADRs are not rewritten — the history is the value.

---

## Index

| ADR | Title | Status | Summary |
| --- | --- | --- | --- |
| [0001](0001-decision-intelligence-not-dashboards.md) | Decision Intelligence, not dashboards | Accepted | The product is a decision engine; charts are only evidence |
| [0002](0002-scope-boundaries-not-an-erp.md) | Scope boundaries — not an ERP/POS/IMS/CRM | Accepted | Disciplined scope to avoid feature creep |
| [0003](0003-human-in-the-loop-decisioning.md) | Human-in-the-loop decisioning | Accepted | System recommends; humans decide; no default autonomy |
| [0004](0004-explainable-ai-mandate.md) | Explainable-AI mandate (4 mandatory elements) | Accepted | Every recommendation carries reasoning, confidence, evidence, impact |
| [0005](0005-multi-agent-orchestration.md) | Multi-agent architecture with orchestration | Accepted | 11-agent design with an Orchestrator and added guardian agents |
| [0006](0006-layer-over-systems-of-record.md) | Layer over existing systems of record | Accepted | Integrate, don't replace; source-agnostic core |
| [0007](0007-ai-governance-framework.md) | AI Governance Framework | Accepted | Platform-wide controls: grounding, confidence, fallback, override, audit, versioning, traceability, fairness, privacy |

---

## ADR Template

New ADRs should follow this structure:

```
# ADR-NNNN — <Title>

- Status: Proposed | Accepted | Superseded by ADR-XXXX
- Date: <phase / date>
- Deciders: <roles>

## Context
What forces are at play? What problem or tension prompted a decision?

## Decision
The decision, stated plainly.

## Rationale
Why this decision, given the context and principles.

## Trade-offs
What we give up; risks we accept.

## Alternatives Considered
Options evaluated and why they were not chosen.

## Consequences
What becomes easier or harder as a result.
```

---

## Relationship to Product Principles

Every ADR here is downstream of the [Product Principles](../../product/10-product-principles.md)
and [AI Philosophy](../../product/12-ai-philosophy.md). Where a principle needed a concrete,
defensible architectural commitment, that commitment is recorded as an ADR.
