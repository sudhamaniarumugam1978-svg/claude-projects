# Non-Functional Requirements (NFR / SLO Specification)

> **Purpose.** The **authoritative specification** for StockSense's measurable system
> qualities — the "-ilities" and service-level objectives (SLOs) that the implementation
> must satisfy. Where other documents describe *what* the system does, this document defines
> *how well* it must do it, in numbers that can be tested and monitored.

This specification operationalizes the quality commitments made in
[ADR-0007 (AI Governance)](adr/0007-ai-governance-framework.md),
[ADR-0008 (Security Architecture)](adr/0008-security-architecture.md), and
[ADR-0009 (Technology Stack)](adr/0009-technology-stack.md), and it quantifies the
"cross-cutting concerns" named in the [Agent Architecture §7](13-agent-architecture.md#7-cross-cutting-concerns-non-agent-system-wide).
Operational instrumentation of these targets is tracked in
[Success Metrics](../business/11-success-metrics.md).

---

## How to Read This Specification

- **Requirement ID** — stable identifier (`NFR-<AREA>-NN`) for cross-reference and testing.
- **Target** — the measurable objective. These are **baseline targets** for Phase 1; they
  are confirmed/tuned via load and resilience testing at Phase 1 kickoff. Semantics and the
  *existence* of a target are fixed here; exact numbers may be ratified per environment.
- **Measurement method** — how the value is computed/observed.
- **Monitoring approach** — how it is watched in production (tooling per
  [ADR-0009](adr/0009-technology-stack.md): OpenTelemetry + Prometheus + Grafana + Loki).
- **Owner** — the accountable role (roster consistent with the
  [Risk Register](../business/risk-register.md) and [Success Metrics](../business/11-success-metrics.md)).

**Scope definitions used below**
- **Core API** = the interactive request/response services users depend on (auth, reads,
  recommendation retrieval, decision actions).
- **Analysis pipeline** = asynchronous ingestion → data quality → forecast → risk →
  recommendation generation.
- **Interactive vs. generation latency** — *retrieving* prepared recommendations is
  interactive; *generating* forecasts/recommendations is pipeline work with its own targets.

> **Phase 0 status.** No target here is populated yet — the system is not built. This
> document defines the contract the Phase 1 implementation must meet and be measured against
> from day one.

---

## 1. Availability

| ID | Description | Target | Measurement Method | Monitoring Approach | Owner |
| --- | --- | --- | --- | --- | --- |
| NFR-AV-01 | Core API availability (monthly) | **≥ 99.9%** (≈ ≤ 43 min downtime/month) | Successful/total qualified requests over rolling 30 days | SLO dashboard + error-budget burn alerts (Prometheus/Grafana) | Platform/SRE Lead |
| NFR-AV-02 | Error budget policy | Feature rollout pauses when monthly error budget is exhausted | Budget = 1 − SLO; consumed vs. remaining | Automated burn-rate alerts (fast/slow) | Platform/SRE Lead |
| NFR-AV-03 | Analysis pipeline availability | **≥ 99.5%** of scheduled cycles complete on time | Completed-on-time cycles / scheduled cycles | Orchestrator job telemetry + alerting | Platform/SRE Lead |
| NFR-AV-04 | Planned maintenance | Zero-downtime deploys for Core API; maintenance windows announced | Deploy strategy audit (rolling/blue-green) | Deployment records (Argo CD) | Platform/SRE Lead |
| NFR-AV-05 | Dependency degradation | External-dependency outage (LLM/connector) must not take down Core API | Chaos/fault-injection test results | Dependency health + circuit-breaker metrics | Platform/SRE Lead |

## 2. Reliability

| ID | Description | Target | Measurement Method | Monitoring Approach | Owner |
| --- | --- | --- | --- | --- | --- |
| NFR-REL-01 | Core API error rate | **< 0.5%** 5xx over rolling 1h | 5xx / total requests | Error-rate alerts (Prometheus) | Platform/SRE Lead |
| NFR-REL-02 | Mean Time to Restore (MTTR), critical | **< 1 hour** | Σ restore time / incidents | Incident tracking; MTTR trend | Platform/SRE Lead |
| NFR-REL-03 | Change failure rate | **< 15%** of deployments | Failed-or-rolled-back deploys / total | CI/CD + incident correlation | Engineering Lead |
| NFR-REL-04 | Message processing guarantee | At-least-once delivery; **idempotent** consumers; no lost/duplicated decisions | Contract tests + reconciliation checks | Queue depth, DLQ, redelivery metrics (RabbitMQ) | Platform/SRE Lead |
| NFR-REL-05 | Graceful degradation | On sub-component failure, fail safe (read-only / last-known-good, clearly labeled) — never emit unsafe output | Fault-injection test outcomes | Degradation-mode telemetry + alerts | Platform/SRE Lead |
| NFR-REL-06 | Data freshness on stall | A stalled feed is flagged (not treated as "zero demand") within its SLA | Freshness watermark vs. SLA | Per-source freshness board | Integration Lead |

## 3. Performance

| ID | Description | Target | Measurement Method | Monitoring Approach | Owner |
| --- | --- | --- | --- | --- | --- |
| NFR-PERF-01 | Core API read latency | **p95 < 300 ms, p99 < 800 ms** | Percentile of server-side duration | Latency histograms (OTel/Prometheus) | Platform/SRE Lead |
| NFR-PERF-02 | Core API write/action latency | **p95 < 500 ms, p99 < 1.2 s** | Percentile of server-side duration | Latency histograms | Platform/SRE Lead |
| NFR-PERF-03 | Recommendation **retrieval** latency (interactive) | **p95 < 2 s** to load the ranked, explained brief | End-to-end request timing | Endpoint latency dashboard | Product Lead + Platform/SRE Lead |
| NFR-PERF-04 | Recommendation **generation** latency (pipeline) | Per-tenant daily cycle completes **< 15 min** for a typical catalog (≤ ~50k SKUs); incremental refresh **< 5 min** | Orchestrator stage timing | Pipeline latency per stage | AI Lead + Platform/SRE Lead |
| NFR-PERF-05 | Forecast generation latency | Full-catalog forecast batch **< 30 min** (≤ ~50k SKUs); incremental **< 5 min** | Forecast Agent job timing | Job-duration metrics + alerts | AI Lead |
| NFR-PERF-06 | Data ingestion → analysis-ready | POS event available to analysis **< 10 min** (near-real-time tier) | Watermark: ready_time − arrival_time | Pipeline freshness metric (ENG-04) | Platform/SRE Lead |
| NFR-PERF-07 | LLM narration latency (explanation) | **p95 < 5 s** per generated explanation (cacheable) | LLM call timing (via abstraction) | Provider latency metrics | AI Lead |
| NFR-PERF-08 | UI initial render | First meaningful render **< 2.5 s** on a typical connection | Web vitals (LCP) | RUM/synthetic checks | Engineering Lead |

## 4. Scalability

| ID | Description | Target | Measurement Method | Monitoring Approach | Owner |
| --- | --- | --- | --- | --- | --- |
| NFR-SCAL-01 | Ingestion throughput | Sustain **≥ 1,000,000 POS events/hour** aggregate with headroom | Load test at peak profile | Throughput vs. capacity dashboard (ENG-05) | Platform/SRE Lead |
| NFR-SCAL-02 | Concurrent users | Support **≥ 5,000 concurrent active users** within latency SLOs | Load test to target concurrency | Active-session + latency correlation | Platform/SRE Lead |
| NFR-SCAL-03 | Catalog scale per tenant | Handle tenants up to **~100k SKUs** within generation SLOs | Scale test with large synthetic catalog | Per-tenant duration trends | AI Lead |
| NFR-SCAL-04 | Horizontal elasticity | Stateless services autoscale on load; no single-node bottleneck | Autoscaling test under ramp | HPA metrics; saturation signals | Platform/SRE Lead |
| NFR-SCAL-05 | Multi-tenant growth | Linear-ish cost/latency as tenants grow; scale-out path defined for data tier | Capacity model + trend | Cost-per-tenant (OPS-08) + latency | Platform/SRE Lead |
| NFR-SCAL-06 | Vector-store scale trigger | Defined thresholds (recall/latency/volume) trigger pgvector → Qdrant migration | Threshold monitoring | Vector query latency/recall dashboard | AI Lead |

## 5. Security

Security NFRs quantify [ADR-0008](adr/0008-security-architecture.md). See that ADR for the
full control set; the targets below are the measurable commitments.

| ID | Description | Target | Measurement Method | Monitoring Approach | Owner |
| --- | --- | --- | --- | --- | --- |
| NFR-SEC-01 | Encryption in transit | **100%** of traffic over TLS 1.2+ (prefer 1.3); HTTP refused/redirected | Config/endpoint scan | TLS posture scan; HSTS checks | Security Lead |
| NFR-SEC-02 | Encryption at rest | **100%** of datastores, backups, and audit logs encrypted (AES-256, managed KMS) | Storage config audit | KMS/config drift alerts | Security Lead |
| NFR-SEC-03 | Tenant isolation | **Zero** cross-tenant data access; enforced at data layer (RLS) | Automated isolation test suite (CI gate) | Authz-denial + anomaly monitoring | Security Lead |
| NFR-SEC-04 | Authentication | OIDC/OAuth2; **MFA required** for privileged roles; short-lived JWT + rotating revocable refresh | Auth config + policy audit | Auth success/failure, token-reuse alerts | Security Lead |
| NFR-SEC-05 | Access control | RBAC + tenant scoping, **deny-by-default** | Authz policy tests | Authz-denial spikes | Security Lead |
| NFR-SEC-06 | Rate limiting | Per-identity/tenant/IP limits; stricter on auth endpoints; standard 429 + `Retry-After` | Rate-limit config test | 429 rate + abuse alerts | Platform/SRE Lead |
| NFR-SEC-07 | Vulnerability management | **Critical** vulns patched ≤ 7 days; **High** ≤ 30 days | Dependency/image/IaC scan results | CI scan gates + tracking | Security Lead |
| NFR-SEC-08 | Secrets hygiene | **Zero** secrets in source/images/logs; rotation enforced | CI secret scanning; rotation audit | Secret-access anomaly alerts | Security Lead |
| NFR-SEC-09 | Security event capture | 100% of auth/authz/secret-access/config-change events logged (immutable) | Audit-log completeness check | Log-completeness monitor | Security Lead |

## 6. Maintainability

| ID | Description | Target | Measurement Method | Monitoring Approach | Owner |
| --- | --- | --- | --- | --- | --- |
| NFR-MNT-01 | Automated test coverage | **≥ 80%** on core decision/agent logic | Coverage report | CI coverage trend (ENG-06) | Engineering Lead |
| NFR-MNT-02 | Deployment lead time | Median commit → prod **< 1 day** | VCS + CI/CD timestamps | DORA lead-time dashboard | Engineering Lead |
| NFR-MNT-03 | Contract-first agents | 100% inter-agent messages validated against versioned schemas | Contract tests in CI | Schema-violation alerts | Engineering Lead |
| NFR-MNT-04 | Provider abstraction | LLM, embeddings, vector store, object storage, and secrets are swappable behind interfaces | Architecture conformance review | Dependency-coupling checks | Architecture Lead |
| NFR-MNT-05 | Reproducible builds | Deterministic dependency resolution (lockfiles: uv, pnpm) | Build reproducibility check | CI build integrity | Engineering Lead |
| NFR-MNT-06 | Documentation currency | ADRs/architecture updated with material design changes; cross-links valid | Doc review at phase/change gates | Link-check in CI | Architecture Lead |

## 7. Observability

| ID | Description | Target | Measurement Method | Monitoring Approach | Owner |
| --- | --- | --- | --- | --- | --- |
| NFR-OBS-01 | Distributed tracing | **100%** of decisions carry an end-to-end `trace_id` (raw data → recommendation → decision) | Trace-coverage audit | Tracing backend (Tempo/Jaeger) | Platform/SRE Lead |
| NFR-OBS-02 | Structured logging | 100% structured (JSON) logs with correlation IDs; no secrets/PII in logs | Log-format lint + sampling | Loki queries + PII scans | Platform/SRE Lead |
| NFR-OBS-03 | Metrics coverage | Every service exports health, latency, error, and saturation metrics | Metrics-coverage audit | Prometheus targets up% | Platform/SRE Lead |
| NFR-OBS-04 | Alerting signal quality | Actionable alert ratio **≥ 90%** (avoid fatigue) | Alert disposition review | Actionable-vs-noise trend (OPS-09) | Platform/SRE Lead |
| NFR-OBS-05 | Decision traceability on demand | Any recommendation can produce a full provenance trail | Spot-audit reconstruction | Trace/audit linkage checks | AI Lead |
| NFR-OBS-06 | Governance/AI monitors | Calibration, hallucination-violation, and drift monitors active in prod | Monitor liveness check | Governance dashboards (ADR-0007) | AI Lead |

## 8. Disaster Recovery

Quantifies [ADR-0008 §18, §20](adr/0008-security-architecture.md).

| ID | Description | Target | Measurement Method | Monitoring Approach | Owner |
| --- | --- | --- | --- | --- | --- |
| NFR-DR-01 | Recovery Point Objective (RPO) | **≤ 15 min** for transactional data | Backup/replication lag measurement | Replication-lag + PITR window monitor | Platform/SRE Lead |
| NFR-DR-02 | Recovery Time Objective (RTO), critical services | **≤ 1 hour** | DR drill timing | DR runbook drill records | Platform/SRE Lead |
| NFR-DR-03 | Regional/provider failover RTO | **≤ 4 hours** | Failover drill timing | Failover drill records | Platform/SRE Lead |
| NFR-DR-04 | Backup frequency | DB: continuous WAL/PITR + **daily** full snapshots; audit log: continuous; object store: versioned | Backup job success logs | Backup success calendar (OPS-07) | Platform/SRE Lead |
| NFR-DR-05 | Backup encryption & isolation | 100% encrypted; **3-2-1** with ≥1 isolated off-account copy | Backup config audit | Backup integrity checks | Platform/SRE Lead |
| NFR-DR-06 | Restore verification | Restore tests **pass** on a **monthly/quarterly** schedule within RTO | Scheduled restore-test results | Restore-test pass/fail log | Platform/SRE Lead |

## 9. Data Integrity

Quantifies the [Data Quality Policy](../business/data-quality-policy.md) and the data
protections in [ADR-0007](adr/0007-ai-governance-framework.md).

| ID | Description | Target | Measurement Method | Monitoring Approach | Owner |
| --- | --- | --- | --- | --- | --- |
| NFR-DI-01 | Data quality gate | Data must reach **High band (`data_quality_score` ≥ 0.80)** to flow to analysis normally; **Low band (< 0.50)** is quarantined | Data Quality pipeline scoring | Quality-score + band distribution (OPS-01) | Data Quality Lead |
| NFR-DI-02 | Quarantine over corruption | Impossible values (negative stock, impossible sales) **flagged/quarantined**, never silently trusted | Validation-rule outcomes | Quarantine rate + reasons (OPS-04) | Data Quality Lead |
| NFR-DI-03 | Idempotent ingestion | Re-ingestion does not duplicate records/quantities | De-dup/reconciliation tests | Duplicate-rate metric | Integration Lead |
| NFR-DI-04 | Audit log immutability | Audit records are append-only and **tamper-evident** | Integrity/hash-chain verification | Tamper-evidence checks | Security Lead |
| NFR-DI-05 | Audit log retention | Retain **≥ 13 months online**; long-term archive per retention policy (configurable for compliance) | Retention config audit | Retention-policy monitor | Security Lead |
| NFR-DI-06 | Backup consistency | Restores produce a consistent, tenant-isolated dataset | Restore-validation checks | Restore-test data validation | Platform/SRE Lead |
| NFR-DI-07 | Non-destructive processing | Raw source data is never mutated in place; corrections are derived and logged | Pipeline design conformance | Correction/annotation audit | Data Quality Lead |

## 10. AI Service Quality

Quantifies [ADR-0004 (Explainable AI)](adr/0004-explainable-ai-mandate.md) and
[ADR-0007 (AI Governance)](adr/0007-ai-governance-framework.md). Accuracy KPIs (WMAPE,
precision/recall, outcome accuracy) live in
[Success Metrics §2](../business/11-success-metrics.md#2-ai-performance-kpis); the items
below are the *service-quality* guarantees.

| ID | Description | Target | Measurement Method | Monitoring Approach | Owner |
| --- | --- | --- | --- | --- | --- |
| NFR-AIQ-01 | Explanation completeness | **100%** of recommendations carry all four mandatory elements (reasoning, confidence, evidence, impact) or are not emitted | Recommendation-boundary validation | Completeness gauge (AI-08); violations block | AI Lead |
| NFR-AIQ-02 | Hallucination / grounding | **~0%** ungrounded or numerically-inconsistent outputs reach users | Grounding + numeric-integrity checks | Violation control chart (AI-10) | AI Lead |
| NFR-AIQ-03 | Confidence calibration | Expected Calibration Error (ECE) below threshold; **80% confidence ≈ 80% success** | ECE vs. realized outcomes | Reliability diagram + alerts (AI-03) | AI Lead |
| NFR-AIQ-04 | Confidence banding behavior | **Low-band (< 0.50)** outputs never emitted as recommendations; **Medium (0.50–0.79)** flagged uncertain; **High (≥ 0.80)** primary | Band-routing tests | Band distribution monitor | AI Lead |
| NFR-AIQ-05 | Model response timeout | LLM calls time out at **≤ 30 s** with retry/fallback via provider abstraction; timeouts degrade gracefully (no fabrication) | Call-timeout instrumentation | Timeout/fallback rate metrics | AI Lead |
| NFR-AIQ-06 | Forecast confidence attached | **100%** of forecasts carry a calibrated confidence/interval | Output-contract validation | Contract-conformance monitor | AI Lead |
| NFR-AIQ-07 | Model drift control | Drift below alert threshold; breach triggers evaluation/rollback | Rolling WMAPE / PSI vs. baseline | Drift dashboard + alerts (AI-11) | AI Lead |
| NFR-AIQ-08 | Model/prompt versioning | **100%** of AI outputs record model + prompt version (reproducible, reversible) | Output metadata audit | Version-stamp completeness | AI Lead |
| NFR-AIQ-09 | Human-in-the-loop | **0** default autonomous executions; every material action is human-decided | Workflow conformance test | Action-path audit | Product Lead |

---

## Cross-Cutting Notes

- **Targets are baselines.** Every numeric target above is an initial commitment to be
  validated by load, chaos, and DR testing during Phase 1; adjustments are recorded here as
  the authoritative source (with change history).
- **Environments.** SLOs apply to production. Non-prod environments have relaxed targets but
  the **same** security, data-integrity, and governance requirements.
- **Anti-gaming.** Performance targets are balanced against correctness/governance (e.g.,
  NFR-AIQ-05 timeouts degrade honestly rather than fabricate; NFR-PERF is never met by
  skipping explanation/validation).

## Traceability

| This NFR area | Governed / measured by |
| --- | --- |
| Availability, Reliability, Performance, Scalability, Observability, DR | [Success Metrics §3 Engineering & §4 Operational](../business/11-success-metrics.md); [ADR-0009](adr/0009-technology-stack.md) |
| Security | [ADR-0008](adr/0008-security-architecture.md); [Risk Register](../business/risk-register.md) (RSK-11) |
| Data Integrity | [Data Quality Policy](../business/data-quality-policy.md); [ADR-0007](adr/0007-ai-governance-framework.md) |
| AI Service Quality | [ADR-0004](adr/0004-explainable-ai-mandate.md), [ADR-0007](adr/0007-ai-governance-framework.md); [Success Metrics §2 AI](../business/11-success-metrics.md#2-ai-performance-kpis) |

## Governance & Review

- **Authority.** This document is the single source of truth for measurable system
  qualities. Conflicting numbers elsewhere defer to this specification.
- **Review cadence.** Reviewed at each phase boundary and whenever an SLO is breached or a
  target is re-ratified; changes are versioned with rationale.
- **Ownership roster** mirrors the [Risk Register](../business/risk-register.md) and
  [Success Metrics owner roster](../business/11-success-metrics.md#owner-roster-summary).

## Related Documents

- [Agent Architecture](13-agent-architecture.md) · [Agent Catalog](../agents/agent-catalog.md)
- [ADR-0004](adr/0004-explainable-ai-mandate.md) · [ADR-0007](adr/0007-ai-governance-framework.md) · [ADR-0008](adr/0008-security-architecture.md) · [ADR-0009](adr/0009-technology-stack.md) · [ADR-0010](adr/0010-multi-agent-architecture-rationale.md)
- [Data Quality Policy](../business/data-quality-policy.md) · [Success Metrics](../business/11-success-metrics.md) · [Risk Register](../business/risk-register.md)
