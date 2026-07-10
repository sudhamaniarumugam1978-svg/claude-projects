# Risk Register

> **Purpose.** Identify, assess, and assign ownership for the material risks facing
> StockSense, and record how each is detected and mitigated. This register is a living
> governance artifact: it makes risk explicit and accountable rather than implicit, and it
> connects each risk to the controls already established in the
> [AI Governance Framework (ADR-0007)](../architecture/adr/0007-ai-governance-framework.md),
> [Security Architecture (ADR-0008)](../architecture/adr/0008-security-architecture.md), and
> [Data Quality Policy](data-quality-policy.md).

Phase 0 note: this is planning documentation. Probabilities and statuses are initial
assessments for the pre-implementation stage and are reviewed each phase.

---

## How to Read This Register

- **Risk ID** — stable identifier (`RSK-NN`) for cross-reference.
- **Category** — Data, Integration, AI/ML, Infrastructure, Security, Compliance, or Vendor.
- **Probability** — likelihood if no/partial mitigation were in place: **Low / Medium / High**.
- **Business impact** — effect on retailers, trust, and revenue.
- **Technical impact** — effect on the platform and its correctness.
- **Severity** — combined view (Probability × Impact): **Low / Medium / High / Critical**.
- **Detection method** — how we know the risk is materializing.
- **Mitigation strategy** — controls that prevent, reduce, or contain the risk.
- **Owner** — the accountable role.
- **Status** — **Open** (identified, mitigation planned), **Mitigating** (controls being
  built/active), **Monitored** (accepted residual risk under watch).

Because StockSense is pre-implementation, most statuses are **Open** with mitigations
**planned** and traceable to an ADR/policy; they move to **Mitigating**/**Monitored** as
Phase 1 delivers the controls.

---

## Risk Summary (Heat View)

| ID | Risk | Category | Probability | Severity | Owner | Status |
| --- | --- | --- | :---: | :---: | --- | --- |
| RSK-01 | Poor retailer data | Data | High | High | Data Quality Lead | Open |
| RSK-02 | External API failures | Integration | Medium | High | Integration Lead | Open |
| RSK-03 | POS integration failures | Integration | High | High | Integration Lead | Open |
| RSK-04 | Inventory inaccuracies | Data | High | High | Data Quality Lead | Open |
| RSK-05 | AI hallucinations | AI/ML | Medium | Critical | AI Lead | Open |
| RSK-06 | Low-confidence recommendations | AI/ML | High | Medium | AI Lead | Open |
| RSK-07 | Incorrect forecasts | AI/ML | Medium | High | AI Lead | Open |
| RSK-08 | Network outages | Infrastructure | Medium | High | Platform/SRE Lead | Open |
| RSK-09 | Vendor dependency | Vendor | Medium | High | Architecture Lead | Open |
| RSK-10 | Database corruption | Infrastructure | Low | Critical | Platform/SRE Lead | Open |
| RSK-11 | Authentication failures | Security | Medium | Critical | Security Lead | Open |
| RSK-12 | Regulatory changes | Compliance | Medium | High | Product/Compliance Lead | Open |
| RSK-13 | Model drift | AI/ML | High | High | AI Lead | Open |

---

## Detailed Risk Register

### RSK-01 — Poor retailer data

| Field | Detail |
| --- | --- |
| **Risk ID** | RSK-01 |
| **Description** | Ingested retailer data is incomplete, malformed, inconsistent, or hand-edited (esp. CSV), undermining every downstream decision. |
| **Category** | Data |
| **Probability** | High — SMB/independent data is frequently messy ([Market Research](04-market-research.md)). |
| **Business impact** | Wrong or withheld recommendations; eroded trust; slow time-to-value. |
| **Technical impact** | Corrupted inputs propagate into forecasts, risk detection, and impact estimates. |
| **Detection method** | Data Quality pipeline scoring; completeness/validity/accuracy metrics; quarantine and reject rates ([Data Quality Policy §17](data-quality-policy.md#17-data-quality-metrics)). |
| **Mitigation strategy** | Enforce the [Data Quality Policy](data-quality-policy.md): staged validation, `data_quality_score` that travels downstream, quarantine over silent cleaning, escalation to the tenant data owner. Low-quality data lowers confidence or withholds output ([ADR-0007](../architecture/adr/0007-ai-governance-framework.md)). |
| **Owner** | Data Quality Lead |
| **Status** | Open (policy defined; enforcement built in Phase 1) |

### RSK-02 — External API failures

| Field | Detail |
| --- | --- |
| **Risk ID** | RSK-02 |
| **Description** | Third-party/system-of-record APIs (POS/IMS/ERP/supplier) return errors, time out, throttle, or change contracts. |
| **Category** | Integration |
| **Probability** | Medium |
| **Business impact** | Stale or missing data; delayed recommendations; degraded trust if unnoticed. |
| **Technical impact** | Ingestion gaps; partial datasets; cascading downstream staleness. |
| **Detection method** | Connector health checks, error-rate and latency monitoring, freshness/lag metrics, schema-drift detection. |
| **Mitigation strategy** | Retries with backoff, circuit breakers, and timeouts; continue on last-known-good data **flagged as stale** (Integration Agent degradation); schema-version pinning; alerting via monitoring ([Agent Catalog](../agents/agent-catalog.md), [ADR-0008 §17](../architecture/adr/0008-security-architecture.md)). |
| **Owner** | Integration Lead |
| **Status** | Open |

### RSK-03 — POS integration failures

| Field | Detail |
| --- | --- |
| **Risk ID** | RSK-03 |
| **Description** | POS feed stalls, retransmits, delivers partial batches, or arrives out of order, so sales signal is wrong or misinterpreted as "no demand." |
| **Category** | Integration |
| **Probability** | High — POS feeds are high-volume and prone to sync issues. |
| **Business impact** | Missed stockout risks; distorted demand; poor reorder recommendations. |
| **Technical impact** | Duplicate/late/missing events corrupt the demand signal and stock reconciliation. |
| **Detection method** | Feed-gap detection, freshness watermark, duplicate rate, ordering/late-arrival flags ([Data Quality Policy §12](data-quality-policy.md#12-pos-validation)). |
| **Mitigation strategy** | Idempotent ingestion on transaction id; gap detection treats silence as a data-quality event (not zero sales); late/out-of-order handling; reconciliation against stock movements; stalled-feed alerts. |
| **Owner** | Integration Lead |
| **Status** | Open |

### RSK-04 — Inventory inaccuracies

| Field | Detail |
| --- | --- |
| **Risk ID** | RSK-04 |
| **Description** | Recorded stock diverges from physical reality (shrink, miscounts, unrecorded receipts/returns), including impossible negative inventory. |
| **Category** | Data |
| **Probability** | High — shrink/admin error is endemic in retail ([Market Research](04-market-research.md)). |
| **Business impact** | Recommendations based on false stock positions; wrong reorders; lost trust. |
| **Technical impact** | Negative inventory and contradictions corrupt the inventory truth model. |
| **Detection method** | Negative-inventory detection, cross-record reconciliation, discrepancy surfacing ([Data Quality Policy §6](data-quality-policy.md#6-negative-inventory-detection)). |
| **Mitigation strategy** | Flag and quarantine impossible values; surface discrepancies rather than clamping; reconcile via adjacent adjustments; mark coverage gaps in summaries; reflect in confidence scoring. |
| **Owner** | Data Quality Lead |
| **Status** | Open |

### RSK-05 — AI hallucinations

| Field | Detail |
| --- | --- |
| **Risk ID** | RSK-05 |
| **Description** | An AI-generated rationale, number, or recommendation is fabricated or unsupported by evidence. |
| **Category** | AI/ML |
| **Probability** | Medium |
| **Business impact** | A confident but false recommendation causes a costly wrong decision and destroys trust — an existential risk to the product thesis. |
| **Technical impact** | Ungrounded output bypasses the evidence chain if uncontrolled. |
| **Detection method** | Grounding/contradiction checks; numeric-integrity validation (numbers must match `evidence_refs`); explanation-completeness monitoring; human override signals ([ADR-0007 §2](../architecture/adr/0007-ai-governance-framework.md#2-hallucination-prevention-strategy)). |
| **Mitigation strategy** | Hallucination-prevention strategy: grounding requirement, numbers from the deterministic pipeline (not free-generated), schema-constrained outputs, "evidence or silence," and hard rejection of outputs missing mandatory elements at the Recommendation Agent boundary. |
| **Owner** | AI Lead |
| **Status** | Open (treated as a top-severity defect class) |

### RSK-06 — Low-confidence recommendations

| Field | Detail |
| --- | --- |
| **Risk ID** | RSK-06 |
| **Description** | The system produces recommendations it is not sufficiently confident in, risking either noise (if shown) or missed value (if over-suppressed). |
| **Category** | AI/ML |
| **Probability** | High (frequent, especially on sparse data) |
| **Business impact** | Noise erodes trust; over-suppression reduces usefulness. Managed correctly, this is a *feature* (honesty), not a failure. |
| **Technical impact** | Requires correct band routing and fallback behavior across agents. |
| **Detection method** | Confidence-band distribution; Low-band suppression rate; adoption vs. reject/modify ratios ([Success Metrics](11-success-metrics.md)). |
| **Mitigation strategy** | Confidence thresholds (Low/Medium/High) with deterministic behavior: Low-band items are not emitted as recommendations, downgraded to informational, or trigger a request for more data; Medium flagged as uncertain ([ADR-0007 §4–5](../architecture/adr/0007-ai-governance-framework.md#4-confidence-thresholds-low-medium-high)). |
| **Owner** | AI Lead |
| **Status** | Open |

### RSK-07 — Incorrect forecasts

| Field | Detail |
| --- | --- |
| **Risk ID** | RSK-07 |
| **Description** | Demand forecasts are materially wrong (bias or high error), leading to bad reorder/markdown recommendations. |
| **Category** | AI/ML |
| **Probability** | Medium |
| **Business impact** | Stockouts or overstock — the exact costs StockSense exists to reduce. |
| **Technical impact** | Error/bias propagates into risk detection and recommendations. |
| **Detection method** | Forecast accuracy (MAPE/WMAPE) vs. actuals; calibration monitoring; segment-bias monitoring by the Learning/Feedback Agent ([Success Metrics](11-success-metrics.md)). |
| **Mitigation strategy** | Method selection by data density with simpler defensible fallbacks; confidence intervals on every forecast; feedback loop from realized outcomes; forecasts feed recommendations only with attached confidence ([Agent Catalog](../agents/agent-catalog.md)). |
| **Owner** | AI Lead |
| **Status** | Open |

### RSK-08 — Network outages

| Field | Detail |
| --- | --- |
| **Risk ID** | RSK-08 |
| **Description** | Loss of network/connectivity between clients, StockSense services, or external systems of record. |
| **Category** | Infrastructure |
| **Probability** | Medium |
| **Business impact** | Temporary unavailability; delayed data and recommendations. |
| **Technical impact** | Ingestion and delivery interruptions; possible partial processing. |
| **Detection method** | Uptime/health monitoring, connectivity probes, error-rate spikes, alerting ([ADR-0008 §17](../architecture/adr/0008-security-architecture.md)). |
| **Mitigation strategy** | Resilient retries and queuing; graceful degradation (read-only/last-known-good, clearly labeled); redundancy per disaster-recovery design; fail safe rather than emit unsafe outputs ([ADR-0008 §20](../architecture/adr/0008-security-architecture.md)). |
| **Owner** | Platform/SRE Lead |
| **Status** | Open |

### RSK-09 — Vendor dependency

| Field | Detail |
| --- | --- |
| **Risk ID** | RSK-09 |
| **Description** | Over-reliance on a specific third party (cloud, model provider, POS/ERP vendor) creates lock-in, pricing, or continuity risk. |
| **Category** | Vendor |
| **Probability** | Medium |
| **Business impact** | Cost increases, service disruption, or forced migration; feature loss if a provider changes terms. |
| **Technical impact** | Tight coupling to a provider's APIs/models complicates substitution. |
| **Detection method** | Dependency inventory review; provider SLA/roadmap tracking; single-point-of-failure analysis. |
| **Mitigation strategy** | Abstraction boundaries (source-agnostic core, [ADR-0006](../architecture/adr/0006-layer-over-systems-of-record.md)); versioned/pinned models with rollback ([ADR-0007 §9](../architecture/adr/0007-ai-governance-framework.md)); avoid deep coupling; evaluate portability; contractual review. |
| **Owner** | Architecture Lead |
| **Status** | Open |

### RSK-10 — Database corruption

| Field | Detail |
| --- | --- |
| **Risk ID** | RSK-10 |
| **Description** | Corruption or loss of core datastores, including the inventory truth model or the immutable audit log. |
| **Category** | Infrastructure |
| **Probability** | Low |
| **Business impact** | Severe: potential data loss, incorrect decisions, and loss of auditability/trust. |
| **Technical impact** | Integrity loss across the platform; possible cross-record inconsistency. |
| **Detection method** | Integrity checks/checksums, backup-verification results, restore tests, anomaly monitoring ([ADR-0008 §16–18](../architecture/adr/0008-security-architecture.md)). |
| **Mitigation strategy** | Encrypted, regular, tested backups (3-2-1); tamper-evident append-only audit log; tenant-aware granular restore; DR runbooks with RPO/RTO targets; least-privilege DB access to limit corruption vectors ([ADR-0008 §9, §18, §20](../architecture/adr/0008-security-architecture.md)). |
| **Owner** | Platform/SRE Lead |
| **Status** | Open |

### RSK-11 — Authentication failures

| Field | Detail |
| --- | --- |
| **Risk ID** | RSK-11 |
| **Description** | Auth weaknesses or incidents: credential compromise, token theft/misuse, or a broken-access-control flaw enabling cross-tenant access. |
| **Category** | Security |
| **Probability** | Medium (attempts are constant against any multi-tenant, data-rich target) |
| **Business impact** | Critical: cross-tenant data exposure would be existential for trust and could carry legal/regulatory consequences. |
| **Technical impact** | Unauthorized access, privilege escalation, integrity compromise. |
| **Detection method** | Auth success/failure and lockout monitoring; authz-denial spikes; token-reuse detection; anomalous access alerts ([ADR-0008 §16–17](../architecture/adr/0008-security-architecture.md)). |
| **Mitigation strategy** | OIDC/OAuth2 + MFA for privileged roles; short-lived JWT with rotating, revocable refresh and reuse detection; RBAC with **mandatory tenant scoping** and deny-by-default; Argon2id password hashing; rate limiting on auth endpoints ([ADR-0008 §1–4, §10](../architecture/adr/0008-security-architecture.md)). |
| **Owner** | Security Lead |
| **Status** | Open |

### RSK-12 — Regulatory changes

| Field | Detail |
| --- | --- |
| **Risk ID** | RSK-12 |
| **Description** | New or changing regulation (data protection, AI transparency/fairness, sector rules such as pharmacy) imposes new obligations. |
| **Category** | Compliance |
| **Probability** | Medium (AI and privacy regulation is actively evolving) |
| **Business impact** | Compliance cost, feature constraints, or market-access limits if unaddressed. |
| **Technical impact** | May require changes to data handling, retention, explainability, or audit exports. |
| **Detection method** | Regulatory horizon scanning; periodic compliance review; customer/contractual requirement tracking. |
| **Mitigation strategy** | Governance and security built in early: explainability, audit trails, data minimization, retention/deletion, tenant isolation ([ADR-0007](../architecture/adr/0007-ai-governance-framework.md), [ADR-0008 §19](../architecture/adr/0008-security-architecture.md)); governance roadmap aligns to emerging standards (SOC 2 / ISO 27001-style, AI-governance frameworks). |
| **Owner** | Product/Compliance Lead |
| **Status** | Open |

### RSK-13 — Model drift

| Field | Detail |
| --- | --- |
| **Risk ID** | RSK-13 |
| **Description** | Forecasting/ranking model performance degrades over time as demand patterns, catalog, or seasonality shift away from training conditions. |
| **Category** | AI/ML |
| **Probability** | High (drift is expected in real retail over time) |
| **Business impact** | Gradually worsening recommendations and calibration; silent erosion of value and trust. |
| **Technical impact** | Accuracy/calibration decay; stale assumptions in the pipeline. |
| **Detection method** | Continuous accuracy and **calibration monitoring** (does 80% mean 80%?); drift detection after data/model changes; override-rate trends by the Learning/Feedback Agent ([ADR-0007 §3, §9](../architecture/adr/0007-ai-governance-framework.md)). |
| **Mitigation strategy** | Ongoing calibration/drift monitoring with alerting; feedback-loop retraining/tuning from realized outcomes; versioned models with evaluated, staged, reversible updates and rollback on regression ([ADR-0007 §8–9](../architecture/adr/0007-ai-governance-framework.md)). |
| **Owner** | AI Lead |
| **Status** | Open |

---

## Ownership Summary

| Owner role | Risks |
| --- | --- |
| **AI Lead** | RSK-05, RSK-06, RSK-07, RSK-13 |
| **Data Quality Lead** | RSK-01, RSK-04 |
| **Integration Lead** | RSK-02, RSK-03 |
| **Platform/SRE Lead** | RSK-08, RSK-10 |
| **Security Lead** | RSK-11 |
| **Architecture Lead** | RSK-09 |
| **Product/Compliance Lead** | RSK-12 |

---

## Governance & Review

- **Cadence.** The register is reviewed at each phase boundary and whenever a new material
  risk is identified; probabilities, severities, and statuses are updated with rationale.
- **Traceability.** Every mitigation references the ADR or policy that implements it, so the
  register stays synchronized with the architecture rather than drifting from it.
- **Status lifecycle.** Open → Mitigating (controls active/being built) → Monitored (accepted
  residual risk under watch). New risks are added with the next free `RSK-NN` id.
- **Metrics linkage.** Detection methods map to concrete measures in
  [Success Metrics](11-success-metrics.md) and the [Data Quality Policy](data-quality-policy.md#17-data-quality-metrics),
  plus the governance and security monitors in
  [ADR-0007](../architecture/adr/0007-ai-governance-framework.md) and
  [ADR-0008](../architecture/adr/0008-security-architecture.md).

---

## Related Documents

- [ADR-0007 — AI Governance Framework](../architecture/adr/0007-ai-governance-framework.md)
- [ADR-0008 — Security Architecture](../architecture/adr/0008-security-architecture.md)
- [ADR-0006 — Layer over systems of record](../architecture/adr/0006-layer-over-systems-of-record.md)
- [Data Quality Policy](data-quality-policy.md) · [Success Metrics](11-success-metrics.md) · [Business Workflow](09-business-workflow.md)
- [Agent Architecture](../architecture/13-agent-architecture.md) · [Agent Catalog](../agents/agent-catalog.md)
