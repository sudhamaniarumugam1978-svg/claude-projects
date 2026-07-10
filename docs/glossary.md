# Glossary

> **Purpose.** A shared vocabulary for StockSense across retail, inventory, AI/ML, and
> engineering domains. Definitions are concise and technically accurate, written to be
> understood by both developers and business stakeholders. Where a term has a specific
> meaning *within StockSense*, that usage is noted and linked to the relevant document.

Terms are grouped by domain for browsing; each group is alphabetized. Cross-references use
**See also** links.

**Quick navigation:** [Retail & Inventory](#retail--inventory-terms) ·
[Forecasting & Analytics](#forecasting--analytics-terms) ·
[AI / ML](#ai--ml-terms) · [Systems & Integration](#systems--integration-terms) ·
[Platform & Security](#platform--security-terms) ·
[StockSense-Specific](#stocksense-specific-terms)

---

## Retail & Inventory Terms

**ABC Analysis**
A prioritization technique that classifies inventory into tiers (A = high value/impact,
B = moderate, C = low) so attention and controls focus where they matter most. Descriptive
and static — it ranks items but does not predict or decide. *In StockSense:* a supporting
diagnostic, not a substitute for predictive risk detection.

**Carrying Cost (Holding Cost)**
The total cost of holding inventory over time — capital tied up, storage, insurance,
spoilage, and obsolescence. High carrying cost is the penalty for overstock.

**Dead Stock**
Inventory that has had no or negligible sales over a defined window; capital effectively
frozen on the shelf. See also *Overstock*, *Dead-Stock Ratio* in
[Success Metrics](business/11-success-metrics.md).

**EOQ (Economic Order Quantity)**
The order quantity that minimizes total inventory cost by balancing ordering cost against
holding cost. Formula (classic): `EOQ = √(2·D·S / H)`, where `D` = annual demand,
`S` = cost per order, `H` = holding cost per unit per year. Assumes stable demand, so it is
fragile in real retail.

**GMROI (Gross Margin Return on Investment)**
A profitability measure of inventory: how much gross margin is earned per unit of inventory
cost. Formula: `GMROI = gross margin / average inventory cost`. A GMROI above 1 means
inventory earns more margin than it costs to hold.

**Inventory Distortion**
The combined financial cost of *out-of-stocks* (lost sales) and *overstocks* (excess/markdowns).
An industry umbrella metric quantifying the total penalty of getting inventory levels wrong.
See [Market Research](research/04-market-research.md) for cited scale.

**Inventory Turnover (Turns)**
How many times inventory is sold and replaced in a period. Formula:
`Turnover = COGS / average inventory value`. Higher turns generally indicate efficient
inventory use. See also *DIO*.

**Days of Inventory On Hand (DIO)**
Average number of days stock is held before it sells. Formula:
`DIO = (average inventory / COGS) × days ≈ 365 / turnover`. Optimized to a healthy band —
not simply minimized.

**Lead Time**
The elapsed time between placing a replenishment order and the goods becoming available for
sale. *Lead-time variance* (unpredictability) is as important as the average, and is a key
input to *Safety Stock* and *Reorder Point*.

**Overstock**
Holding more inventory than demand justifies, tying up working capital and risking markdowns,
spoilage, or obsolescence. The opposite failure mode from a *Stockout*.

**Perishability / Expiry**
The property of stock that loses value or becomes unsellable after a date (e.g., grocery,
pharmacy). Introduces a time clock on inventory decisions and expiry-driven write-offs.

**Reorder Point (ROP)**
The stock level at which a replenishment order should be placed to avoid a stockout during
the lead time. Formula: `ROP = (average demand during lead time) + safety stock`.

**Safety Stock**
Buffer inventory held to absorb variability in demand and lead time, reducing stockout risk
at the cost of higher carrying cost. Sized from demand/lead-time variability and a target
service level.

**Service Level**
The target probability of *not* stocking out during a replenishment cycle (e.g., 95%).
Higher service levels require more safety stock.

**Shrink (Shrinkage)**
The loss of inventory versus recorded levels, from theft, administrative/process error, or
system inaccuracies. Measured as a percentage of sales. Shrink also *corrupts the data*
decisions rely on. See [Market Research](research/04-market-research.md).

**SKU (Stock Keeping Unit)**
The unique identifier for a distinct, sellable product variant (specific item, size, color,
pack). The primary key that joins inventory, sales, and forecasting. *In StockSense:* an
invalid or unknown SKU is a data-quality event — see
[Data Quality Policy §5](business/data-quality-policy.md#5-invalid-sku-handling).

**Stockout (Out-of-Stock, OOS)**
When demand exists but the item is unavailable to sell — an immediate lost sale and a
driver of customer churn. The problem StockSense most directly aims to predict and prevent.

**Write-Off**
Removing inventory value from the books because it is unsellable (expired, spoiled, damaged,
obsolete). A direct margin loss and a key perishable/pharmacy metric.

---

## Forecasting & Analytics Terms

**Bias (Forecast Bias)**
A systematic tendency to over- or under-forecast. Formula:
`Bias = Σ(forecast − actual) / Σ actual`. Persistent bias in a segment is also a *fairness*
concern. See [Success Metrics AI-02](business/11-success-metrics.md#2-ai-performance-kpis).

**Confidence Interval**
A range around a forecast expressing uncertainty (e.g., "demand 90–120 units, 80%
interval"). Communicates *how sure* a prediction is, not just a point estimate.

**Demand Forecasting**
Predicting future demand per SKU over a horizon, accounting for trend, seasonality, and
events. The core "what will happen" capability that feeds risk detection and reorder
recommendations. *In StockSense:* every forecast carries calibrated confidence — see
[Agent Catalog](agents/agent-catalog.md).

**Forecast Error**
The difference between forecasted and actual demand. Common measures: *MAE*, *MAPE*
(mean absolute percentage error), and *WMAPE* (volume-weighted MAPE). Every forecast error
becomes either a stockout or an overstock, which is why reducing it is high-value.

**MAPE / WMAPE**
*Mean Absolute Percentage Error* and its *Weighted* variant. `WMAPE = Σ|actual − forecast| /
Σ actual × 100`. WMAPE is preferred in retail because it weights by volume and handles
low-volume SKUs more robustly. See also *Forecast Error*.

**Seasonality**
Recurring demand patterns tied to time (day-of-week, holidays, seasons). A primary signal
in demand forecasting; ignoring it causes predictable stockouts and overstocks.

**Time Series**
Data points ordered in time (e.g., daily sales per SKU). The primary input structure for
demand forecasting.

---

## AI / ML Terms

**Calibration (Confidence Calibration)**
The property that stated confidence matches real-world outcomes — outputs asserted at 80%
confidence should be correct ~80% of the time. Measured with *ECE* (Expected Calibration
Error). *In StockSense:* miscalibration is treated as a defect
([ADR-0007](architecture/adr/0007-ai-governance-framework.md)).

**Confidence Score**
A calibrated value in `[0,1]` attached to every AI output, indicating how much to trust it.
Drives behavior via *thresholds* (Low / Medium / High). Can only be weakened by poor data
quality, never inflated. See
[ADR-0007 §3–4](architecture/adr/0007-ai-governance-framework.md#3-confidence-score-methodology).

**Explainable AI (XAI)**
AI whose outputs are accompanied by human-understandable reasoning and traceable evidence,
rather than opaque "black box" results. *In StockSense:* every recommendation must carry
reasoning, confidence, supporting data, and business impact — enforced at the Recommendation
Agent boundary ([ADR-0004](architecture/adr/0004-explainable-ai-mandate.md)).

**Grounding**
Constraining AI outputs to verifiable source data (the retailer's own data) rather than the
model's general/parametric knowledge. The primary defense against *hallucination*.

**Hallucination**
An AI output that is fabricated or unsupported by evidence — a confident-sounding but false
claim or number. *In StockSense:* prevented via grounding, numeric-integrity checks, and
"evidence or silence," and treated as a top-severity defect
([ADR-0007 §2](architecture/adr/0007-ai-governance-framework.md#2-hallucination-prevention-strategy)).

**Human-in-the-Loop (HITL)**
A design where AI proposes and a human makes the final decision (approve / modify / reject).
The system augments, never replaces, the decision-maker
([ADR-0003](architecture/adr/0003-human-in-the-loop-decisioning.md)).

**Large Language Model (LLM)**
A neural model trained on large text corpora that generates and interprets natural language.
*In StockSense:* used for narrative explanation and the thin assistant interface — never to
free-generate the numbers that drive decisions (those come from the deterministic pipeline).

**Model Drift**
Gradual degradation of model performance as real-world patterns diverge from training
conditions (demand shifts, new products, seasonality). Detected via rolling accuracy and
input-distribution monitoring (e.g., *PSI*); triggers evaluation or rollback. See
[Risk Register RSK-13](business/risk-register.md).

**Model Versioning**
Assigning immutable version identifiers to models and pinning them in production, so every
output is attributable and upgrades are staged, evaluated, and reversible
([ADR-0007 §9](architecture/adr/0007-ai-governance-framework.md#9-model-version-tracking)).

**Multi-Agent System**
An architecture composed of specialized, cooperating agents that each own a cohesive
responsibility and communicate via defined contracts, rather than one monolith. *In
StockSense:* the Decision Intelligence Engine is an 11-agent system
([Agent Architecture](architecture/13-agent-architecture.md)).

**Prompt Engineering**
The practice of designing, structuring, and refining the instructions given to an LLM to
produce reliable, well-formed outputs. *In StockSense:* prompts are versioned, reviewed
release artifacts (not edited live), and each output records the prompt version used
([ADR-0007 §8](architecture/adr/0007-ai-governance-framework.md#8-prompt-versioning-strategy)).

**Recommendation Engine**
A system that produces ranked, actionable suggestions. *In StockSense:* the Recommendation
Agent converts risk findings and forecasts into specific, prioritized actions — each with
reasoning, confidence, evidence, and business impact — and is the enforcement point for
explainability ([Agent Catalog](agents/agent-catalog.md)).

**Retrieval-Augmented Generation (RAG)**
A pattern where a model retrieves relevant source data (often via a *vector database*) and
generates output grounded in it, improving accuracy and reducing hallucination.

**Vector Database**
A datastore optimized for storing and searching high-dimensional *embeddings* by similarity,
enabling semantic search and retrieval. Commonly used to ground LLM responses (see *RAG*).
*In StockSense:* a candidate component for grounded assistant retrieval, subject to tenant
isolation.

---

## Systems & Integration Terms

**API (Application Programming Interface)**
A defined contract that lets software components exchange data and invoke functionality. *In
StockSense:* connectors consume system-of-record APIs; failures are a tracked risk
([Risk Register RSK-02](business/risk-register.md)).

**Connector**
An integration component that ingests data from a specific external source (a given POS, IMS,
ERP, or file format) and maps it toward the internal model. New connectors are additive.

**CSV (Comma-Separated Values)**
A plain-text tabular file format, common for manual data exports. The lowest-trust ingestion
source, given the strictest validation profile
([Data Quality Policy §11](business/data-quality-policy.md#11-csv-validation)).

**ERP (Enterprise Resource Planning)**
Integrated business software spanning finance, procurement, supply chain, and more.
Authoritative but complex and enterprise-priced. *In StockSense:* a data source to layer on
top of — **not** something StockSense is or replaces
([ADR-0006](architecture/adr/0006-layer-over-systems-of-record.md)).

**IMS (Inventory Management System)**
Software that records stock levels and movements — a *system of record* for inventory.
StockSense is the *decision layer above* an IMS, not a replacement for it.

**OMS (Order Management System)**
Software that manages the order lifecycle across channels — capture, routing, fulfillment,
and status — often bridging sales channels and inventory/fulfillment.

**POS (Point of Sale)**
The system that processes customer transactions at checkout and is a primary source of
real-time sales data. *In StockSense:* a high-trust but high-volume feed with its own
validation profile ([Data Quality Policy §12](business/data-quality-policy.md#12-pos-validation)).

**System of Record**
The authoritative source for a given dataset (e.g., the POS/IMS/ERP for sales and stock).
StockSense integrates with systems of record rather than becoming one.

**WMS (Warehouse Management System)**
Software that manages physical warehouse operations — receiving, put-away, bin locations,
picking, and shipping. Out of StockSense's decision-intelligence scope
([Product Scope](product/06-product-scope.md)).

---

## Platform & Security Terms

**Audit Log**
An immutable, append-only, tamper-evident record of decisions and security events, enabling
after-the-fact reconstruction. See
[ADR-0007 §7](architecture/adr/0007-ai-governance-framework.md#7-audit-logging-requirements)
and [ADR-0008 §16](architecture/adr/0008-security-architecture.md).

**Encryption at Rest / in Transit**
Protecting stored data (at rest) and data moving across networks (in transit) with strong
cryptography. Both are mandatory in StockSense
([ADR-0008 §7–8](architecture/adr/0008-security-architecture.md)).

**JWT (JSON Web Token)**
A signed, self-contained token carrying identity/authorization claims. *In StockSense:*
access tokens are short-lived with rotating, revocable refresh tokens
([ADR-0008 §3](architecture/adr/0008-security-architecture.md#3-jwt-lifecycle)).

**Least Privilege**
Granting the minimum access necessary for a task, limiting the blast radius of any
compromise. A core security principle across the platform.

**Multi-Tenancy / Tenant Isolation**
Serving many retailers ("tenants") from shared infrastructure while guaranteeing that no
tenant can access another's data. Enforced end-to-end, including at the data layer
([ADR-0008 §9](architecture/adr/0008-security-architecture.md)).

**OWASP Top 10**
An industry-standard list of the most critical web application security risks, used as a
baseline threat checklist. See
[ADR-0008 §15](architecture/adr/0008-security-architecture.md#15-owasp-top-10-considerations).

**RBAC (Role-Based Access Control)**
Authorization model that grants permissions by role, combined in StockSense with mandatory
*tenant scoping* and deny-by-default
([ADR-0008 §2](architecture/adr/0008-security-architecture.md#2-role-based-access-control-rbac)).

**RPO / RTO (Recovery Point / Time Objective)**
Disaster-recovery targets: *RPO* = maximum acceptable data loss (how far back a restore may
go); *RTO* = maximum acceptable time to restore service. See
[ADR-0008 §20](architecture/adr/0008-security-architecture.md).

**Secrets Management**
Centralized, access-audited handling of credentials and keys (no secrets in source, logs, or
client bundles), with rotation
([ADR-0008 §5](architecture/adr/0008-security-architecture.md)).

---

## StockSense-Specific Terms

**Agent**
A specialized component owning one cohesive responsibility in the Decision Intelligence
Engine (e.g., Forecast Agent, Risk Detection Agent). See the
[Agent Catalog](agents/agent-catalog.md).

**Confidence Band (Low / Medium / High)**
The standardized tiers that map a *confidence score* to system behavior (e.g., Low-band
outputs are not emitted as recommendations). See
[ADR-0007 §4](architecture/adr/0007-ai-governance-framework.md#4-confidence-thresholds-low-medium-high).

**`data_quality_score`**
A `[0,1]` trustworthiness score attached to records/datasets by the Data Quality Agent that
travels downstream, capping or reducing the confidence of anything built on that data. See
[Data Quality Policy §14](business/data-quality-policy.md#14-quality-scoring-methodology).

**Decision Intelligence**
The discipline of turning data directly into recommended actions with explicit reasoning —
the category StockSense occupies. Distinct from reporting/BI, which stops at visualization
([ADR-0001](architecture/adr/0001-decision-intelligence-not-dashboards.md)).

**Decision Intelligence Engine**
The core StockSense product: the multi-agent system that predicts, explains, and recommends.
"The engine is the product; the assistant is a thin window onto it."

**`evidence_refs`**
References carried on every message that point to the specific upstream data used to produce
an output, making explanations and traceability *structural* rather than reconstructed. See
[Agent Architecture §5](architecture/13-agent-architecture.md).

**Mandatory Recommendation Elements**
The four fields every recommendation must include or it is not emitted: **reasoning,
confidence, supporting data, and business impact**
([ADR-0004](architecture/adr/0004-explainable-ai-mandate.md)).

**Message Envelope**
The shared contract wrapping inter-agent messages, carrying `trace_id`, `evidence_refs`,
`confidence`, and `data_quality_score`. The mechanism that makes governance guarantees
enforceable. See [Agent Architecture §5.2](architecture/13-agent-architecture.md#52-canonical-message-envelope-conceptual).

**Orchestrator**
The cross-cutting agent that sequences the pipeline, parallelizes independent analysis,
enforces message contracts, and owns end-to-end *traceability* via `trace_id`. Added during
the critical review of the agent set
([Agent Architecture §2](architecture/13-agent-architecture.md#2-critical-evaluation-of-the-suggested-agent-set)).

**Quarantine**
Holding suspect data out of analysis (rather than trusting or silently discarding it) pending
reconciliation or human resolution
([Data Quality Policy §15](business/data-quality-policy.md#15-escalation-workflow)).

**Signal over Noise**
The principle that only high-value, high-confidence, high-impact items reach the user; an
unopened or dismissed alert is a failure. Enforced by the Notification Agent
([Product Principles](product/10-product-principles.md)).

**`trace_id`**
A unique identifier propagated across the whole decision chain so any recommendation can be
followed back to its raw inputs and logic — the operational basis of "no black boxes."

---

## Related Documents

- [Executive Summary](executive-summary.md) · [Documentation Index](README.md)
- [Agent Architecture](architecture/13-agent-architecture.md) · [Agent Catalog](agents/agent-catalog.md)
- [Data Quality Policy](business/data-quality-policy.md) · [Success Metrics](business/11-success-metrics.md) · [Risk Register](business/risk-register.md)
- [ADR Index](architecture/adr/README.md)
