# 11 — Success Metrics & Metrics Framework

> **Purpose.** Define how we know StockSense is working — end to end — for the retailer
> (business outcomes), the AI (quality and trust), the engineering system (reliability), the
> operation (data and cost health), and adoption (usage and retention). Every metric is
> **measurable**, owned, and tied to the [Product Principles](../product/10-product-principles.md):
> impact, explanation, and trust.

**Guiding rule:** *we measure problems prevented and decisions improved — not features
shipped or charts viewed.*

This document is the canonical **Metrics Framework**. Metrics are grouped into five
categories and each carries a stable ID for cross-reference:

| Prefix | Category | Primary audience |
| --- | --- | --- |
| `BK-` | [Business KPIs](#1-business-kpis) | Retailer, Customer Success, Product |
| `AI-` | [AI Performance KPIs](#2-ai-performance-kpis) | AI/ML, Product |
| `ENG-` | [Engineering KPIs](#3-engineering-kpis) | Platform/SRE, Engineering |
| `OPS-` | [Operational KPIs](#4-operational-kpis) | Platform/SRE, Data Quality, Integration |
| `ADO-` | [Product Adoption KPIs](#5-product-adoption-kpis) | Product, Customer Success |

> **Phase 0 note.** No metric here can be *populated* until implementation (Phase 1+). This
> document defines **what** we measure, **how**, and the **direction/target** of success, so
> the product is instrumented to be measurable from day one. **Baseline capture per customer
> at onboarding is mandatory** — targets below are stated as improvements over that baseline.
> Numeric targets are initial and tuned in Phase 1.

Each metric is specified with a consistent template: **Definition · Formula · Data source ·
Target value · Measurement frequency · Responsible owner · Visualization · Example.**

---

## 1. Business KPIs

The outcomes retailers actually pay for. These are the north-star category — everything else
exists to move these. **Benchmark context:** inventory distortion and shrink cost retailers
an estimated **3–8% of revenue** ([Market Research](../research/04-market-research.md)), so
even single-digit improvements are materially valuable.

### BK-01 — Stockout Rate
| Attribute | Detail |
| --- | --- |
| **Definition** | Share of SKU-days on which an item was out of stock (weighted toward high-velocity items). |
| **Formula** | `Stockout Rate = (SKU-days out of stock / total SKU-days) × 100` |
| **Data source** | Inventory Intelligence state model + POS/IMS stock movements. |
| **Target value** | ↓ Reduce vs. baseline (e.g., −30–50% within 2 quarters). |
| **Frequency** | Weekly (trend), monthly (reported). |
| **Owner** | Customer Success Lead (business); AI Lead (model contribution). |
| **Visualization** | Trend line vs. baseline; heatmap by category/store. |
| **Example** | Baseline 6.0% of SKU-days → 3.3% after two quarters = 45% reduction. |

### BK-02 — Lost-Sales Value
| Attribute | Detail |
| --- | --- |
| **Definition** | Estimated revenue (or margin) lost due to stockouts. |
| **Formula** | `Lost Sales = Σ over stockout periods (forecasted demand − actual sales) × unit price` |
| **Data source** | Forecast Agent (demand) + POS (actuals) + catalog (price/margin). |
| **Target value** | ↓ Reduce vs. baseline. |
| **Frequency** | Weekly (estimate), monthly (reported). |
| **Owner** | Customer Success Lead. |
| **Visualization** | Stacked bar by category; waterfall vs. prior period. |
| **Example** | 400 unmet units × $2.50 = $1,000 lost in a week on one SKU. |

### BK-03 — Dead-Stock Ratio
| Attribute | Detail |
| --- | --- |
| **Definition** | Share of inventory value with no/negligible sales over a defined window. |
| **Formula** | `Dead-Stock Ratio = (value of SKUs with zero sales in window / total inventory value) × 100` |
| **Data source** | Inventory state model + sales history (Analytics Agent aging analysis). |
| **Target value** | ↓ Reduce vs. baseline. |
| **Frequency** | Monthly. |
| **Owner** | Customer Success Lead. |
| **Visualization** | Aging bucket bar chart (0–30 / 31–60 / 61–90 / 90+ days). |
| **Example** | $18k of $150k inventory unsold in 90 days → 12% dead-stock ratio. |

### BK-04 — Overstock / Excess Inventory Value
| Attribute | Detail |
| --- | --- |
| **Definition** | Capital tied up in stock above the optimal/target level. |
| **Formula** | `Excess Value = Σ max(0, on-hand − target stock) × unit cost` |
| **Data source** | Inventory state model + Analytics Agent target levels. |
| **Target value** | ↓ Reduce vs. baseline. |
| **Frequency** | Monthly. |
| **Owner** | Customer Success Lead. |
| **Visualization** | Bar by category; trend line of total excess. |
| **Example** | 500 excess units × $6 cost = $3,000 trapped capital on one SKU. |

### BK-05 — Inventory Turnover
| Attribute | Detail |
| --- | --- |
| **Definition** | How many times inventory is sold and replaced in a period. |
| **Formula** | `Turnover = COGS / average inventory value` |
| **Data source** | POS/ERP (COGS) + inventory state model. |
| **Target value** | ↑ Increase vs. baseline. |
| **Frequency** | Monthly / quarterly. |
| **Owner** | Customer Success Lead. |
| **Visualization** | Gauge vs. target; trend line. |
| **Example** | COGS $600k / avg inventory $100k = 6.0× turns/year. |

### BK-06 — Days of Inventory On Hand (DIO)
| Attribute | Detail |
| --- | --- |
| **Definition** | Average number of days stock is held before sale. |
| **Formula** | `DIO = (average inventory / COGS) × days in period` (≈ `365 / turnover`) |
| **Data source** | POS/ERP + inventory state model. |
| **Target value** | → Optimize toward target band (not simply minimize). |
| **Frequency** | Monthly. |
| **Owner** | Customer Success Lead. |
| **Visualization** | Trend line with target band shading. |
| **Example** | Turnover 6.0× → DIO ≈ 61 days. |

### BK-07 — Spoilage / Expiry Write-Off Rate
| Attribute | Detail |
| --- | --- |
| **Definition** | Value written off due to expiry/spoilage (perishables, pharmacy). |
| **Formula** | `Write-Off Rate = (value expired or spoiled / total inventory value handled) × 100` |
| **Data source** | Write-off/adjustment records + inventory state model. |
| **Target value** | ↓ Reduce vs. baseline. |
| **Frequency** | Weekly (perishables), monthly (reported). |
| **Owner** | Customer Success Lead. |
| **Visualization** | Trend line; bar by category (esp. perishable/pharma). |
| **Example** | $2,100 expired of $70k handled = 3.0% write-off rate. |

### BK-08 — Gross Margin Impact (Attributed)
| Attribute | Detail |
| --- | --- |
| **Definition** | Incremental margin attributable to acted-upon StockSense recommendations. |
| **Formula** | `Margin Impact = Σ (margin of acted recommendations vs. counterfactual baseline)` |
| **Data source** | Recommendation + decision log (acted/outcome) + margin data. |
| **Target value** | ↑ Increase (positive, growing). |
| **Frequency** | Monthly / quarterly. |
| **Owner** | Product Lead + Customer Success Lead. |
| **Visualization** | Waterfall (baseline → recovered margin); cumulative line. |
| **Example** | 45 approved reorder/markdown actions → est. $12k margin recovered in a quarter. |

### BK-09 — Working Capital Freed
| Attribute | Detail |
| --- | --- |
| **Definition** | Capital released by reducing excess/dead stock. |
| **Formula** | `Working Capital Freed = baseline excess inventory value − current excess inventory value` |
| **Data source** | Inventory state model (excess value over time). |
| **Target value** | ↑ Increase (cumulative). |
| **Frequency** | Monthly / quarterly. |
| **Owner** | Customer Success Lead. |
| **Visualization** | Cumulative area chart. |
| **Example** | Excess inventory $50k → $38k = $12k working capital freed. |

---

## 2. AI Performance KPIs

These enforce the [AI Philosophy](../product/12-ai-philosophy.md) and
[ADR-0007](../architecture/adr/0007-ai-governance-framework.md): every output must be
accurate **and** trustworthy. Owner for all: **AI Lead**.

### AI-01 — Forecast Accuracy (WMAPE)
| Attribute | Detail |
| --- | --- |
| **Definition** | Volume-weighted accuracy of demand forecasts vs. actuals. |
| **Formula** | `WMAPE = Σ|actual − forecast| / Σ actual × 100`; report `Accuracy = 100 − WMAPE` |
| **Data source** | Forecast Agent outputs + POS actuals (Learning/Feedback Agent). |
| **Target value** | ↓ WMAPE vs. naive baseline (industry AI shows 20–50% error reduction). |
| **Frequency** | Weekly (rolling), monthly (reported). |
| **Owner** | AI Lead. |
| **Visualization** | Actual-vs-forecast overlay; WMAPE trend line. |
| **Example** | Naive WMAPE 35% → model WMAPE 18% = ~49% error reduction. |

### AI-02 — Forecast Bias
| Attribute | Detail |
| --- | --- |
| **Definition** | Systematic tendency to over- or under-forecast. |
| **Formula** | `Bias = Σ(forecast − actual) / Σ actual × 100` |
| **Data source** | Forecast outputs + actuals, segmented by category/store. |
| **Target value** | → Near 0 (within ±5%); no persistent segment bias (fairness, [ADR-0007 §13](../architecture/adr/0007-ai-governance-framework.md#13-bias-and-fairness-considerations)). |
| **Frequency** | Monthly. |
| **Owner** | AI Lead. |
| **Visualization** | Bias-by-segment bar chart around a zero line. |
| **Example** | +9% bias on beverages → flagged for correction. |

### AI-03 — Confidence Calibration Error (ECE)
| Attribute | Detail |
| --- | --- |
| **Definition** | Gap between stated confidence and realized success rate (does 80% mean 80%?). |
| **Formula** | `ECE = Σ_bins (n_bin / N) × |accuracy_bin − confidence_bin|` |
| **Data source** | Recommendation confidence + realized outcomes (Learning/Feedback Agent). |
| **Target value** | ↓ Minimize (low ECE); miscalibration treated as a defect. |
| **Frequency** | Monthly. |
| **Owner** | AI Lead. |
| **Visualization** | **Reliability diagram** (confidence vs. observed accuracy, with diagonal). |
| **Example** | Items at 0.8 confidence succeed 62% of the time → recalibrate. |

### AI-04 — Stockout Detection Lead Time
| Attribute | Detail |
| --- | --- |
| **Definition** | How far in advance a stockout risk is flagged before it occurs. |
| **Formula** | `Lead Time = mean(stockout event time − first risk-flag time)` |
| **Data source** | Risk Detection alerts + observed stockout events. |
| **Target value** | ↑ Increase (earlier warning, e.g., ≥ supplier lead time). |
| **Frequency** | Weekly. |
| **Owner** | AI Lead. |
| **Visualization** | Distribution histogram of lead-time days. |
| **Example** | Median 4 days warning vs. 3-day resupply → actionable in time. |

### AI-05 — Risk-Alert Precision
| Attribute | Detail |
| --- | --- |
| **Definition** | Share of flagged risks that were genuine (protects signal-over-noise). |
| **Formula** | `Precision = TP / (TP + FP)` |
| **Data source** | Risk alerts + outcome labels (from Learning/Feedback + user feedback). |
| **Target value** | ↑ High (e.g., ≥0.85). |
| **Frequency** | Weekly / monthly. |
| **Owner** | AI Lead. |
| **Visualization** | Precision–recall curve; confusion matrix. |
| **Example** | 85 genuine of 100 alerts → precision 0.85. |

### AI-06 — Risk-Alert Recall
| Attribute | Detail |
| --- | --- |
| **Definition** | Share of actual risk events the system caught. |
| **Formula** | `Recall = TP / (TP + FN)` |
| **Data source** | Detected alerts vs. all realized risk events. |
| **Target value** | ↑ High, balanced against precision. |
| **Frequency** | Monthly. |
| **Owner** | AI Lead. |
| **Visualization** | Precision–recall curve; trend of missed events. |
| **Example** | Caught 78 of 90 real stockouts → recall 0.87. |

### AI-07 — False-Alarm Rate
| Attribute | Detail |
| --- | --- |
| **Definition** | Share of alerts users judge to be noise. |
| **Formula** | `False-Alarm Rate = alerts dismissed as noise / total alerts × 100` |
| **Data source** | Notification interactions + user feedback. |
| **Target value** | ↓ Low (protect attention; one false alarm costs more trust than many correct ones). |
| **Frequency** | Weekly. |
| **Owner** | AI Lead. |
| **Visualization** | Trend line; alerts-by-disposition stacked bar. |
| **Example** | 12 of 100 alerts dismissed as noise → 12%. |

### AI-08 — Explanation Completeness
| Attribute | Detail |
| --- | --- |
| **Definition** | Share of recommendations carrying all four mandatory elements (reasoning, confidence, evidence, impact). |
| **Formula** | `Completeness = recs with all 4 elements / total recs × 100` |
| **Data source** | Recommendation Agent validation logs. |
| **Target value** | **100% (hard requirement)** — enforced at the Recommendation boundary ([ADR-0004](../architecture/adr/0004-explainable-ai-mandate.md)). |
| **Frequency** | Continuous (per output); reported daily. |
| **Owner** | AI Lead. |
| **Visualization** | Single-value gauge pinned at 100% with violation alerts. |
| **Example** | Any output below 100% is a release-blocking defect. |

### AI-09 — Recommendation Outcome Accuracy
| Attribute | Detail |
| --- | --- |
| **Definition** | Did acting on a recommendation produce its predicted result? |
| **Formula** | `Outcome Accuracy = recommendations with realized predicted outcome / acted recommendations × 100` |
| **Data source** | Decision log + realized outcomes (Learning/Feedback Agent). |
| **Target value** | ↑ Increase over time. |
| **Frequency** | Monthly. |
| **Owner** | AI Lead. |
| **Visualization** | Trend line; predicted-vs-actual scatter. |
| **Example** | 68 of 80 acted reorders avoided the predicted stockout → 85%. |

### AI-10 — Grounding / Hallucination Violation Rate
| Attribute | Detail |
| --- | --- |
| **Definition** | Rate of AI outputs failing grounding, numeric-integrity, or contradiction checks. |
| **Formula** | `Violation Rate = outputs failing grounding checks / total AI outputs × 100` |
| **Data source** | Governance validation logs ([ADR-0007 §2](../architecture/adr/0007-ai-governance-framework.md#2-hallucination-prevention-strategy)). |
| **Target value** | → ~0% (treated as top-severity defect class). |
| **Frequency** | Continuous; reported daily. |
| **Owner** | AI Lead. |
| **Visualization** | Control chart with zero-tolerance threshold. |
| **Example** | A generated number disagreeing with `evidence_refs` is blocked and counted. |

### AI-11 — Model Drift Indicator
| Attribute | Detail |
| --- | --- |
| **Definition** | Degradation of model performance/inputs vs. the deployed baseline over time. |
| **Formula** | `Drift = rolling WMAPE − baseline WMAPE` and/or `PSI` on input distributions |
| **Data source** | Rolling accuracy + input-distribution monitoring (Learning/Feedback Agent). |
| **Target value** | Below alert threshold; breach triggers evaluation/rollback ([ADR-0007 §9](../architecture/adr/0007-ai-governance-framework.md#9-model-version-tracking)). |
| **Frequency** | Weekly. |
| **Owner** | AI Lead. |
| **Visualization** | Trend line vs. baseline with alert band; PSI heatmap. |
| **Example** | Rolling WMAPE drifts +7 pts over baseline → drift alert + review. |

---

## 3. Engineering KPIs

Reliability and delivery health of the platform and pipeline. Includes the four DORA
delivery metrics. Owner for all unless noted: **Platform/SRE Lead** (delivery metrics:
**Engineering Lead**).

### ENG-01 — System Availability (Uptime)
| Attribute | Detail |
| --- | --- |
| **Definition** | Share of time core services are available and healthy. |
| **Formula** | `Availability = (uptime / total time) × 100` |
| **Data source** | Health checks + uptime monitoring ([ADR-0008 §17](../architecture/adr/0008-security-architecture.md)). |
| **Target value** | High per SLO (e.g., ≥99.9%). |
| **Frequency** | Continuous; monthly reported. |
| **Owner** | Platform/SRE Lead. |
| **Visualization** | SLO burn-down; uptime trend. |
| **Example** | 43 min downtime in 30 days ≈ 99.90%. |

### ENG-02 — API Latency (p95 / p99)
| Attribute | Detail |
| --- | --- |
| **Definition** | Tail response times for API requests. |
| **Formula** | 95th / 99th percentile of request duration over a window. |
| **Data source** | API gateway / service telemetry. |
| **Target value** | Under budget (e.g., p95 < 300 ms, p99 < 800 ms). |
| **Frequency** | Continuous. |
| **Owner** | Platform/SRE Lead. |
| **Visualization** | Latency percentile bands over time. |
| **Example** | p95 270 ms, p99 610 ms during peak. |

### ENG-03 — Error Rate
| Attribute | Detail |
| --- | --- |
| **Definition** | Share of requests failing with server errors. |
| **Formula** | `Error Rate = (5xx / failed requests / total requests) × 100` |
| **Data source** | Service/gateway logs. |
| **Target value** | ↓ Low (e.g., <0.5%). |
| **Frequency** | Continuous. |
| **Owner** | Platform/SRE Lead. |
| **Visualization** | Error-rate trend with alert threshold. |
| **Example** | 120 errors / 60k requests = 0.2%. |

### ENG-04 — Data Pipeline Latency (Freshness)
| Attribute | Detail |
| --- | --- |
| **Definition** | Delay from data arriving to being processed and analysis-ready. |
| **Formula** | `Pipeline Latency = processed-ready time − record arrival time` |
| **Data source** | Orchestrator + agent pipeline telemetry. |
| **Target value** | ↓ Within cadence target (e.g., < X min/hours per tier). |
| **Frequency** | Continuous. |
| **Owner** | Platform/SRE Lead. |
| **Visualization** | Latency distribution per stage; end-to-end trend. |
| **Example** | POS event → analysis-ready in 8 min. |

### ENG-05 — Throughput
| Attribute | Detail |
| --- | --- |
| **Definition** | Volume the system processes per unit time (requests, records, SKUs). |
| **Formula** | `Throughput = processed units / time window` |
| **Data source** | Pipeline + service telemetry. |
| **Target value** | Meets peak-load requirement with headroom. |
| **Frequency** | Continuous. |
| **Owner** | Platform/SRE Lead. |
| **Visualization** | Throughput vs. capacity line. |
| **Example** | 1.2M records/hour sustained at peak. |

### ENG-06 — Automated Test Coverage
| Attribute | Detail |
| --- | --- |
| **Definition** | Share of code exercised by automated tests (a quality signal, not a goal in itself). |
| **Formula** | `Coverage = (covered lines or branches / total) × 100` |
| **Data source** | CI test/coverage reports. |
| **Target value** | Meets team threshold (e.g., ≥80% on core logic). |
| **Frequency** | Per build / weekly. |
| **Owner** | Engineering Lead. |
| **Visualization** | Coverage trend; module heatmap. |
| **Example** | Recommendation module at 88% branch coverage. |

### ENG-07 — Deployment Frequency (DORA)
| Attribute | Detail |
| --- | --- |
| **Definition** | How often changes are shipped to production. |
| **Formula** | Count of production deployments per period. |
| **Data source** | CI/CD pipeline records. |
| **Target value** | ↑ Higher (small, frequent, safe releases). |
| **Frequency** | Weekly. |
| **Owner** | Engineering Lead. |
| **Visualization** | Bar of deployments/week. |
| **Example** | 9 production deploys in a week. |

### ENG-08 — Change Failure Rate (DORA)
| Attribute | Detail |
| --- | --- |
| **Definition** | Share of deployments causing a failure/rollback. |
| **Formula** | `CFR = (deployments causing failure / total deployments) × 100` |
| **Data source** | CI/CD + incident records. |
| **Target value** | ↓ Low (elite < 15%). |
| **Frequency** | Monthly. |
| **Owner** | Engineering Lead. |
| **Visualization** | Trend line vs. DORA benchmark band. |
| **Example** | 1 of 20 deploys needed rollback = 5%. |

### ENG-09 — Mean Time to Restore (MTTR, DORA)
| Attribute | Detail |
| --- | --- |
| **Definition** | Average time to recover service after a failure. |
| **Formula** | `MTTR = Σ restore durations / number of incidents` |
| **Data source** | Incident tracking. |
| **Target value** | ↓ Low (e.g., < 1 hour for critical). |
| **Frequency** | Monthly. |
| **Owner** | Platform/SRE Lead. |
| **Visualization** | MTTR trend; incident timeline. |
| **Example** | Three incidents restored in 20/35/50 min → MTTR ≈ 35 min. |

### ENG-10 — Lead Time for Changes (DORA)
| Attribute | Detail |
| --- | --- |
| **Definition** | Time from code committed to running in production. |
| **Formula** | `Lead Time = deploy time − commit time` (median). |
| **Data source** | Version control + CI/CD. |
| **Target value** | ↓ Short (elite < 1 day). |
| **Frequency** | Monthly. |
| **Owner** | Engineering Lead. |
| **Visualization** | Median lead-time trend. |
| **Example** | Median 6 hours commit-to-prod. |

---

## 4. Operational KPIs

Health of data, integrations, cost, and running operations. These link tightly to the
[Data Quality Policy](data-quality-policy.md) and the [Risk Register](risk-register.md).

### OPS-01 — Data Quality Score
| Attribute | Detail |
| --- | --- |
| **Definition** | Mean `data_quality_score` across feeds/tenants (composite of the six quality dimensions). |
| **Formula** | `mean(data_quality_score)` over records/feeds ([Data Quality Policy §14](data-quality-policy.md#14-quality-scoring-methodology)). |
| **Data source** | Data Quality Agent scoring. |
| **Target value** | ↑ High-band (≥0.80). |
| **Frequency** | Continuous; daily reported. |
| **Owner** | Data Quality Lead. |
| **Visualization** | Gauge + trend; band distribution (Low/Med/High). |
| **Example** | Tenant feed averaging 0.86 → High band. |

### OPS-02 — Ingestion Success Rate
| Attribute | Detail |
| --- | --- |
| **Definition** | Share of ingestion runs that complete successfully. |
| **Formula** | `Success Rate = (successful runs / total runs) × 100` |
| **Data source** | Integration Agent run logs. |
| **Target value** | ↑ High (e.g., ≥99%). |
| **Frequency** | Continuous; daily. |
| **Owner** | Integration Lead. |
| **Visualization** | Success/failure stacked bar per source. |
| **Example** | 198 of 200 scheduled syncs succeeded = 99%. |

### OPS-03 — Feed Freshness / Lag
| Attribute | Detail |
| --- | --- |
| **Definition** | Age of the newest data per source (detects stalled feeds). |
| **Formula** | `Freshness Lag = now − timestamp(latest record)` |
| **Data source** | Integration + Data Quality watermarks. |
| **Target value** | ↓ Within per-source SLA. |
| **Frequency** | Continuous. |
| **Owner** | Integration Lead. |
| **Visualization** | Per-source freshness status board (green/amber/red). |
| **Example** | POS feed lag 6 min (OK); ERP extract lag 30 h (amber). |

### OPS-04 — Quarantine Rate
| Attribute | Detail |
| --- | --- |
| **Definition** | Share of records held out of analysis due to quality issues. |
| **Formula** | `Quarantine Rate = (quarantined records / total records) × 100` |
| **Data source** | Data Quality pipeline logs. |
| **Target value** | ↓ Reduce (with orphan/negative causes trending down). |
| **Frequency** | Daily / weekly. |
| **Owner** | Data Quality Lead. |
| **Visualization** | Trend line; quarantine reason breakdown (Pareto). |
| **Example** | 1.4% of rows quarantined, mostly orphan SKUs. |

### OPS-05 — Escalation Resolution Time
| Attribute | Detail |
| --- | --- |
| **Definition** | Time from a data-quality quarantine/escalation to resolution. |
| **Formula** | `mean(resolved time − escalation time)` |
| **Data source** | Escalation workflow logs ([Data Quality Policy §15](data-quality-policy.md#15-escalation-workflow)). |
| **Target value** | ↓ Reduce. |
| **Frequency** | Weekly. |
| **Owner** | Data Quality Lead + Customer Success Lead. |
| **Visualization** | Cycle-time distribution; SLA compliance bar. |
| **Example** | Median resolution 1.2 days. |

### OPS-06 — Operational Incident Rate
| Attribute | Detail |
| --- | --- |
| **Definition** | Count/severity of operational incidents per period. |
| **Formula** | Count by severity per period (with Ops MTTR from ENG-09). |
| **Data source** | Incident tracking. |
| **Target value** | ↓ Reduce, especially high-severity. |
| **Frequency** | Monthly. |
| **Owner** | Platform/SRE Lead. |
| **Visualization** | Incidents-by-severity stacked bar; trend. |
| **Example** | 0 critical, 3 minor incidents this month. |

### OPS-07 — Backup Success & Restore-Test Pass Rate
| Attribute | Detail |
| --- | --- |
| **Definition** | Backups completing successfully and passing periodic restore tests. |
| **Formula** | `Backup Success = successful backups / scheduled × 100`; `Restore Pass = passed restore tests / attempted × 100` |
| **Data source** | Backup system + DR test records ([ADR-0008 §18](../architecture/adr/0008-security-architecture.md)). |
| **Target value** | 100% backup success; all restore tests pass. |
| **Frequency** | Backup: daily; restore test: monthly/quarterly. |
| **Owner** | Platform/SRE Lead. |
| **Visualization** | Status calendar; restore-test pass/fail log. |
| **Example** | 30/30 daily backups; last restore test passed within RTO. |

### OPS-08 — Infrastructure Cost per Active Tenant
| Attribute | Detail |
| --- | --- |
| **Definition** | Cost efficiency of serving each active retailer. |
| **Formula** | `Cost per Tenant = total infra cost / active tenants` |
| **Data source** | Cloud billing + tenant registry. |
| **Target value** | ↓ Trend down with scale (protects unit economics; mitigates vendor cost risk RSK-09). |
| **Frequency** | Monthly. |
| **Owner** | Platform/SRE Lead + Product Lead. |
| **Visualization** | Cost-per-tenant trend vs. tenant growth. |
| **Example** | $9,000 infra / 300 tenants = $30/tenant/month. |

### OPS-09 — Alert Signal-to-Noise Ratio
| Attribute | Detail |
| --- | --- |
| **Definition** | Share of operational alerts that are actionable (avoids alert fatigue). |
| **Formula** | `Signal-to-Noise = actionable alerts / total alerts × 100` |
| **Data source** | Monitoring/alerting + on-call disposition. |
| **Target value** | ↑ High actionable share. |
| **Frequency** | Weekly. |
| **Owner** | Platform/SRE Lead. |
| **Visualization** | Actionable-vs-noise stacked trend. |
| **Example** | 46 of 50 alerts actionable = 92%. |

---

## 5. Product Adoption KPIs

Value is only realized if the product is used and its recommendations are acted on. Owner
mix: **Product Lead** and **Customer Success Lead**.

### ADO-01 — Recommendation Adoption Rate
| Attribute | Detail |
| --- | --- |
| **Definition** | Share of recommendations approved (including approved-with-modification) — the core proxy for usefulness and trust. |
| **Formula** | `Adoption = (approved + approved-with-modification) / total recommendations × 100` |
| **Data source** | Decision log (approve/modify/reject). |
| **Target value** | ↑ High and rising. |
| **Frequency** | Weekly. |
| **Owner** | Product Lead. |
| **Visualization** | Trend line; disposition funnel (shown → viewed → approved). |
| **Example** | 320 of 500 recommendations acted on = 64% adoption. |

### ADO-02 — Time-to-First-Value (TTFV)
| Attribute | Detail |
| --- | --- |
| **Definition** | Time from connecting data to receiving the first actionable recommendation. |
| **Formula** | `TTFV = first actionable recommendation time − data-connected time` |
| **Data source** | Onboarding + recommendation logs. |
| **Target value** | ↓ Minutes (validates the low-friction promise). |
| **Frequency** | Per onboarding; monthly cohort. |
| **Owner** | Customer Success Lead. |
| **Visualization** | Distribution histogram; cohort trend. |
| **Example** | Median TTFV 12 minutes for new tenants. |

### ADO-03 — Stickiness (DAU/WAU)
| Attribute | Detail |
| --- | --- |
| **Definition** | Habit strength — daily over weekly active users. |
| **Formula** | `Stickiness = DAU / WAU` |
| **Data source** | Product usage analytics. |
| **Target value** | ↑ Higher (e.g., managers checking the morning brief daily). |
| **Frequency** | Weekly. |
| **Owner** | Product Lead. |
| **Visualization** | Stickiness trend; DAU/WAU overlay. |
| **Example** | DAU 210 / WAU 300 = 0.70 stickiness. |

### ADO-04 — Retention / Renewal Rate
| Attribute | Detail |
| --- | --- |
| **Definition** | Share of customers continuing to use and pay (inverse of churn). |
| **Formula** | `Retention = (renewed / up-for-renewal) × 100`; `Churn = 100 − Retention` |
| **Data source** | Billing + subscription records. |
| **Target value** | ↑ High retention / ↓ low churn. |
| **Frequency** | Monthly / quarterly. |
| **Owner** | Customer Success Lead. |
| **Visualization** | Cohort retention curve. |
| **Example** | 92 of 100 renewals = 92% retention (8% churn). |

### ADO-05 — Modify-vs-Reject Ratio
| Attribute | Detail |
| --- | --- |
| **Definition** | Distinguishes "close but adjusted" (modify) from "wrong" (reject). |
| **Formula** | `Ratio = modified recommendations / rejected recommendations` |
| **Data source** | Decision log. |
| **Target value** | ↑ Higher (modify > reject signals near-useful output). |
| **Frequency** | Weekly. |
| **Owner** | Product Lead + AI Lead. |
| **Visualization** | Modify/reject stacked bar over time. |
| **Example** | 90 modified vs. 30 rejected → ratio 3.0. |

### ADO-06 — Feature Adoption Rate
| Attribute | Detail |
| --- | --- |
| **Definition** | Share of eligible users actively using a given feature. |
| **Formula** | `Feature Adoption = (users using feature / eligible users) × 100` |
| **Data source** | Product usage analytics. |
| **Target value** | ↑ Increase for value-driving features. |
| **Frequency** | Monthly. |
| **Owner** | Product Lead. |
| **Visualization** | Feature-adoption bar; per-feature trend. |
| **Example** | 40% of managers use the markdown recommendation. |

### ADO-07 — User-Reported Trust
| Attribute | Detail |
| --- | --- |
| **Definition** | Survey measure: "I trust StockSense's recommendations." |
| **Formula** | Mean survey score (e.g., 1–5) / % agreeing. |
| **Data source** | In-product surveys. |
| **Target value** | ↑ High (trust is the adoption gate). |
| **Frequency** | Quarterly. |
| **Owner** | Product Lead + Customer Success Lead. |
| **Visualization** | Score trend; distribution. |
| **Example** | 4.3/5 average trust score. |

### ADO-08 — Explanation Usefulness
| Attribute | Detail |
| --- | --- |
| **Definition** | Whether users find the "why" behind recommendations helpful (validates explanation-first). |
| **Formula** | % of explanations rated helpful (thumbs-up / survey). |
| **Data source** | In-product feedback on explanations. |
| **Target value** | ↑ High. |
| **Frequency** | Monthly / quarterly. |
| **Owner** | Product Lead. |
| **Visualization** | Helpful-rate trend. |
| **Example** | 81% of viewed explanations rated helpful. |

### ADO-09 — Net Promoter Score (NPS)
| Attribute | Detail |
| --- | --- |
| **Definition** | Overall willingness to recommend — product-market-fit signal. |
| **Formula** | `NPS = %promoters − %detractors` |
| **Data source** | Periodic NPS survey. |
| **Target value** | ↑ Positive and rising. |
| **Frequency** | Quarterly. |
| **Owner** | Customer Success Lead. |
| **Visualization** | NPS gauge; promoter/passive/detractor bar. |
| **Example** | 55% promoters − 15% detractors = NPS 40. |

### ADO-10 — Override Learning Rate
| Attribute | Detail |
| --- | --- |
| **Definition** | Improvement in recommendation quality after users override — validates the feedback loop. |
| **Formula** | Change in adoption/outcome accuracy attributable to override-driven learning over time. |
| **Data source** | Learning/Feedback Agent + decision outcomes. |
| **Target value** | ↑ Positive (system learns from overrides). |
| **Frequency** | Quarterly. |
| **Owner** | AI Lead + Product Lead. |
| **Visualization** | Before/after adoption trend around learning cycles. |
| **Example** | Adoption on a category rose 8 pts after override-driven tuning. |

---

## Metric Hierarchy (How They Connect)

The categories form a causal chain. Foundational quality and reliability enable adoption,
which produces business outcomes.

```
Engineering + Operational (reliable system, trustworthy data)
        │  enable
        ▼
AI Performance (accurate, calibrated, explained, grounded)
        │  earns
        ▼
Product Adoption (users act on recommendations, stay, and trust)
        │  drives
        ▼
Business KPIs (fewer stockouts, less dead stock, higher turnover, freed capital)
        │  =
        ▼
  NORTH STAR: Recovered margin / prevented loss per retailer
```

If engineering/operations fail, data and uptime fail; if AI quality fails, trust fails; if
trust fails, adoption fails; if adoption fails, no business outcome is achieved. This is why
the foundational categories are treated as first-class, not secondary.

---

## Owner Roster (Summary)

| Owner role | Owns (categories / examples) |
| --- | --- |
| **Customer Success Lead** | Business outcomes (BK-01…09), TTFV, retention, NPS |
| **Product Lead** | Adoption (ADO-01…10), margin attribution, feature adoption |
| **AI Lead** | All AI Performance KPIs (AI-01…11) |
| **Engineering Lead** | Delivery metrics (ENG-06…08, ENG-10), test coverage |
| **Platform/SRE Lead** | Reliability (ENG-01…05, ENG-09), operational health (OPS-06…09) |
| **Data Quality Lead** | OPS-01, OPS-04, OPS-05 (data quality) |
| **Integration Lead** | OPS-02, OPS-03 (ingestion/freshness) |

Roles mirror the ownership model in the [Risk Register](risk-register.md).

---

## Governance & Review

- **Cadence.** Metrics are reviewed on their stated frequency; the full framework is
  reviewed at each phase boundary and adjusted with rationale.
- **Baselines are mandatory.** Every customer's baseline is captured at onboarding; business
  targets are expressed as improvements over that baseline.
- **Targets are tuned, semantics are fixed.** Numeric targets are refined in Phase 1;
  definitions, formulas, and directions of success are stable.
- **Traceability.** Metrics link to the controls that produce them:
  [Data Quality Policy](data-quality-policy.md), [ADR-0007](../architecture/adr/0007-ai-governance-framework.md),
  [ADR-0008](../architecture/adr/0008-security-architecture.md), and the
  [Risk Register](risk-register.md) detection methods.
- **Anti-gaming.** No single metric is optimized in isolation (e.g., recall is balanced
  against false-alarm rate; DIO is optimized to a band, not minimized). The hierarchy guards
  against local optimization that harms the north star.

---

## Related Documents

- [Product Principles](../product/10-product-principles.md) · [AI Philosophy](../product/12-ai-philosophy.md)
- [Data Quality Policy](data-quality-policy.md) · [Risk Register](risk-register.md) · [Business Workflow](09-business-workflow.md)
- [ADR-0004 — Explainable-AI Mandate](../architecture/adr/0004-explainable-ai-mandate.md) · [ADR-0007 — AI Governance](../architecture/adr/0007-ai-governance-framework.md) · [ADR-0008 — Security Architecture](../architecture/adr/0008-security-architecture.md)
- [Market Research](../research/04-market-research.md) (benchmark context)
