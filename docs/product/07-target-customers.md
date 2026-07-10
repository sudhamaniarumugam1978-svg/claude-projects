# 07 — Target Customers

## Positioning Summary

StockSense targets **independent and mid-sized retailers who carry physical inventory,
feel the pain of stockouts and dead stock directly on their margins, and cannot justify
the cost, complexity, or specialist staffing of an enterprise ERP.**

This is precisely the segment that incumbents underserve: too advanced for a basic IMS to
help them decide, too small for an ERP to be economical. See
[Competitor Analysis](../research/05-competitor-analysis.md).

---

## Primary Target Segments

### 1. Retail Stores (general / independent)
- **Profile:** Single or few locations, hundreds to a few thousand SKUs, owner-operated or
  small management team.
- **Pain:** Reordering by gut feel; capital trapped in slow movers; surprise stockouts on
  best sellers.
- **Why StockSense:** Gives them planning intelligence they currently lack entirely,
  without hiring an analyst.

### 2. Supermarkets / Grocery
- **Profile:** High SKU count, high velocity, significant perishables, thin margins.
- **Pain:** Perishable waste (dead stock with a clock on it), out-of-stocks on staples,
  strong seasonality and day-of-week patterns.
- **Why StockSense:** Perishability and velocity make demand forecasting and early risk
  detection especially valuable; small forecast improvements meaningfully cut spoilage and
  lost sales.

### 3. Mini Marts / Convenience Stores
- **Profile:** Small footprint, limited shelf space, fast-moving consumer goods, minimal
  back-office staff.
- **Pain:** Every shelf slot matters; a dead SKU is a direct opportunity cost; no time for
  analysis.
- **Why StockSense:** Ranked, few-decisions-that-matter output fits an owner who has
  minutes, not hours, and no analytics tooling.

### 4. Pharmacies
- **Profile:** Regulated products, expiry-sensitive stock, mix of fast and long-tail SKUs,
  demand tied to seasons and health cycles.
- **Pain:** Expiry write-offs, stockouts on essential medicines, compliance-sensitive
  record accuracy.
- **Why StockSense:** Expiry-aware risk detection and demand forecasting directly reduce
  costly write-offs and dangerous stockouts.

### 5. Electronics Stores
- **Profile:** High unit value, rapid product obsolescence, long supplier lead times,
  lumpy demand.
- **Pain:** Obsolescence risk on high-value stock; long lead times punish forecasting
  errors severely; capital heavily concentrated in inventory.
- **Why StockSense:** High per-unit stakes make explained, confidence-scored reorder and
  markdown timing recommendations especially high-value.

---

## Common Thread Across Primary Segments

| Attribute | Shared characteristic |
| --- | --- |
| Inventory intensity | Physical stock is a major working-capital commitment |
| Decision maturity | Decisions made by experience/intuition, not systematic forecasting |
| Staffing | No dedicated data science or planning team |
| Tooling | Have a POS/IMS (system of record) but no decision layer |
| Sensitivity | Directly feel stockout and dead-stock costs in the P&L |

---

## Buyer vs. User

- **Economic buyer:** Retail Owner or Operations Manager (controls budget, feels the
  margin impact).
- **Primary daily users:** Store Manager and Inventory Manager (act on recommendations).
- **Executive consumer:** Owner / Operations Manager (consumes summaries, sets policy).

Detailed personas are in [User Personas](08-user-personas.md).

---

## Future Markets (Documented Separately, Out of V1 Scope)

These are explicitly **not** the initial focus and are recorded here only to show the
expansion path. They are governed by the [Product Roadmap](../planning/14-product-roadmap.md).

- **Multi-location chains and franchises** — cross-store redistribution and network-level
  optimization.
- **E-commerce and omnichannel retailers** — unified online/offline demand signals.
- **Wholesale and distribution** — upstream demand aggregation.
- **Specialty verticals** — fashion/apparel (size-curve planning), auto parts, hardware.
- **Restaurants and food service** — ingredient-level perishable forecasting.

Each future market must still pass the same qualification test: inventory-intensive,
decision-underserved, and unable to justify enterprise ERP planning.
