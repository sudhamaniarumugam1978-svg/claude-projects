# 04 — Market Research

> **Purpose.** Establish, with evidence, that retail inventory decision-making is a large,
> costly, and structurally underserved problem — and that the underserved segment
> (independent and mid-sized retailers) is exactly where AI-driven decision intelligence
> can create outsized value.

All figures are cited. Where sources report slightly different numbers for the same
metric (e.g., annual inventory-distortion estimates that shift year to year), the range is
noted rather than a single point figure. _Content from cited sources was rephrased for
compliance with licensing restrictions._

---

## 1. The Scale of the Problem

### 1.1 Inventory distortion (out-of-stocks + overstocks)
- The combined global cost of out-of-stocks and overstocks — "inventory distortion" — has
  been estimated at roughly **$1.77 trillion (2023)**, easing to about **$1.73 trillion
  (2025)** as retailers invested in improvements.[^ihl2023][^ihl2025]
- The split is heavily weighted toward empty shelves: **out-of-stocks ≈ 68% (~$1.2
  trillion)** versus **overstocks ≈ 32% (~$562 billion)**.[^csa]
- Root causes tracked by IHL include empty shelves (replenishment failures), system
  inaccuracies, pricing mismatches, buying errors, vendor problems, and theft.[^ihlfix]

### 1.2 Inventory shrink (loss)
- U.S. retail **shrink reached ~1.6% of total sales in 2022 ($112.1 billion)**, up from
  **$93.9 billion in 2021**, per the National Retail Federation's National Retail Security
  Survey.[^nrf]
- A significant share of shrink is *not* theft but **administrative and process error**
  (miscounts, receiving errors, unrecorded returns) — precisely the kind of inaccuracy
  that better decision support and detection can reduce.[^shrinkbreakdown]

### 1.3 Revenue impact at the store level
- Industry analysis attributes roughly **3–8% of annual revenue** loss to poor inventory
  management, split between lost sales (stockouts) and carrying costs
  (overstock).[^lucent]

**Implication:** Inventory decision quality is not a marginal optimization; it is one of
the largest recoverable losses in retail.

---

## 2. Anatomy of the Core Pain Points

### 2.1 Stockouts (out-of-stocks)
- **What it is:** Demand exists but the item is unavailable.
- **Cost:** Immediate lost sale, plus longer-term customer churn to competitors.
- **Why it persists:** Reorder decisions are reactive and threshold-based; they do not
  anticipate demand shifts (seasonality, day-of-week, local events, lead-time variance).

### 2.2 Overstock and dead stock
- **What it is:** Capital trapped in inventory that sells slowly or not at all.
- **Cost:** Tied-up working capital, storage cost, markdowns, spoilage, and obsolescence.
- **Why it persists:** Over-ordering to avoid stockouts, poor demand estimation, and lack
  of early warning on slowing movers.

### 2.3 Inventory loss / shrink
- **What it is:** Inventory that disappears from records versus reality.
- **Cost:** Direct margin loss; also *corrupts the data* that decisions rely on.
- **Why it persists:** Theft plus a large tail of administrative and process errors.

### 2.4 Demand forecasting difficulty
- **What it is:** Predicting future demand per SKU accurately enough to act.
- **Cost:** Every forecasting error becomes either a stockout or an overstock.
- **Why it persists:** Small retailers rely on intuition or naive averages; real demand is
  seasonal, trend-driven, and event-sensitive.

### 2.5 The "find vs. fix" tax
- Inventory managers spend a disproportionate share of their time *finding* problems
  (scanning reports, building spreadsheets) rather than *fixing* them. This manual
  analysis burden is itself a major, under-counted cost — and a direct target for
  automation.

---

## 3. Current Inventory Optimization Techniques (and Their Limits)

| Technique | What it does | Limitation for the target segment |
| --- | --- | --- |
| **Reorder point / min-max** | Reorder when stock hits a threshold | Static; ignores demand shifts, seasonality, and lead-time variance |
| **Economic Order Quantity (EOQ)** | Optimize order size vs. holding cost | Assumes stable demand; fragile in real retail |
| **ABC analysis** | Prioritize SKUs by value/volume | Descriptive, not predictive; still leaves the decision to the human |
| **Safety stock formulas** | Buffer against variability | Requires good demand/variance estimates the retailer rarely has |
| **Statistical time-series (e.g., moving averages, exponential smoothing)** | Extrapolate history | Struggles with intermittent demand, promotions, and regime changes |
| **Machine-learning forecasting** | Learn complex patterns from data | Historically confined to enterprises with data teams and budget |

**The gap:** The most effective techniques (ML forecasting, optimization) have been locked
inside enterprise tooling and specialist teams. The techniques accessible to small
retailers (reorder points, gut feel) are the weakest.

---

## 4. The Opportunity: AI-Driven Decision Intelligence

Evidence that closing the gap is high-value:
- AI-driven forecasting can **reduce forecast error by 20–50%** and cut **lost sales and
  product unavailability by up to 65%**, per McKinsey.[^mck1]
- AI can **reduce inventory levels by 20–30%** through better demand forecasting and
  optimization.[^mck2]
- Independent syntheses report roughly **20% average reduction in forecasting error** and
  **up to ~10% less excess inventory** where models are actually deployed.[^gitnux]

The prize is not "more accurate charts." It is *materially less lost sales and less
trapped capital* — the exact costs quantified in Section 1.

---

## 5. Current AI Adoption in Retail (and the Underserved Middle)

- AI adoption is **concentrated in large organizations**: surveys report ~78% of large
  organizations using AI in at least one function, while **small firms lag** due to
  capital constraints, limited technical expertise, and integration cost.[^jpm][^itjones]
- In retail specifically, a large share of AI initiatives remain in exploratory or
  proof-of-concept stages rather than operational use — the technology is proven but
  **adoption is early**, especially below the enterprise tier.[^adl]
- Barriers for small and mid-sized retailers are consistent across studies: **cost, lack
  of in-house expertise, and integration/infrastructure limitations.**[^smebarriers]

**Implication and thesis:** The value of AI in inventory is proven, but it has been
delivered almost exclusively to enterprises. There is a large, underserved middle —
independent and mid-sized retailers — for whom an **affordable, explainable,
low-integration decision layer** removes exactly the barriers (cost, expertise,
integration) that studies identify. This is StockSense's market. See
[Target Customers](../product/07-target-customers.md) and
[Value Proposition](../product/03-value-proposition.md).

---

## 6. Market Trends Shaping the Opportunity

1. **From reporting to decisioning.** Buyers increasingly want tools that recommend
   actions, not just visualize data.
2. **Explainability as a purchase criterion.** As AI enters money-losing/making
   decisions, trust and transparency become required, not optional.
3. **Decision layers over systems of record.** Modern architectures favor composable
   layers on top of existing data, lowering switching costs.
4. **AI cost curve falling.** Capabilities once requiring a data team are increasingly
   available as services, making the underserved middle economically reachable.

---

## 7. Research Conclusions

1. Inventory distortion, shrink, and forecasting error represent **trillions in global
   loss** and **3–8% of revenue** at the store level.[^ihl2023][^nrf][^lucent]
2. The most effective optimization techniques exist but have been **inaccessible** to the
   target segment.
3. AI-driven decision intelligence delivers **large, measured improvements** in forecast
   error, lost sales, and inventory levels.[^mck1][^mck2]
4. Adoption is **concentrated in enterprises**, leaving independent and mid-sized retailers
   underserved — a clear, evidence-backed market opening for StockSense.[^jpm][^adl]

---

## Sources

[^ihl2023]: RetailTouchPoints, "IHL Study: Inventory Distortion Will Cost Retailers $1.77 Trillion in 2023" (2023). https://www.retailtouchpoints.com/features/industry-insights/ihl-study-inventory-distortion-will-cost-retailers-1-77-trillion-in-2023
[^ihl2025]: IHL Group, "Retail Inventory Crisis Persists Despite $172 Billion in Improvements" (Sept. 2025). https://www.ihlservices.com/news/analyst-corner/2025/09/retail-inventory-crisis-persists-despite-172-billion-in-improvements/
[^csa]: ChainStoreAge, "Study: Global retail losses due to inventory 'distortion' hit $1.77 trillion." https://chainstoreage.com/study-global-retail-losses-due-inventory-distortion-hit-177-trillion
[^ihlfix]: IHL Group, "Fixing Inventory Distortion: Who's Winning, Who's Failing, What's Working." https://www.ihlservices.com/product/fixing-inventory-distortion-whos-winning-whos-failing-whats-working/
[^nrf]: National Retail Federation, "Shrink Accounted for Over $112 Billion in Industry Losses in 2022" / "National Retail Security Survey 2023." https://nrf.com/media-center/press-releases/shrink-accounted-over-112-billion-industry-losses-2022-according-nrf ; https://nrf.com/research/national-retail-security-survey-2023
[^shrinkbreakdown]: Reporting on NRF 2023 shrink composition (administrative error, audit discrepancies, unrecorded returns). https://gitnux.org/retail-shrinkage-statistics/ ; https://zipdo.co/retail-shrinkage-statistics/
[^lucent]: Lucent Innovation, "How Retail Businesses on Microsoft Dynamics NAV Can Unlock Smarter Inventory Management" (2025). https://www.lucentinnovation.com/resources/technology-posts/how-retail-businesses-on-microsoft-dynamics-nav-can-unlock-smarter-inventory-management-with-data-engineering
[^mck1]: McKinsey & Company, "Stronger forecasting in operations management—even with weak data." https://www.mckinsey.com/capabilities/operations/our-insights/ai-driven-operations-forecasting-in-data-light-environments
[^mck2]: McKinsey & Company, "Harnessing the power of AI in distribution operations." https://www.mckinsey.com/industries/industrials/our-insights/distribution-blog/harnessing-the-power-of-ai-in-distribution-operations
[^gitnux]: Gitnux, "AI in the Retail Industry Statistics" (2026). https://gitnux.org/ai-in-the-retail-industry-statistics/
[^jpm]: JPMorganChase Institute, "Understanding the use of AI among small businesses" (citing NFIB 2025, OECD 2024, Acemoglu et al. 2023). https://www.jpmorganchase.com/institute/all-topics/business-growth-and-entrepreneurship/understanding-ai-use-by-small-businesses
[^itjones]: Jones IT, "2025 AI Adoption Report: What 40% Cost Barriers Mean for SMEs." https://www.itjones.com/blogs/2025-ai-adoption-report-what-40-percent-cost-barriers-mean-for-smes
[^adl]: Arthur D. Little, "Retail AI" viewpoint. https://www.adlittle.com/en/insights/viewpoints/retail-ai
[^smebarriers]: Research on barriers to AI implementation in SMEs (infrastructure, expertise, cost). https://www.researchgate.net/publication/384112060_Barriers_to_the_implementation_of_artificial_intelligence_in_small_and_medium_sized_enterprises_Pilot_study
