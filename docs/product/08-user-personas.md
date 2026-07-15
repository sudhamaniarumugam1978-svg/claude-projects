# 08 — User Personas

These personas are realistic composites of the primary buyers and users defined in
[Target Customers](07-target-customers.md). They exist to keep design decisions grounded in
real goals, constraints, and frustrations. Each persona lists the questions StockSense must
answer for them and how success is felt in their day.

---

## Persona 1 — Retail Owner ("Priya, the Owner-Operator")

| Attribute | Detail |
| --- | --- |
| Role | Owner of a 2-location grocery and general store |
| Age / tech comfort | 47 / moderate; lives in her phone and WhatsApp, not in spreadsheets |
| Reports to | Herself (and the bank) |
| Time for analysis | Minutes per day, usually early morning or late evening |

**Goals**
- Protect cash flow; stop money from being trapped in stock that will not sell.
- Never lose a regular customer to an empty shelf on a staple item.
- Understand the health of the business without becoming a data analyst.

**Frustrations**
- "I only find out something was a problem after it already cost me."
- Her IMS shows current stock but never tells her what to *do*.
- Consultants and ERPs are far too expensive and complex for her.

**What StockSense must answer**
- "Where am I losing money right now, and where am I about to?"
- "What are the top 3 things I should do this week, and why?"

**Definition of success**
- A short, ranked, plain-language morning brief she trusts and can act on in minutes.

---

## Persona 2 — Store Manager ("Marcus, the Floor Leader")

| Attribute | Detail |
| --- | --- |
| Role | Manager of a single supermarket location |
| Age / tech comfort | 34 / comfortable with apps and dashboards |
| Reports to | Retail Owner / Operations Manager |
| Time for analysis | 30–60 minutes daily, interrupted constantly |

**Goals**
- Keep shelves full on high-velocity items, especially before weekends and holidays.
- Reduce perishable waste and end-of-day markdowns.
- Hit the store's inventory and availability targets.

**Frustrations**
- Reordering is reactive and based on memory and gut feel.
- Demand spikes (weather, local events, paydays) catch him off guard.
- Too many alerts that are not actually urgent; real risks get buried.

**What StockSense must answer**
- "Which items will stock out before my next delivery, and how much should I order?"
- "What's about to spoil or go stale that I should discount today?"

**Definition of success**
- Fewer surprise stockouts and less waste, with recommendations he can approve on the go.

---

## Persona 3 — Inventory Manager ("Aisha, the Detail Owner")

| Attribute | Detail |
| --- | --- |
| Role | Inventory / stock manager across a small pharmacy chain |
| Age / tech comfort | 39 / high; power user of the IMS, builds her own spreadsheets |
| Reports to | Operations Manager |
| Time for analysis | Several hours daily — this *is* her job |

**Goals**
- Optimize reorder points, quantities, and timing across thousands of SKUs.
- Minimize expiry write-offs on regulated, date-sensitive stock.
- Balance service level against carrying cost.

**Frustrations**
- Her spreadsheets cannot keep up with SKU count or seasonality.
- She spends most of her time *finding* problems, leaving little time to *solve* them.
- She distrusts tools that give answers without showing their work.

**What StockSense must answer**
- "Which SKUs need attention today, ranked by impact, and what exactly should I change?"
- "Show me the evidence and confidence behind each recommendation so I can trust it."

**Definition of success**
- The system does the *finding* (detection + forecasting) so she can focus on the
  *deciding*; every recommendation is auditable.

---

## Persona 4 — Operations Manager ("David, the Multi-Store Overseer")

| Attribute | Detail |
| --- | --- |
| Role | Operations manager overseeing several convenience/electronics stores |
| Age / tech comfort | 45 / high-level; wants summaries, not raw data |
| Reports to | Owner / executive leadership |
| Time for analysis | Wants a 5-minute read, drill-down only when needed |

**Goals**
- See inventory health across all stores at a glance.
- Standardize good decision-making across managers of varying skill.
- Tie inventory performance to financial outcomes (turnover, margin, working capital).

**Frustrations**
- Inconsistent decisions between stores and managers.
- No single, trustworthy view of where the biggest risks and opportunities are.
- Existing reports are backward-looking and require interpretation.

**What StockSense must answer**
- "Across all my stores, where is the biggest risk and the biggest opportunity right now?"
- "Are my managers acting on the right things, and what's the expected impact?"

**Definition of success**
- An executive-level summary that rolls up risk, recommended actions, and expected impact,
  with the ability to drill into any store.

---

## Cross-Persona Design Implications

| Insight | Design consequence |
| --- | --- |
| All personas are time-poor | Lead with the few decisions that matter; rank by impact |
| Trust varies with expertise | Always show reasoning, evidence, and confidence |
| Skill varies across users | Recommendations must be executable by non-experts |
| Owners/Ops want summaries; managers want specifics | Provide layered detail: executive summary → store → SKU |
| Everyone distrusts black boxes | No unexplained outputs, ever |

These implications feed directly into the [Product Principles](10-product-principles.md)
and the [Agent Architecture](../architecture/13-agent-architecture.md) (notably the
Executive Agent for summaries and the Recommendation Agent for actionability).
