# 06 — Product Scope

The purpose of this document is to draw a hard, defensible boundary around StockSense.
Scope discipline is a feature: it is what keeps StockSense a focused decision intelligence
engine rather than a diluted "everything" platform. Every proposed capability is measured
against a single test:

> **Does this help a retailer make a better inventory decision, before a problem occurs,
> with an explanation they can trust?**

If the answer is no, it is out of scope — no matter how attractive it seems.

---

## What StockSense WILL Do

### 1. Ingest and normalize retail data
- Connect to existing systems of record (POS, IMS, spreadsheets, CSV/exports) via an
  Integration layer.
- Normalize products, sales history, stock levels, suppliers, and lead times into a
  consistent internal model.
- Continuously refresh as new sales and stock data arrive.

### 2. Detect inventory risk proactively
- Identify items at risk of **stockout** before the shelf empties.
- Identify **overstock and dead stock** tying up capital.
- Detect **demand anomalies** (spikes, drops, emerging trends).
- Flag **slow-moving** and **at-risk-of-expiry / obsolescence** inventory.

### 3. Forecast demand
- Produce item-level demand forecasts over relevant horizons.
- Account for seasonality, trend, and recurring patterns.
- Attach a confidence interval / score to every forecast.

### 4. Explain every situation
- For each detected risk, state **why** it is happening in plain language.
- Cite the **supporting data** (the sales pattern, the lead time, the trend) behind it.

### 5. Recommend specific actions
- Recommend concrete actions: reorder quantities, timing, markdown candidates,
  redistribution, and de-listing candidates.
- Rank recommendations by **business impact** (dollars at stake).
- Attach a **confidence score** and **expected impact** to each recommendation.

### 6. Support the human decision
- Present recommendations for the manager to **approve, modify, or reject**.
- Capture decisions and outcomes to improve future recommendations.
- Provide an executive-level summary of the state of inventory health and decisions.

### 7. Notify at the right moment
- Surface time-sensitive risks and recommendations through appropriate channels.
- Respect a "signal over noise" bar — only what matters, when it matters.

---

## What StockSense WILL NOT Do

These exclusions are intentional and are protected by [ADR-0002](../architecture/adr/0002-scope-boundaries-not-an-erp.md).

| Excluded capability | Why it is excluded |
| --- | --- |
| **Be an ERP** (finance, HR, procurement execution, accounting) | Out of mission; a crowded, capital-intensive market. We *inform* procurement decisions; we do not run the general ledger. |
| **Be a POS / checkout system** | We consume sales data; we do not process transactions or payments. |
| **Be a system-of-record IMS** | We are the *decision layer above* the IMS, not a replacement for stock record-keeping. |
| **Be a CRM** | Customer relationship management is a different problem and a different buyer. |
| **Be "a dashboard project"** | Dashboards are a means, never the product. We deliver decisions, not chart libraries. |
| **Be a generic AI chatbot** | The engine is the product; conversational access is a thin, optional interface. |
| **Execute purchase orders directly with suppliers (V1)** | Automatic ordering removes the human from the loop. We recommend; the human executes. Direct execution is a *later* opt-in, human-approved capability, never a default. |
| **Make final business decisions autonomously** | Prohibited by [AI Philosophy](12-ai-philosophy.md). The human always decides. |
| **Provide unexplained "black box" outputs** | Prohibited by [Product Principles](10-product-principles.md). |
| **Warehouse / bin-location / WMS logistics** | Physical warehouse operations are out of the decision-intelligence mission. |
| **Employee scheduling, payroll, or store operations at large** | Not an inventory decision. |

---

## Scope Guardrails Against Feature Creep

1. **The Decision Test.** Every feature must pass the test at the top of this document.
2. **Layer, don't replace.** If a feature requires us to become a system of record, it is
   probably out of scope.
3. **Explanation is mandatory.** If a feature cannot be explained to a non-expert, it does
   not ship.
4. **Impact over volume.** We do not add features that produce *more* output; we add
   features that produce *better decisions*.
5. **Human-in-the-loop is permanent.** No feature may remove the human's final authority.

---

## Boundary Cases (Explicit Rulings)

- **"Can StockSense generate a purchase order?"** — It can *draft and recommend* one with
  quantity and timing. It will not *transmit* it to a supplier without human approval, and
  automated transmission is a post-V1, opt-in capability only.
- **"Can StockSense show charts?"** — Yes, but only in service of explaining a decision.
  Charts are evidence, not the product.
- **"Can StockSense answer free-form questions?"** — Yes, through a thin assistant
  interface grounded in the retailer's data, but only as a window onto the engine — never
  as the engine itself.

See [Product Roadmap](../planning/14-product-roadmap.md) for how in-scope capabilities are
sequenced across V1, V2, and V3.
