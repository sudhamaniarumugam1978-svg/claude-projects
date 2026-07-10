# 09 — Business Workflow

> **Purpose.** Describe the end-to-end business workflow StockSense participates in, from
> supplier to manager action, and make explicit where StockSense adds value: the loop from
> *data* to *decision* to *approved action*, with the human always in control.

---

## The Canonical Flow

```
        Supplier
           │
           ▼
       Inventory
           │
           ▼
         Sales
           │
           ▼
    Inventory Updates
           │
           ▼
      AI Analysis          ◄── StockSense begins here
           │
           ▼
    Recommendations
           │
           ▼
    Manager Actions
           │
           └──────────────► (feedback loops back into AI Analysis)
```

StockSense does **not** replace the supplier, inventory, or sales systems. It observes
their outputs (data), reasons over them (analysis), and returns decisions
(recommendations) for a human to act on (actions). The action then feeds back as new data.

---

## End-to-End Workflow (Detailed)

### Stage 1 — Supplier
- **What happens:** Goods are sourced from suppliers with specific lead times, minimum
  order quantities, costs, and reliability.
- **Data StockSense needs:** Supplier lead times, order constraints, cost, and (where
  available) reliability/variance.
- **StockSense role:** None yet — but supplier attributes (especially lead time and its
  variance) are critical inputs to later risk detection and reorder recommendations.

### Stage 2 — Inventory
- **What happens:** Received goods become on-hand stock at known quantities and locations.
- **Data StockSense needs:** Current stock levels, product catalog, categories,
  perishability/expiry, and cost.
- **StockSense role:** Establish the baseline state of inventory as the ground truth for
  analysis (via the Integration and Inventory Intelligence layers).

### Stage 3 — Sales
- **What happens:** Customers buy items; demand is expressed and revenue is realized.
- **Data StockSense needs:** Transaction-level or aggregated sales history over time,
  including timestamps for seasonality/day-of-week patterns.
- **StockSense role:** Sales history is the primary signal for demand forecasting and
  anomaly detection.

### Stage 4 — Inventory Updates
- **What happens:** Stock levels change from sales, receipts, returns, adjustments, and
  shrink.
- **Data StockSense needs:** Continuous stock movements and adjustments.
- **StockSense role:** Keep its internal model synchronized and detect data-quality issues
  (e.g., shrink/discrepancies that corrupt decisions).

### Stage 5 — AI Analysis *(StockSense core begins)*
- **What happens:** StockSense continuously analyzes the synchronized data.
- **Activities:**
  - **Forecast** demand per SKU with confidence intervals.
  - **Detect risk:** predicted stockouts, overstock/dead stock, anomalies, expiry/obsolescence.
  - **Quantify impact:** estimate revenue at risk / capital trapped for each finding.
- **Output:** A set of evidence-backed findings, each with reasoning, confidence, and
  impact.

### Stage 6 — Recommendations
- **What happens:** Findings are converted into specific, ranked, explained actions.
- **Each recommendation carries (mandatory):** reasoning, confidence score, supporting
  data, and expected business impact — per [AI Philosophy](../product/12-ai-philosophy.md).
- **Examples:** reorder quantity + timing; markdown candidate + suggested discount; dead
  stock to de-list; redistribution suggestion; expedite recommendation.
- **Ranking:** by business impact (dollars at stake), so the manager sees the vital few
  first.

### Stage 7 — Manager Actions
- **What happens:** The human decision-maker reviews and acts.
- **Options:** **Approve**, **Modify**, or **Reject** each recommendation.
- **Execution:** The manager (not StockSense, by default) executes the action in their
  system of record / with their supplier. Automated execution is opt-in only.
- **Capture:** The decision (and later, the outcome) is recorded.

### Feedback Loop — Learning
- Manager decisions and realized outcomes feed back into AI Analysis.
- Overrides are treated as signal: they refine future forecasts and recommendations.
- This closes the loop: **data → analysis → recommendation → action → outcome → better
  analysis.**

---

## Actors and Responsibilities

| Actor | Responsibility in the workflow |
| --- | --- |
| **Supplier** | Provides goods, lead times, constraints (external) |
| **System of record (POS/IMS)** | Records inventory, sales, and updates (external) |
| **StockSense — Integration** | Ingests and normalizes data from systems of record |
| **StockSense — Analysis agents** | Forecast, detect risk, quantify impact |
| **StockSense — Recommendation** | Produce ranked, explained, confidence-scored actions |
| **Store / Inventory Manager** | Approve / modify / reject and execute actions |
| **Operations Manager / Owner** | Consume executive summaries; set policy and thresholds |

Mapped to the multi-agent design in [Agent Architecture](../architecture/13-agent-architecture.md).

---

## Where StockSense Creates Value in the Flow

1. **Between Sales/Updates and Action**, incumbents leave a gap: data exists, but the
   decision is left to an overloaded human. StockSense fills that gap.
2. It converts a **reactive** flow (act after the problem) into a **proactive** one (act
   before the problem), consistent with [Product Vision](../product/01-product-vision.md).
3. It **compresses** the find-analyze-decide cycle from hours/days of manual work into a
   ranked morning brief.

---

## Decision Sequence Diagram (Approve/Modify/Reject)

```
Data (POS/IMS) ─► Integration ─► Analysis (forecast + risk + impact)
                                      │
                                      ▼
                             Recommendation (reason, confidence, evidence, impact)
                                      │
                                      ▼
                            ┌── Manager reviews ──┐
                            │        │            │
                         Approve   Modify       Reject
                            │        │            │
                            ▼        ▼            ▼
                        Execute   Execute      No action
                       (as-is)  (adjusted)         │
                            │        │             │
                            └────────┴─────────────┘
                                      ▼
                             Outcome captured ─► feeds back to Analysis
```

The human is the terminal decision-maker at every branch — never bypassed by default.
