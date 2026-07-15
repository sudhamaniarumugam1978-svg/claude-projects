# ADR-0004 — Explainable-AI mandate (four mandatory elements)

- **Status:** Accepted
- **Date:** Phase 0
- **Deciders:** Product, AI, Architecture

## Context

Retailers will not act on advice they cannot understand or trust, and unexplained AI in a
money-affecting decision is a liability. The product principles require that we *always
explain recommendations*, *always show a confidence score*, and *never generate unexplained
AI outputs*. This must be a structural guarantee, not a best-effort convention.

## Decision

Every recommendation (and executive summary) **must** include all four elements, or it is
**not emitted**:

1. **Reasoning** — plain-language "why."
2. **Confidence** — calibrated score.
3. **Supporting data** — traceable evidence (`evidence_refs`).
4. **Business impact** — expected consequence, used for ranking.

This is enforced at the **Recommendation Agent boundary** as a validation, made possible
because the fields are populated progressively along the pipeline (Data Quality → Forecast
→ Risk → Analytics). Explainability is also a **constraint on model choice**: a less-clever
but explainable method is preferred over an unexplainable one.

## Rationale

- Trust is the adoption gate ([Personas](../../product/08-user-personas.md)).
- Explainability is a purchase criterion and a differentiator
  ([Value Proposition](../../product/03-value-proposition.md)).
- Structural enforcement is the only reliable way to keep the promise at scale.

## Trade-offs

- We may sacrifice marginal accuracy for explainability.
- Additional engineering to carry provenance/evidence through every message.
- Some sophisticated techniques are constrained or require explanation layers.

## Alternatives Considered

1. **Best-effort explanations.** Rejected: promises erode without enforcement.
2. **Accuracy-maximizing black-box models.** Rejected: violates "no black boxes" and
   undermines trust.

## Consequences

- The message envelope carries evidence and confidence as first-class fields
  ([Agent Architecture §5.2](../13-agent-architecture.md#52-canonical-message-envelope-conceptual)).
- "Explanation completeness" is a **100% hard requirement** KPI
  ([Success Metrics](../../business/11-success-metrics.md)).
- Confidence calibration is monitored by the Learning/Feedback Agent.
