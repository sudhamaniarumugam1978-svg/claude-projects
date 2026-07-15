# ADR-0001 — Decision Intelligence, not dashboards

- **Status:** Accepted
- **Date:** Phase 0
- **Deciders:** Product, Architecture

## Context

Most retail inventory tooling terminates in *reporting*: dashboards and charts that
visualize the past and leave analysis, interpretation, and the decision to the user. Our
[Market Research](../../research/04-market-research.md) and
[Competitor Analysis](../../research/05-competitor-analysis.md) show this "chart vs.
conclusion" gap is pervasive — incumbents visualize, few conclude. The founding product
philosophy is that *insights are more valuable than raw charts* and that the system should
*never overwhelm users with unnecessary dashboards*.

## Decision

StockSense is a **Decision Intelligence Engine**. Its primary deliverable is a **ranked,
explained, confidence-scored recommendation** — a decision — not a visualization. Charts
and metrics exist **only as supporting evidence** for a decision, never as the product
itself.

## Rationale

- The measured value in retail inventory is in *acting earlier and better*, not in *seeing
  more data* (see McKinsey forecasting impact in [Market Research](../../research/04-market-research.md)).
- Our target users are time-poor and non-expert ([Personas](../../product/08-user-personas.md));
  they need conclusions, not analysis homework.
- It is the core differentiator against every competitor category
  ([Value Proposition](../../product/03-value-proposition.md)).

## Trade-offs

- We give up the "land grab" of being a flexible BI/dashboard tool with broad appeal.
- We take on the harder engineering and UX challenge of producing trustworthy conclusions,
  not just visualizations.
- We must resist persistent pressure to "just add a dashboard."

## Alternatives Considered

1. **Dashboard-first with optional recommendations.** Rejected: it re-centers the product
   on charts and dilutes the differentiator; it also contradicts "never overwhelm."
2. **Pure alerting (thresholds only).** Rejected: threshold alerts are reactive and
   unexplained — the opposite of decision intelligence.

## Consequences

- Every screen and output is measured by "does this help the user *decide*?"
- The [Agent Architecture](../13-agent-architecture.md) centers on the Recommendation and
  Executive agents as the value-delivering endpoints.
- Charts become a feature *of* an explanation, governed by [Scope](../../product/06-product-scope.md).
