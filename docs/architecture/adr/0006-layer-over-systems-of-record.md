# ADR-0006 — Layer over existing systems of record

- **Status:** Accepted
- **Date:** Phase 0
- **Deciders:** Product, Architecture

## Context

Our target retailers already run a POS/IMS (Zoho, Shopify, Odoo, spreadsheets, etc.). AI
adoption in this segment is blocked chiefly by **cost, expertise, and integration
difficulty** ([Market Research](../../research/04-market-research.md)). Requiring them to
replace their system of record would be off-mission ([ADR-0002](0002-scope-boundaries-not-an-erp.md))
and would raise adoption friction to a level this segment will not tolerate.

## Decision

StockSense operates as a **decision layer on top of the retailer's existing systems of
record.** The **Integration Agent** isolates external systems behind a read-oriented
boundary and maps their data into a normalized, **source-agnostic** internal model. The
core engine never assumes a particular source system.

## Rationale

- Directly removes the **integration barrier** that studies identify as a top adoption
  blocker.
- Keeps scope disciplined — we add a layer, we do not become a system of record.
- Makes the product portable across the fragmented SMB tooling landscape.

## Trade-offs

- We depend on the data quality and availability of systems we do not control (mitigated by
  the [Data Quality Agent](../../agents/agent-catalog.md)).
- Each new source system requires connector work.
- We cannot guarantee data we did not originate; hence quality scoring is mandatory.

## Alternatives Considered

1. **Be the system of record too.** Rejected: violates scope, raises friction, crowded
   market.
2. **Single-platform integration only (e.g., Shopify-only).** Rejected: unduly narrows the
   addressable market and creates ecosystem lock-in.

## Consequences

- The Integration + Data Quality agents form the ingestion layer
  ([Agent Architecture](../13-agent-architecture.md)).
- Deployment/tenancy model (multi-tenant SaaS vs. isolated) is an open Phase 1 decision.
- Roadmap sequences connectors: CSV + one POS/IMS in V1, more later
  ([Roadmap](../../planning/14-product-roadmap.md)).
