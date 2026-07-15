# 14 — Product Roadmap

> **Purpose.** Sequence the in-scope capabilities from [Product Scope](../product/06-product-scope.md)
> across three versions, clearly separating the **MVP (V1)** from the **long-term vision
> (V2–V3)**. The roadmap is disciplined by the same rule as scope: every item must help a
> retailer make a better inventory decision, before a problem occurs, with an explanation
> they can trust.

**Guiding sequencing principle:** *Earn trust first, then expand reliance.* We ship the
narrowest thing that proves the core promise (explained, proactive decisions), then widen.

---

## Version Overview

| | V1 — MVP | V2 — Deepen | V3 — Scale & Autonomy (opt-in) |
| --- | --- | --- | --- |
| **Theme** | Prove the core loop | Sharpen intelligence & reach | Network intelligence & assisted execution |
| **Goal** | Explained, proactive recommendations from connected data | Better forecasts, more risk types, richer roles | Multi-location optimization; opt-in assisted actions |
| **Human role** | Approve / modify / reject everything | Same, with more context | Human sets policy; opt-in delegation for low-risk, high-confidence actions |
| **Success gate** | Retailers trust and act on recommendations | Measurable outcome gains (see KPIs) | Proven reliability + calibrated confidence |

---

## V1 — MVP: The Core Decision Loop

**Objective:** Demonstrate the entire value proposition on a narrow footprint — connect
data, detect risk, forecast demand, and deliver ranked, explained, confidence-scored
recommendations that a human approves.

**In scope (V1):**
- **Integration (foundational connectors):** CSV/spreadsheet import and at least one
  common POS/IMS connector; supplier lead-time capture.
- **Data Quality (baseline):** validation, de-duplication, and a visible data-quality
  score.
- **Inventory Intelligence:** normalized current-state model.
- **Forecast (baseline):** per-SKU demand forecasting with confidence, using methods
  appropriate to data density.
- **Risk Detection (core types):** stockout risk and overstock/dead-stock risk.
- **Analytics:** core KPIs + business-impact quantification for ranking.
- **Recommendation:** reorder quantity/timing and dead-stock/markdown candidates — each
  with the four mandatory elements, ranked by impact.
- **Notification (baseline):** a prioritized "morning brief" / digest.
- **Human loop:** approve / modify / reject, with decisions captured.

**Explicitly deferred from V1:** demand-anomaly and expiry/obsolescence risk types,
multi-store roll-ups, advanced ML forecasting, assistant chat interface, and any assisted
execution.

**V1 exit criteria:** Time-to-first-value in minutes; recommendation adoption rate and
user-reported trust meet target thresholds ([Success Metrics](../business/11-success-metrics.md)).

---

## V2 — Deepen: Sharper Intelligence, Broader Roles

**Objective:** Improve decision quality and expand who StockSense serves within a business.

**Added in scope (V2):**
- **Forecast (advanced):** richer ML models where data supports them; seasonality/event
  handling; improved calibration.
- **Risk Detection (expanded):** demand-anomaly detection and expiry/obsolescence risk
  (unlocking pharmacy and perishable value).
- **Executive Agent:** role-appropriate, multi-store executive summaries.
- **Learning / Feedback Agent:** systematic capture of overrides/outcomes feeding back into
  forecasts and recommendations; confidence-calibration monitoring.
- **Notification (smart routing):** role- and urgency-aware routing; refined
  signal-over-noise suppression.
- **Thin assistant interface (optional):** grounded, evidence-backed Q&A as a *window onto
  the engine* — never the product itself ([Scope](../product/06-product-scope.md)).
- **More connectors:** additional POS/IMS integrations.

**V2 exit criteria:** Measurable business-outcome improvements (reduced stockouts/dead
stock, improved turnover) attributable to StockSense.

---

## V3 — Scale & Assisted Autonomy (Opt-In)

**Objective:** Serve multi-location operators and, only where trust is fully earned, offer
opt-in assisted execution for low-risk, high-confidence actions.

**Added in scope (V3):**
- **Network optimization:** cross-store redistribution and network-level inventory
  balancing (serves the multi-location future market from
  [Target Customers](../product/07-target-customers.md)).
- **Opt-in assisted execution:** for narrowly-scoped, low-risk, high-confidence actions
  (e.g., routine reorders within pre-approved policy), always human-configured, always
  reversible, never a default. Bound by [AI Philosophy](../product/12-ai-philosophy.md).
- **Advanced integrations:** deeper supplier connectivity; drafting purchase orders for
  human approval.
- **Vertical/expansion packs:** capabilities tuned for specific segments and future
  markets.
- **Advanced observability & governance:** enterprise-grade audit trails and policy
  controls.

**V3 guardrails:** Assisted execution requires demonstrated calibration and reliability,
and remains strictly opt-in and reversible. StockSense never becomes an autonomous
decision-maker by default.

---

## What Stays Constant Across All Versions

Regardless of version, StockSense **never**:
- becomes an ERP/POS/CRM,
- emits unexplained outputs,
- projects uncalibrated confidence,
- removes the human's final authority by default.

These are permanent, per [Product Principles](../product/10-product-principles.md).

---

## Roadmap at a Glance (Capability × Version)

| Capability | V1 | V2 | V3 |
| --- | :---: | :---: | :---: |
| CSV + first POS/IMS connector | ✓ | ✓ | ✓ |
| Additional connectors | — | ✓ | ✓ |
| Data quality scoring | ✓ | ✓ | ✓ |
| Baseline forecasting (+confidence) | ✓ | ✓ | ✓ |
| Advanced ML forecasting | — | ✓ | ✓ |
| Stockout + overstock risk | ✓ | ✓ | ✓ |
| Anomaly + expiry/obsolescence risk | — | ✓ | ✓ |
| Ranked, explained recommendations | ✓ | ✓ | ✓ |
| Morning brief / digest | ✓ | ✓ | ✓ |
| Executive multi-store summaries | — | ✓ | ✓ |
| Learning/feedback loop | partial* | ✓ | ✓ |
| Thin assistant interface | — | ✓ | ✓ |
| Cross-store network optimization | — | — | ✓ |
| Opt-in assisted execution | — | — | ✓ |

\* V1 captures decisions; V2 operationalizes the feedback into model improvement.

---

## Sequencing Rationale

1. **V1 proves the promise cheaply.** The two highest-value, most-universal risks
   (stockout, dead stock) plus explained recommendations validate the entire thesis before
   heavy investment.
2. **V2 compounds trust into outcomes.** Once retailers act on recommendations, better
   forecasting and the feedback loop convert usage into measurable savings.
3. **V3 expands only where trust is proven.** Multi-store scale and any assisted execution
   come last, gated by demonstrated reliability — consistent with "earn trust
   incrementally, keep it permanently."
