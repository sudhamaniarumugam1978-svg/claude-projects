# Agent Catalog

> **Purpose.** The definitive per-agent specification for the StockSense Decision
> Intelligence Engine. Each entry defines the agent's responsibility, inputs, outputs,
> guarantees (contracts), failure behavior, and the product principle it upholds.
>
> This is a **design specification**, not implementation. It complements the system-level
> [Agent Architecture](../architecture/13-agent-architecture.md).

## Reading this catalog

Each agent is specified with a consistent template:

- **Mission** — the single responsibility.
- **Inputs / Outputs** — the message contracts it consumes and produces.
- **Guarantees** — the invariants it must always hold.
- **Failure & degradation** — what it does when it cannot fulfill its mission.
- **Upholds** — the product principle / AI-philosophy rule it enforces.

All outputs use the shared message envelope (`trace_id`, `evidence_refs`, `confidence`,
`data_quality_score`) defined in the [Agent Architecture §5.2](../architecture/13-agent-architecture.md#52-canonical-message-envelope-conceptual).

---

## 1. Integration Agent

- **Mission:** Connect to the retailer's existing systems of record and ingest their data
  without requiring them to replace anything.
- **Inputs:** External connections — POS/IMS APIs, CSV/spreadsheet exports, supplier data
  (lead times, MOQ, cost, reliability).
- **Outputs:** Raw, source-tagged records mapped toward the internal schema.
- **Guarantees:**
  - Read-oriented by default; least-privilege access to external systems.
  - Source and timestamp provenance on every record.
  - New connectors are additive and do not break downstream contracts.
- **Failure & degradation:** On connection failure, report clearly and continue with last
  known good data (flagged as stale); never silently drop data.
- **Upholds:** "Layered, not rip-and-replace" ([Scope](../product/06-product-scope.md)).

---

## 2. Data Quality Agent *(added in critical review)*

- **Mission:** Ensure downstream decisions rest on trustworthy data.
- **Inputs:** Raw records from the Integration Agent.
- **Outputs:** Validated, de-duplicated, reconciled records **plus a `data_quality_score`**.
- **Guarantees:**
  - Detect missing, duplicate, stale, or contradictory records.
  - Surface discrepancies (e.g., shrink/adjustment signals) rather than absorbing them.
  - Attach a trustworthiness score that travels with the data.
- **Failure & degradation:** If quality is poor, lower the score and propagate it; do not
  clean-and-hide. Poor quality must be *visible* downstream.
- **Upholds:** "Never recommend without evidence"; graceful degradation
  ([AI Philosophy](../product/12-ai-philosophy.md)).

---

## 3. Inventory Intelligence Agent

- **Mission:** Maintain a single, normalized, source-agnostic model of current inventory
  truth.
- **Inputs:** Validated records (with quality scores) from the Data Quality Agent.
- **Outputs:** The normalized inventory state model — catalog, on-hand levels, categories,
  perishability/expiry attributes, supplier attributes, and derived fields (e.g., days of
  cover).
- **Guarantees:**
  - One consistent representation regardless of source system.
  - Current, reconciled state with clear "as of" timestamps.
- **Failure & degradation:** Expose known gaps in the model rather than interpolating
  silently.
- **Upholds:** Traceability; foundation for all analysis.

---

## 4. Forecast Agent

- **Mission:** Predict future demand per SKU — the core of "what will happen."
- **Inputs:** Inventory state model + sales history (with quality scores).
- **Outputs:** Per-SKU demand forecasts over relevant horizons, each with a **calibrated
  confidence interval / score** and the factors driving it (seasonality, trend, events).
- **Guarantees:**
  - Every forecast carries calibrated confidence.
  - Driving factors are recorded as evidence (feeding explanations).
  - Method selection respects data density (simpler, defensible methods for sparse data).
- **Failure & degradation:** With sparse/low-quality data, fall back to simpler baselines
  and *lower confidence honestly*; never project false certainty.
- **Upholds:** "Always show confidence"; "Prediction over reporting"
  ([Principles](../product/10-product-principles.md)).

---

## 5. Risk Detection Agent

- **Mission:** Find inventory problems *before* they occur.
- **Inputs:** Inventory state model, demand forecasts (+confidence), supplier lead times.
- **Outputs:** Risk findings, each typed and evidence-backed:
  - **Stockout risk** (predicted run-out vs. next replenishment).
  - **Overstock / dead-stock risk** (slow movers, excess vs. optimal).
  - **Demand anomaly** (spike/drop/emerging trend).
  - **Expiry / obsolescence risk** (perishables, aging high-value stock).
- **Guarantees:**
  - Each finding references the forecast and data behind it (`evidence_refs`).
  - Findings carry a severity/likelihood consistent with underlying confidence.
- **Failure & degradation:** Where confidence is low, mark findings as tentative rather
  than suppressing or over-asserting them.
- **Upholds:** Proactivity; "Never recommend without evidence."

---

## 6. Analytics Agent

- **Mission:** Compute the metrics and diagnostics that answer "why" and quantify "how
  much."
- **Inputs:** Inventory state model, forecasts, risk findings.
- **Outputs:**
  - Inventory KPIs (turnover, days on hand, dead-stock ratio, etc. — see
    [Success Metrics](../business/11-success-metrics.md)).
  - **Business-impact quantification** per finding (revenue at risk, capital trapped,
    spoilage value) — the basis for ranking.
- **Guarantees:** Impact estimates are explainable and tied to concrete inputs.
- **Failure & degradation:** Report ranges/uncertainty on impact when inputs are noisy.
- **Upholds:** "Prioritize business impact."
- **Boundary vs. Executive Agent:** Analytics computes metrics/diagnostics (data-level);
  the Executive Agent *synthesizes* them into role-appropriate narratives (top-level).

---

## 7. Recommendation Agent — *the contract enforcement point*

- **Mission:** Convert findings into specific, ranked, executable actions — and refuse to
  emit anything that is not fully explained.
- **Inputs:** Risk findings (+evidence), forecasts (+confidence), impact estimates.
- **Outputs:** Ranked recommendations. **Every recommendation MUST contain all four:**
  1. **Reasoning** (plain-language "why"),
  2. **Confidence** (calibrated),
  3. **Supporting data** (`evidence_refs`),
  4. **Business impact** (used for ranking).
  Action types include: reorder (quantity + timing), expedite, markdown (candidate +
  suggested discount), redistribute, and de-list/dead-stock actions.
- **Guarantees:**
  - **Hard rejection** of any candidate output missing a mandatory element.
  - Ranking strictly by business impact.
  - Actions are executable by a non-expert.
- **Failure & degradation:** If a mandatory element cannot be produced, withhold the
  recommendation (or downgrade to an informational, clearly-labeled note) rather than
  emitting a partial one.
- **Upholds:** The entire [AI Philosophy](../product/12-ai-philosophy.md) contract;
  "Always explain," "Never unexplained outputs."

---

## 8. Executive Agent

- **Mission:** Give owners and operations managers a role-appropriate, cross-store view of
  "so what."
- **Inputs:** Recommendations, risk findings, analytics/KPIs.
- **Outputs:** Concise executive summaries — top risks, top opportunities, expected impact,
  and where to drill down — rolled up across locations.
- **Guarantees:**
  - Summaries are synthesized, not raw data dumps.
  - Drill-down path preserved (summary → store → SKU).
- **Failure & degradation:** Clearly note coverage gaps (e.g., a store with stale data).
- **Upholds:** Persona needs (Owner/Ops want summaries — see
  [Personas](../product/08-user-personas.md)); "Insight over charts."

---

## 9. Notification Agent

- **Mission:** Deliver the right output to the right person at the right time — and nothing
  more.
- **Inputs:** Recommendations and executive summaries.
- **Outputs:** Targeted notifications through appropriate channels, prioritized by impact
  and urgency.
- **Guarantees:**
  - **Signal-over-noise suppression:** low-impact/low-confidence items are not pushed.
  - Routing respects role (manager vs. owner) and urgency.
- **Failure & degradation:** When uncertain about urgency, prefer the digest over the
  interrupt; an unopened alert is a failure.
- **Upholds:** "Signal over noise"; "Never overwhelm."

---

## 10. Learning / Feedback Agent *(added in critical review)*

- **Mission:** Close the loop so the system improves from human decisions and outcomes.
- **Inputs:** Human decisions (approve/modify/reject) and realized outcomes over time.
- **Outputs:** Feedback signals to the Forecast and Recommendation agents; calibration
  monitoring for confidence scores.
- **Guarantees:**
  - Overrides are treated as signal, never ignored.
  - Confidence calibration is continuously monitored (does 80% mean 80%?).
  - The human is never overruled — feedback *tunes* the system, it does not override
    people.
- **Failure & degradation:** With insufficient feedback data, make no unjustified model
  changes; report calibration uncertainty.
- **Upholds:** Feedback loop in [Business Workflow](../business/09-business-workflow.md);
  calibrated confidence.

---

## 11. Orchestrator *(added in critical review)*

- **Mission:** Conduct the pipeline and own end-to-end traceability.
- **Inputs:** System triggers/schedules; agent status.
- **Outputs:** Sequenced (and where safe, parallelized) agent execution; a consolidated
  decision-level trace.
- **Guarantees:**
  - Enforces message contracts between agents.
  - Assigns and propagates `trace_id` so any recommendation can be followed back to raw
    data.
  - Parallelizes independent analysis (Forecast / Risk / Analytics consume the same
    Foundation model).
- **Failure & degradation:** On a failed agent, halt the affected decision chain and report
  it with the trace; never emit a downstream output built on a failed upstream step.
- **Upholds:** "Traceable, no black boxes"; reliability.

---

## Contract Enforcement Summary

The single most important architectural guarantee is that **the Recommendation Agent (and
Executive Agent) cannot emit an output missing reasoning, confidence, supporting data, or
business impact.** Because these fields are populated progressively as messages flow
through the pipeline (Data Quality → Forecast → Risk → Analytics), enforcement at the
decision boundary is a *validation*, not a hopeful convention. This is what operationalizes
the promise: **StockSense never produces an unexplained AI output.**

---

## Agent → Principle Traceability

| Agent | Primary principle enforced |
| --- | --- |
| Integration | Layer, don't replace |
| Data Quality | Never recommend without evidence |
| Inventory Intelligence | Traceability / single source of truth |
| Forecast | Prediction over reporting; calibrated confidence |
| Risk Detection | Proactivity |
| Analytics | Prioritize business impact |
| Recommendation | Always explain; never unexplained outputs (enforcement point) |
| Executive | Insight over charts; layered detail |
| Notification | Signal over noise |
| Learning/Feedback | Learn from feedback; confidence calibration |
| Orchestrator | Traceable, no black boxes; reliability |
