# ADR-0005 — Multi-agent architecture with orchestration

- **Status:** Accepted
- **Date:** Phase 0
- **Deciders:** Architecture

## Context

The engine must ingest data, ensure its quality, forecast, detect risk, quantify impact,
recommend, summarize, notify, and learn — a set of distinct concerns. The brief suggested
eight agents. A critical review ([Agent Architecture §2](../13-agent-architecture.md#2-critical-evaluation-of-the-suggested-agent-set))
found three structural gaps: no data-quality guardian, no coordination/traceability owner,
and no learning loop.

## Decision

Adopt a **multi-agent architecture of 11 agents**: the eight suggested (Integration,
Inventory Intelligence, Forecast, Risk Detection, Recommendation, Analytics, Executive,
Notification) plus three additions — **Data Quality**, **Learning/Feedback**, and an
**Orchestrator**. Agents communicate via **explicit, versioned message contracts** with a
shared envelope carrying `trace_id`, `evidence_refs`, `confidence`, and
`data_quality_score`. The Orchestrator sequences work, parallelizes independent analysis,
enforces contracts, and owns end-to-end traceability.

## Rationale

- **Separation of concerns** enables independent testing, evolution, and observability.
- The **Data Quality** agent protects the "never recommend without evidence" promise
  against shrink/admin-error data corruption ([Market Research](../../research/04-market-research.md)).
- The **Orchestrator** provides the traceability required by "no black boxes."
- The **Learning/Feedback** agent realizes the feedback loop in the
  [Business Workflow](../../business/09-business-workflow.md).

## Trade-offs

- More components than a monolith → more coordination and operational surface.
- Contract-first messaging adds upfront design effort.
- Orchestration introduces a coordination layer that must itself be reliable.

## Alternatives Considered

1. **Monolithic engine.** Rejected: poor separation, weak traceability, hard to evolve.
2. **The suggested 8 agents unchanged.** Rejected: leaves the three structural gaps
   unaddressed.
3. **Choreography without an orchestrator.** Rejected for now: implicit ordering harms
   traceability; the specific runtime coordination style (bus vs. workflow engine) is left
   open for Phase 1.

## Consequences

- Code organization will follow agent/layer boundaries
  ([Repository Planning](../../planning/15-repository-planning.md)).
- The Recommendation Agent becomes the contract-enforcement point for explainability
  ([ADR-0004](0004-explainable-ai-mandate.md)).
- The concrete orchestration runtime remains an open Phase 1 decision.
