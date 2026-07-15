# ADR-0002 — Scope boundaries: not an ERP/POS/IMS/CRM

- **Status:** Accepted
- **Date:** Phase 0
- **Deciders:** Product, Architecture

## Context

Products that touch inventory face constant gravitational pull toward becoming an ERP,
POS, inventory-management system, or CRM — because adjacent features always look
attractive. This pull is the primary cause of feature creep and diluted positioning. The
brief is explicit that StockSense is *none* of these.

## Decision

StockSense is scoped **exclusively** as a decision intelligence layer for inventory. It
will **not** become an ERP, POS, system-of-record IMS, CRM, or "dashboard project," and it
will **not** execute purchase orders directly by default. Every candidate feature must pass
**the Decision Test**: *does it help a retailer make a better inventory decision, before a
problem occurs, with an explanation they can trust?*

## Rationale

- Focus is the product's strategic advantage against broad, expensive incumbents
  ([Competitor Analysis](../../research/05-competitor-analysis.md)).
- These adjacent categories are crowded, capital-intensive, and a different job
  ([Value Proposition](../../product/03-value-proposition.md)).
- Layering over existing systems (see [ADR-0006](0006-layer-over-systems-of-record.md))
  makes replacing them both unnecessary and off-mission.

## Trade-offs

- We forgo revenue from adjacent modules and the "one vendor for everything" pitch.
- We depend on integrating with systems of record we do not own.
- We must repeatedly say "no" to reasonable-sounding requests.

## Alternatives Considered

1. **Bundle a lightweight IMS.** Rejected: turns us into a system of record, raises
   adoption friction, and dilutes focus.
2. **Add auto-execution of orders by default.** Rejected: violates human-in-the-loop
   ([ADR-0003](0003-human-in-the-loop-decisioning.md)); only ever an opt-in V3 capability.

## Consequences

- The [Product Scope](../../product/06-product-scope.md) "will not" list is enforceable and
  cited here.
- Scope guardrails become a standing review criterion for the roadmap.
