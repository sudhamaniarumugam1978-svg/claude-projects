# ADR-0003 — Human-in-the-loop decisioning

- **Status:** Accepted
- **Date:** Phase 0
- **Deciders:** Product, Architecture, AI

## Context

Automation can be tempting: fully autonomous reordering promises convenience. But the
retailer owns the business and the risk, our target users are skeptical of black boxes, and
a wrong autonomous action costs real money and trust. The founding
[AI Philosophy](../../product/12-ai-philosophy.md) states that AI must augment — never
replace — the final business decision.

## Decision

StockSense **recommends; the human decides.** Every material recommendation is a proposal
the user can **approve, modify, or reject**. There is **no default autonomous execution**.
Any assisted execution is strictly **opt-in**, human-configured, reversible, limited to
low-risk/high-confidence actions, and deferred to V3
([Roadmap](../../planning/14-product-roadmap.md)).

## Rationale

- Trust is the adoption gate for our skeptical, non-expert users
  ([Personas](../../product/08-user-personas.md)).
- Keeping the human as the terminal decision-maker bounds the blast radius of any model
  error.
- It differentiates us from "autonomous" pitches that retailers distrust.

## Trade-offs

- We forgo the "hands-off automation" marketing angle in early versions.
- Value depends on users actually engaging with recommendations (mitigated by
  signal-over-noise and ranking-by-impact).

## Alternatives Considered

1. **Autonomous reordering by default.** Rejected: violates the core philosophy and
   concentrates risk.
2. **No execution assistance ever.** Rejected as too rigid; a tightly-scoped, opt-in
   assisted mode is acceptable once trust is proven (V3).

## Consequences

- The [Business Workflow](../../business/09-business-workflow.md) terminates at a human
  decision node.
- The [Learning/Feedback Agent](../../agents/agent-catalog.md) tunes the system from human
  decisions but never overrules people.
