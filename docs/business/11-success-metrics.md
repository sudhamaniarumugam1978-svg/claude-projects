# 11 — Success Metrics

> **Purpose.** Define how we know StockSense is working — for the retailer (business
> outcomes), for the user (engagement and trust), and for the product/AI (quality). Metrics
> are chosen to be **measurable** and tied to the [Product Principles](../product/10-product-principles.md):
> impact, explanation, and trust.

A guiding rule: **we measure problems prevented and decisions improved, not features
shipped or charts viewed.**

---

## 1. Customer Business Outcomes (North-Star Category)

These are the outcomes retailers actually care about. They are the ultimate proof of value.

| KPI | Definition | Target direction | How measured |
| --- | --- | --- | --- |
| **Stockout rate** | % of SKU-days out of stock (esp. high-velocity items) | ↓ Reduce | Compare pre/post StockSense; track availability |
| **Lost-sales value** | Estimated revenue lost to stockouts | ↓ Reduce | Forecasted demand × unavailability |
| **Dead-stock ratio** | % of inventory value not sold within a defined window | ↓ Reduce | Aging analysis on stock value |
| **Overstock / excess inventory value** | Capital tied up above target levels | ↓ Reduce | On-hand vs. optimal stock |
| **Inventory turnover** | COGS ÷ average inventory | ↑ Increase | Standard turnover calculation |
| **Days of inventory on hand (DIO)** | Avg. days stock is held before sale | ↓ Optimize | Standard DIO calculation |
| **Spoilage / expiry write-offs** (perishable/pharma) | Value written off due to expiry | ↓ Reduce | Write-off records |
| **Gross margin impact** | Margin recovered via better decisions | ↑ Increase | Attributed margin from acted recommendations |
| **Working capital freed** | Capital released from reduced overstock | ↑ Increase | Reduction in excess inventory value |

**Benchmark context (why these matter):** inventory distortion and shrink represent
trillions globally and an estimated **3–8% of retailer revenue** — so even single-digit
percentage improvements are materially valuable. See
[Market Research](../research/04-market-research.md).

---

## 2. Efficiency & Time-Savings Outcomes

StockSense's promise includes removing the manual "find the problem" burden.

| KPI | Definition | Target |
| --- | --- | --- |
| **Time saved on manual analysis** | Hours/week no longer spent hunting for problems in reports/spreadsheets | ↓ Reduce |
| **Time-to-decision** | Time from a risk emerging to a decision being made | ↓ Reduce |
| **Manual analysis eliminated** | % of routine analysis now automated | ↑ Increase |
| **Decision throughput** | Number of quality inventory decisions made per manager per week | ↑ Increase |
| **Coverage** | % of SKUs actively monitored for risk | → 100% |

---

## 3. Product Engagement & Adoption

Value is only realized if the product is used and its recommendations are acted on.

| KPI | Definition | Why it matters |
| --- | --- | --- |
| **Recommendation adoption rate** | % of recommendations approved (or approved-with-modification) | Core proxy for usefulness and trust |
| **Time-to-first-value** | Time from connecting data to first actionable recommendation | Measures low-friction promise (target: minutes) |
| **Active usage (DAU/WAU)** | Managers checking the morning brief / acting regularly | Habit formation |
| **Retention / renewal** | Customers continuing to use and pay | Sustained value |
| **Modify vs. reject ratio** | Modified (still useful) vs. rejected (not useful) | Distinguishes "close" from "wrong" |

---

## 4. AI & Recommendation Quality

These metrics enforce the [AI Philosophy](../product/12-ai-philosophy.md): every output
must be accurate *and* trustworthy.

| KPI | Definition | Target |
| --- | --- | --- |
| **Forecast accuracy (e.g., MAPE / WMAPE)** | Error between forecast and actual demand | ↓ Reduce (industry AI benchmarks show 20–50% error reduction vs. naive methods) |
| **Confidence calibration** | Do 80%-confidence recommendations succeed ~80% of the time? | Well-calibrated (low calibration error) |
| **Stockout detection lead time** | How far in advance a stockout risk is flagged | ↑ Increase (earlier warning) |
| **Precision of risk alerts** | % of flagged risks that were genuine | ↑ Increase (protect signal-over-noise) |
| **False-alarm rate** | % of alerts users deem noise | ↓ Reduce |
| **Explanation completeness** | % of recommendations with all four mandatory elements (reasoning, confidence, evidence, impact) | **100% (hard requirement)** |
| **Recommendation outcome accuracy** | Did acting on the recommendation produce the predicted result? | ↑ Increase |

---

## 5. Trust & Experience

| KPI | Definition | Why it matters |
| --- | --- | --- |
| **User-reported trust** | Survey: "I trust StockSense's recommendations" | Trust is the adoption gate |
| **Explanation usefulness** | Do users find the "why" helpful? | Validates explanation-first principle |
| **Net Promoter / satisfaction** | Willingness to recommend | Overall product-market fit signal |
| **Override learning rate** | Improvement in recommendations after user overrides | Validates the feedback loop |

---

## Metric Hierarchy (How They Connect)

```
Trust & Quality (AI is accurate + explained + calibrated)
        │  enables
        ▼
Engagement & Adoption (users act on recommendations)
        │  drives
        ▼
Efficiency (time saved, faster decisions)
        │  produces
        ▼
Business Outcomes (fewer stockouts, less dead stock, higher turnover, freed capital)
        │  = 
        ▼
  NORTH STAR: Recovered margin / prevented loss per retailer
```

If AI quality fails, trust fails; if trust fails, adoption fails; if adoption fails, no
business outcome is achieved. This is why quality and explanation metrics are treated as
foundational, not secondary.

---

## Phase 0 Note

No metric here can be *populated* until implementation (Phase 1+). This document defines
**what** we will measure and the **direction** of success, so that the product is built to
be measurable from day one. Baseline capture for each customer is a required step at
onboarding.
