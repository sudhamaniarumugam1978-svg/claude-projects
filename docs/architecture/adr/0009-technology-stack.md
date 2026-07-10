# ADR-0009 — Technology Stack Selection

- **Status:** Accepted (frozen for Phase 1)
- **Date:** Phase 0 → Phase 1 boundary
- **Deciders:** Architecture, Engineering, AI, Platform/SRE, Security & Privacy

## Context

Phase 0 deliberately left the implementation stack open — the
[Agent Architecture](../13-agent-architecture.md#9-open-architectural-questions-deferred-to-phase-1-design)
and [Repository Planning](../../planning/15-repository-planning.md#3-planned-code-structure-phase-1--not-yet-created)
both state that language, frameworks, and deployment shape would be settled via an ADR "at
the start of Phase 1." This ADR is that decision. Its objective is to **finalize and freeze
the technology stack** so Phase 1 begins with a single, agreed implementation standard
rather than per-service improvisation.

The stack must serve a specific product: a **multi-tenant, AI-driven, multi-agent Decision
Intelligence Engine** ([ADR-0005](0005-multi-agent-orchestration.md)) that is
explainable ([ADR-0004](0004-explainable-ai-mandate.md)), governed
([ADR-0007](0007-ai-governance-framework.md)), secure
([ADR-0008](0008-security-architecture.md)), and layered over external systems of record
([ADR-0006](0006-layer-over-systems-of-record.md)). It must be affordable for a lean team
serving cost-sensitive retailers, avoid crippling vendor lock-in
([Risk Register RSK-09](../../business/risk-register.md)), and be operable without a large
platform team in V1.

## Stack-Wide Decision Principles

Every selection below is judged against these, in priority order:

1. **Fit the mission.** AI/ML-heavy → a Python-first core; explainability/governance →
   frameworks that expose state and traceability.
2. **Security & governance alignment.** Must support tenant isolation, encryption, secrets,
   and auditability (ADR-0007/0008) natively.
3. **Portability over lock-in.** Prefer open standards and self-hostable components so we
   can move clouds/providers; isolate unavoidable provider coupling behind abstractions.
4. **Minimize operational surface in V1, scale out later.** Reuse one system for two jobs
   where safe (e.g., Postgres for relational + vector), split when scale demands.
5. **Managed where failure is catastrophic** (keys, secrets, primary DB); **self-managed
   where cost/portability dominates** (observability).
6. **Team velocity & hiring.** Mainstream, well-documented, widely-known tools beat clever
   niche ones.

> **Freeze scope.** This ADR freezes *technology choices*. Exact version pinning, sizing,
> and the deployment/tenancy topology are Phase 1 kickoff tasks that must conform to these
> choices.

---

## Decisions (per technology)

Each decision states: **Why · Alternatives · Trade-offs · Scalability · Cost · Learning
curve · Long-term maintainability.**

### 1. Frontend — **React + TypeScript (Next.js)**
- **Why:** Largest ecosystem and talent pool; TypeScript gives type safety for a data-dense
  decision UI; Next.js provides routing, SSR/streaming for fast first render, and a mature
  build pipeline. Fits "insight over charts" — a responsive app, not a BI tool.
- **Alternatives:** Vue/Nuxt (smaller ecosystem), Angular (heavier, steeper), SvelteKit
  (leaner but smaller community/hiring).
- **Trade-offs:** React boilerplate and churn vs. unmatched ecosystem/hiring; Next.js adds
  framework opinions we accept for velocity.
- **Scalability:** Scales as a stateless static/SSR frontend behind a CDN; component model
  scales with team size.
- **Cost:** Open source; hosting is cheap (static/edge). No licensing.
- **Learning curve:** Low–moderate; ubiquitous skills.
- **Maintainability:** High — huge community, long-term support, easy to staff.

### 2. Backend — **Python + FastAPI**
- **Why:** Python is the lingua franca of AI/ML and forecasting (scikit-learn, statsmodels,
  Prophet/StatsForecast) and of LLM SDKs, so the decision engine and its API share one
  language. FastAPI is async, high-performance, and Pydantic-typed with **auto-generated
  OpenAPI** (see #19).
- **Alternatives:** Node.js/NestJS (splits language from the ML core), Go (fast but weaker
  ML ecosystem), Java/Spring (heavyweight for a lean team).
- **Trade-offs:** Python's raw throughput and GIL are weaker than Go/JVM — mitigated by
  async I/O, horizontal scaling, and pushing hot numeric paths into vectorized libraries.
- **Scalability:** Stateless services scale horizontally; async handles I/O-bound
  integration/LLM calls well.
- **Cost:** Open source; efficient enough that compute cost is dominated by AI inference,
  not the web tier.
- **Learning curve:** Low; Python + FastAPI is fast to onboard.
- **Maintainability:** High — one language across API and AI reduces context-switching;
  typed models keep contracts honest.

### 3. Database — **PostgreSQL**
- **Why:** Rock-solid relational core with JSONB flexibility; **row-level security (RLS)**
  directly supports mandatory tenant isolation ([ADR-0008 §9](0008-security-architecture.md));
  rich extensions — **TimescaleDB** for sales time-series and **pgvector** for embeddings
  (#9) — let us serve several needs from one trusted engine (principle 4).
- **Alternatives:** MySQL (weaker extensions/JSON), SQL Server (licensing, Microsoft-centric),
  MongoDB (loses relational integrity our joins need).
- **Trade-offs:** A single relational store is not infinitely scalable for every workload;
  we accept that and split specialized workloads out only when metrics demand.
- **Scalability:** Vertical + read replicas; partitioning and Timescale for time-series;
  managed (e.g., RDS/Aurora) for HA. Extremely high ceiling before sharding is needed.
- **Cost:** Open source; managed hosting is predictable and mid-range.
- **Learning curve:** Low; SQL is universal.
- **Maintainability:** High — mature tooling, migrations, and a deep operational knowledge
  base.

### 4. Cache — **Redis (Valkey-compatible)**
- **Why:** Versatile in-memory store for caching, session/token denylists, rate limiting
  ([ADR-0008 §10](0008-security-architecture.md)), and ephemeral coordination. Mature and
  ubiquitous. We standardize on the **open-source Valkey fork** to avoid the recent Redis
  licensing shift while keeping full API compatibility.
- **Alternatives:** Memcached (cache-only, no data structures), KeyDB (smaller community),
  in-process caches (don't share across instances).
- **Trade-offs:** In-memory means volatility; we treat it as a cache, not a source of truth.
- **Scalability:** Clustering and replicas; managed offerings scale easily.
- **Cost:** Open source; memory-priced hosting, modest at our scale.
- **Learning curve:** Low.
- **Maintainability:** High; one caching technology for many jobs reduces sprawl.

### 5. Message Queue — **RabbitMQ**
- **Why:** Reliable brokered messaging for inter-agent events and asynchronous work
  (ingestion, analysis fan-out) under the Orchestrator's control. Rich routing, acks, and
  dead-letter queues fit a pipeline that must be **traceable and reliable** (no lost or
  double-processed decisions).
- **Alternatives:** Apache Kafka (superb for high-volume streaming/event-sourcing but heavy
  to operate — kept as the scale path for large POS event volumes), Redis Streams (simpler
  but fewer delivery guarantees), cloud SQS (managed but provider-coupled).
- **Trade-offs:** Another stateful system to operate; less throughput than Kafka at extreme
  scale — acceptable for V1, revisit at high event volumes.
- **Scalability:** Clustered/quorum queues; managed options available. Kafka is the
  documented upgrade if streaming volume outgrows it.
- **Cost:** Open source; modest hosting.
- **Learning curve:** Moderate; well-documented patterns.
- **Maintainability:** Good; mature and stable. Abstract publish/consume so a future Kafka
  swap is contained.

### 6. AI Framework — **LangGraph (agent orchestration) + Python ML stack**
- **Why:** LangGraph models agents as an explicit **graph of stateful nodes**, which maps
  directly onto our Orchestrator + typed message-envelope design and makes state,
  provenance, and control flow inspectable — essential for **traceability and
  explainability** ([ADR-0004](0004-explainable-ai-mandate.md), [ADR-0007](0007-ai-governance-framework.md)).
  Forecasting/ML uses the proven Python scientific stack (**StatsForecast/Prophet,
  scikit-learn, statsmodels**) so method choice can respect data density
  ([Agent Catalog](../../agents/agent-catalog.md)).
- **Alternatives:** Bare LangChain (less explicit control flow), LlamaIndex (retrieval-first,
  narrower), AutoGen/CrewAI (conversational-agent oriented, less deterministic control), a
  fully custom framework (maximum control, higher build cost).
- **Trade-offs:** Framework churn is real in this space; we wrap it behind our own agent
  interfaces so the engine is not hostage to any one library.
- **Scalability:** Orchestration scales with the backend; heavy compute is the LLM/forecast
  calls, scaled independently.
- **Cost:** Open source; cost is the underlying inference (#7).
- **Learning curve:** Moderate; graph model is intuitive but the ecosystem moves fast.
- **Maintainability:** Good if isolated behind our abstractions; explicit graphs are easier
  to reason about and test than free-form agent loops.

### 7. LLM Provider — **Anthropic Claude (behind a provider abstraction)**
- **Why:** Strong reasoning, instruction-following, and reliable **structured/grounded
  output** — exactly what explanation-first, hallucination-averse recommendations need
  ([ADR-0007](0007-ai-governance-framework.md)). Accessed through an internal
  provider-abstraction layer so models are pinned/versioned and swappable
  ([ADR-0007 §9](0007-ai-governance-framework.md#9-model-version-tracking)), mitigating
  vendor dependency ([RSK-09](../../business/risk-register.md)).
- **Alternatives:** OpenAI (strong, comparable — retained as a first-class fallback via the
  abstraction), Google Gemini, self-hosted open models (Llama/Mistral — lower unit cost, far
  higher ops burden; a future cost lever).
- **Trade-offs:** External dependency and per-token cost vs. avoiding the cost/complexity of
  self-hosting; addressed by abstraction + caching + using the LLM only for narrative, never
  for the numbers (which come from the deterministic pipeline).
- **Scalability:** Managed API scales elastically; concurrency governed by budget and rate
  limits.
- **Cost:** Usage-based and the largest variable cost; controlled via prompt discipline,
  caching, model-tier selection, and Low-band withholding.
- **Learning curve:** Low SDK integration; moderate prompt/governance discipline (#6, ADR-0007).
- **Maintainability:** High if the abstraction is respected; provider swaps stay contained.

### 8. Embedding Model — **Voyage AI (primary) with open-source fallback**
- **Why:** Anthropic does not offer first-party embeddings and recommends Voyage; Voyage
  models are strong and cost-effective for retrieval/grounding (#9). Kept behind the same
  provider abstraction as #7.
- **Alternatives:** OpenAI `text-embedding-3` (excellent; alternate managed option),
  Cohere Embed, self-hosted open models (**BGE / E5 via sentence-transformers**) for
  zero-marginal-cost/on-prem — retained as the cost/portability fallback.
- **Trade-offs:** Managed embeddings add a dependency and per-call cost vs. self-hosting's
  ops burden; abstraction makes switching cheap.
- **Scalability:** Managed API scales; embeddings are cached and recomputed only on change.
- **Cost:** Low relative to generation; batch + cache to minimize.
- **Learning curve:** Low.
- **Maintainability:** High; abstraction + caching isolate the choice.

### 9. Vector Database — **pgvector (V1), Qdrant (scale path)**
- **Why:** Starting with **pgvector** reuses PostgreSQL (principle 4): one datastore, one
  backup/security model, inherited tenant isolation — no new system to secure or operate for
  V1's moderate embedding volumes.
- **Alternatives:** Qdrant (open-source, high-performance — the documented scale-out target),
  Weaviate, Milvus, Pinecone (managed, fast to start but provider-coupled and priced per
  scale).
- **Trade-offs:** pgvector's performance ceiling is lower than a dedicated engine; we accept
  that for V1 and migrate to Qdrant when recall/latency/volume metrics require, behind a
  retrieval abstraction.
- **Scalability:** pgvector scales to substantial sizes with proper indexing; Qdrant scales
  horizontally beyond that.
- **Cost:** pgvector adds ~nothing (reuses Postgres); dedicated DBs add infra/managed cost.
- **Learning curve:** Low (it's Postgres); Qdrant moderate later.
- **Maintainability:** High initially (fewer systems); planned, contained migration path.

### 10. Authentication — **Keycloak (OIDC/OAuth2)**
- **Why:** Open-source, self-hostable identity provider implementing the OIDC/OAuth2 + MFA +
  SSO federation standards mandated by [ADR-0008 §1–3](0008-security-architecture.md).
  Avoids per-MAU pricing that scales painfully with a multi-tenant SMB base, and keeps
  identity portable (no lock-in).
- **Alternatives:** Auth0/Okta or AWS Cognito (managed, lower ops but per-user cost and
  lock-in — retained as the option if ops load outweighs savings), Clerk/Supabase Auth
  (great DX, less enterprise SSO depth), building our own (rejected — bespoke auth is a
  classic vulnerability source, per [ADR-0008](0008-security-architecture.md)).
- **Trade-offs:** Operational responsibility for a security-critical service vs. cost control
  and portability. We accept the ops cost and harden it; standards-compliance keeps a managed
  swap feasible.
- **Scalability:** Clustered Keycloak scales to large user bases; stateless token validation
  scales in services.
- **Cost:** Open source; only infra cost — flat vs. per-user managed pricing.
- **Learning curve:** Moderate–high (Keycloak configuration).
- **Maintainability:** Good; standards-based so identity is portable, but requires security
  patching discipline.

### 11. Cloud Platform — **AWS**
- **Why:** Broadest, most mature managed-service catalog (RDS/Aurora, ElastiCache, S3, EKS,
  KMS, Secrets Manager), largest talent pool, and strong security/compliance posture
  supporting ADR-0008. We keep workloads **cloud-portable** (containers + Terraform) to blunt
  lock-in.
- **Alternatives:** GCP (excellent data/ML, smaller enterprise footprint), Azure (strong for
  Microsoft-centric orgs), multi-cloud from day one (needless complexity for V1).
- **Trade-offs:** Deepest managed services create some gravitational lock-in; mitigated by
  portable compute/IaC and provider abstractions.
- **Scalability:** Effectively unlimited managed scaling.
- **Cost:** Pay-as-you-go; managed convenience carries a premium — controlled by
  right-sizing, autoscaling, and cost monitoring ([OPS-08](../../business/11-success-metrics.md)).
- **Learning curve:** Moderate; widely known.
- **Maintainability:** High; managed services reduce undifferentiated ops.

### 12. Object Storage — **Amazon S3 (S3-compatible abstraction)**
- **Why:** Durable, cheap, virtually infinite storage for CSV uploads, backups
  ([ADR-0008 §18](0008-security-architecture.md)), model artifacts, and exports; the de-facto
  standard API. Encryption-at-rest and access controls satisfy ADR-0008.
- **Alternatives:** GCS/Azure Blob (equivalent, other clouds), **MinIO** (S3-compatible,
  self-hostable — used for local/dev and as an on-prem escape hatch).
- **Trade-offs:** AWS coupling — mitigated by coding to the S3 API so MinIO/other clouds
  work unchanged.
- **Scalability:** Essentially unlimited.
- **Cost:** Very low per GB; lifecycle policies control long-term cost.
- **Learning curve:** Low.
- **Maintainability:** High; the S3 API is a stable, universal standard.

### 13. Monitoring — **OpenTelemetry + Prometheus + Grafana**
- **Why:** **OpenTelemetry** is the vendor-neutral instrumentation standard (metrics + traces),
  future-proofing us against tool lock-in; **Prometheus** stores metrics; **Grafana**
  visualizes and alerts. Traces via **Tempo/Jaeger** carry the `trace_id` that underpins
  decision traceability ([ADR-0007 §10](0007-ai-governance-framework.md)).
- **Alternatives:** Datadog/New Relic (superb managed all-in-one, but cost scales sharply and
  couples us — retained as an option if self-managed ops become a burden), AWS CloudWatch
  (convenient, AWS-coupled).
- **Trade-offs:** Self-managed observability is operational work vs. managed convenience/cost.
- **Scalability:** Prometheus (with remote-write/Thanos/Mimir) and Grafana scale to large
  fleets.
- **Cost:** Open source; infra cost only — materially cheaper than per-host managed tools at
  scale.
- **Learning curve:** Moderate.
- **Maintainability:** High; OTel means instrumentation survives backend swaps.

### 14. Logging — **Structured logging → Grafana Loki**
- **Why:** JSON structured logs with correlation/`trace_id` (ties logs to the audit and
  decision trace, ADR-0007) shipped to **Loki**, which pairs with Grafana for a single pane of
  glass alongside metrics/traces and is cost-efficient (indexes labels, not full text).
- **Alternatives:** ELK/OpenSearch (powerful full-text search, heavier and pricier to run —
  the option if deep log search is needed), Datadog/CloudWatch Logs (managed, cost/lock-in).
- **Trade-offs:** Loki's label-based indexing is less flexible than full-text search; adequate
  for structured logs and far cheaper.
- **Scalability:** Horizontally scalable, object-storage-backed (uses S3, #12).
- **Cost:** Open source; low storage cost on S3.
- **Learning curve:** Low–moderate.
- **Maintainability:** High; cohesive with the monitoring stack.

### 15. CI/CD — **GitHub Actions + Argo CD (GitOps)**
- **Why:** The repository is on GitHub, so **GitHub Actions** is zero-friction for build/test/
  scan pipelines (including the security and unsafe-SQL gates from
  [ADR-0008](0008-security-architecture.md) and prompt/model eval gates from
  [ADR-0007](0007-ai-governance-framework.md)). **Argo CD** provides declarative **GitOps**
  deployment to Kubernetes (git as the single source of deployment truth — auditable and
  reversible).
- **Alternatives:** GitLab CI (needs GitLab), Jenkins (heavy, self-managed), CircleCI
  (external), pushing deploys from CI without GitOps (less auditable).
- **Trade-offs:** GitHub Actions couples CI to GitHub (acceptable — that's our SCM); Argo adds
  a component but yields auditable, reversible deploys aligned with our governance ethos.
- **Scalability:** Both scale to many services/environments.
- **Cost:** Actions has a usable free tier then usage pricing; Argo is open source.
- **Learning curve:** Actions low; Argo/GitOps moderate.
- **Maintainability:** High; declarative pipelines and GitOps are self-documenting.

### 16. Containerization — **Docker + Kubernetes (managed, EKS)**
- **Why:** **Docker** images are the universal build/runtime unit; **Kubernetes** gives
  portable, self-healing orchestration and clean scaling of independent agents/services
  ([ADR-0005](0005-multi-agent-orchestration.md)). Managed K8s (EKS) offloads control-plane
  ops. Portability is itself a lock-in hedge (principle 3).
- **Alternatives:** AWS ECS/Fargate (simpler, less to learn, but AWS-coupled — a reasonable
  V1 simplification), Docker Compose (dev only), Nomad (smaller ecosystem).
- **Trade-offs:** K8s has real complexity and a learning curve for a lean team; we accept it
  for portability and scale, and **may run a reduced K8s footprint (or start on Fargate) in
  early V1**, converging on the standard as load grows.
- **Scalability:** Excellent — horizontal pod autoscaling, multi-AZ.
- **Cost:** Managed control plane + nodes; right-sizing and autoscaling control spend.
- **Learning curve:** High (the biggest in this stack) — mitigated by managed K8s and IaC.
- **Maintainability:** High once established; portable and industry-standard, easy to staff.

### 17. Infrastructure as Code — **Terraform / OpenTofu**
- **Why:** Declarative, provider-rich, mature IaC to make all cloud infra reproducible,
  reviewable, and versioned. We standardize on **OpenTofu** (the open-source fork) to avoid
  the HashiCorp BSL licensing change while retaining Terraform compatibility and ecosystem.
- **Alternatives:** Pulumi (real languages — nice, smaller community), AWS CDK/CloudFormation
  (AWS-only, undercuts portability), Ansible (config management, not infra provisioning).
- **Trade-offs:** HCL is its own language and state management needs discipline; the payoff is
  reproducible, auditable infrastructure.
- **Scalability:** Modules scale to large, multi-environment estates.
- **Cost:** Open source; only state-backend storage.
- **Learning curve:** Moderate.
- **Maintainability:** High; infra changes get the same review rigor as code.

### 18. Testing Framework — **pytest (backend) · Vitest + React Testing Library + Playwright (frontend/E2E) · AI evals**
- **Why:** **pytest** is the Python standard (fixtures, rich plugins) for the backend and
  agents; **Vitest + RTL** for fast frontend unit/component tests; **Playwright** for reliable
  cross-browser E2E. A dedicated **AI evaluation suite** provides the regression gates that
  ADR-0007 requires for prompt/model changes.
- **Alternatives:** unittest (barer), Jest (fine; Vitest is faster with Vite), Cypress
  (good E2E; Playwright has broader browser support).
- **Trade-offs:** Multiple tools across tiers vs. best-in-class per tier; AI evals are
  non-deterministic and need thoughtful, tolerance-based assertions.
- **Scalability:** All parallelize in CI.
- **Cost:** Open source.
- **Learning curve:** Low–moderate.
- **Maintainability:** High; mainstream tools with strong docs. Tests are first-class per
  engineering KPIs ([ENG-06](../../business/11-success-metrics.md)).

### 19. API Documentation — **OpenAPI (auto-generated by FastAPI) + Swagger UI / Redoc**
- **Why:** FastAPI generates an **OpenAPI** spec from typed Pydantic models automatically, so
  docs stay in sync with code by construction; rendered via Swagger UI (interactive) and Redoc
  (readable). The spec also drives client generation and contract testing.
- **Alternatives:** Hand-written docs (drift-prone), Postman collections (not a source of
  truth), Stoplight (extra tooling).
- **Trade-offs:** Auto-docs are only as good as the type annotations — which we require anyway.
- **Scalability:** Scales automatically with the API surface.
- **Cost:** Free (built into FastAPI).
- **Learning curve:** Low.
- **Maintainability:** High — docs are a build artifact, not a manual chore.

### 20. Package Management — **uv (Python) · pnpm (JavaScript/TypeScript)**
- **Why:** **uv** is a fast, modern Python package/venv manager with reproducible lockfiles;
  **pnpm** is efficient (content-addressed store) with first-class monorepo workspaces.
  Deterministic installs matter for reproducible builds and supply-chain integrity
  ([ADR-0008](0008-security-architecture.md)).
- **Alternatives:** Poetry/pip-tools (mature, slower — Poetry is the fallback if uv proves
  limiting), npm/Yarn (heavier disk/instal footprint than pnpm).
- **Trade-offs:** uv is newer (smaller track record) but rapidly adopted; we accept minor
  maturity risk for speed and reproducibility, with Poetry as an escape hatch.
- **Scalability:** Both handle large dependency graphs and monorepos well.
- **Cost:** Open source.
- **Learning curve:** Low.
- **Maintainability:** High; lockfiles ensure reproducible, auditable dependencies.

### 21. Secrets Management — **AWS Secrets Manager + KMS (primary); OpenBao/Vault (path)**
- **Why:** Secrets and keys are security-critical, so we prefer a **managed, integrated,
  highly-reliable** solution: **AWS Secrets Manager** for credentials/tokens with automatic
  rotation, and **AWS KMS** for encryption keys — directly satisfying
  [ADR-0008 §5, §7](0008-security-architecture.md). Deep IAM integration enforces least
  privilege.
- **Alternatives:** **HashiCorp Vault / OpenBao** (open-source fork — more powerful dynamic
  secrets and cloud-portable; the documented path if we need multi-cloud or advanced dynamic
  secrets), Kubernetes Secrets alone (insufficient — base64, not real secret management).
- **Trade-offs:** Managed secrets deepen AWS coupling; accepted here because reliability of
  the secrets/key path outweighs portability, and abstracting secret access keeps a Vault
  migration feasible.
- **Scalability:** Fully managed, scales transparently.
- **Cost:** Per-secret/per-API-call pricing — modest; far cheaper than a secrets breach.
- **Learning curve:** Low (Secrets Manager); higher for Vault later.
- **Maintainability:** High; managed rotation and auditability reduce operational risk.

---

## Finalized Technology Stack (Implementation Standard)

This table is the **frozen standard for Phase 1**. Deviations require a superseding ADR.

| # | Layer | **Selected Technology** | Primary Alternative / Scale Path | Notes |
| --- | --- | --- | --- | --- |
| 1 | Frontend | **React + TypeScript (Next.js)** | SvelteKit / Vue+Nuxt | CDN-served, SSR/streaming |
| 2 | Backend | **Python + FastAPI** | Node.js/NestJS; Go | Async, Pydantic-typed |
| 3 | Database | **PostgreSQL** (+ TimescaleDB) | MySQL; Aurora (managed) | RLS for tenant isolation |
| 4 | Cache | **Redis (Valkey)** | Memcached | Cache, rate limiting, denylists |
| 5 | Message Queue | **RabbitMQ** | Apache Kafka (scale) | Reliable inter-agent events |
| 6 | AI Framework | **LangGraph** + Python ML (StatsForecast/scikit-learn) | Custom; LlamaIndex | Explicit, traceable agent graph |
| 7 | LLM Provider | **Anthropic Claude** (via abstraction) | OpenAI; self-hosted OSS | Pinned/versioned; swappable |
| 8 | Embedding Model | **Voyage AI** (via abstraction) | OpenAI embeddings; BGE/E5 (self-host) | Cached |
| 9 | Vector Database | **pgvector** (V1) | **Qdrant** (scale); Pinecone | Reuses Postgres in V1 |
| 10 | Authentication | **Keycloak (OIDC/OAuth2)** | Auth0/Okta; AWS Cognito | Standards-based, MFA/SSO |
| 11 | Cloud Platform | **AWS** | GCP; Azure | Portable via containers + IaC |
| 12 | Object Storage | **Amazon S3** (S3 API) | GCS/Azure Blob; MinIO (self-host/dev) | Encrypted; lifecycle policies |
| 13 | Monitoring | **OpenTelemetry + Prometheus + Grafana** (Tempo/Jaeger) | Datadog; CloudWatch | Vendor-neutral; carries `trace_id` |
| 14 | Logging | **Structured logs → Grafana Loki** | OpenSearch/ELK; Datadog | JSON + correlation IDs |
| 15 | CI/CD | **GitHub Actions + Argo CD (GitOps)** | GitLab CI; Jenkins | Security/eval gates in pipeline |
| 16 | Containerization | **Docker + Kubernetes (EKS)** | AWS ECS/Fargate (V1 simpler) | Portable; managed control plane |
| 17 | Infrastructure as Code | **Terraform / OpenTofu** | Pulumi; AWS CDK | Reproducible, reviewed infra |
| 18 | Testing | **pytest · Vitest + RTL · Playwright · AI evals** | unittest; Jest; Cypress | AI eval = ADR-0007 regression gate |
| 19 | API Documentation | **OpenAPI (FastAPI) + Swagger UI/Redoc** | Stoplight | Auto-generated, in sync |
| 20 | Package Management | **uv (Python) · pnpm (JS/TS)** | Poetry; npm/Yarn | Reproducible lockfiles |
| 21 | Secrets Management | **AWS Secrets Manager + KMS** | HashiCorp Vault / OpenBao | Managed rotation; IAM least-privilege |

---

## Rationale

- **Coherence.** A Python-first core unifies the API and the AI/agent engine; PostgreSQL
  (with pgvector/Timescale) and the Grafana observability stack each do multiple jobs,
  minimizing moving parts in V1 (principle 4).
- **Governance & security by construction.** RLS (tenant isolation), OpenTelemetry
  `trace_id`, OpenAPI-from-types, managed KMS/Secrets, and pipeline security/eval gates make
  ADR-0007/0008 requirements native to the stack rather than bolted on.
- **Lock-in hedged.** Open standards (OIDC, OTel, S3 API, OpenAPI, containers, Terraform) and
  provider abstractions (LLM, embeddings, vector DB, secrets) keep the costliest dependencies
  swappable, addressing [RSK-09](../../business/risk-register.md).
- **Lean-team operable.** Managed AWS services and GitOps reduce undifferentiated ops; the one
  high-complexity choice (Kubernetes) is managed and may start as a reduced footprint.

## Trade-offs (cross-cutting)

- **Python throughput** is lower than Go/JVM — accepted for AI-ecosystem fit; mitigated by
  async, horizontal scaling, and vectorized numeric libs.
- **Self-managed observability, auth, and queue** (Grafana stack, Keycloak, RabbitMQ) trade
  operational effort for cost control and portability; each has a managed escape hatch.
- **Kubernetes learning curve** is the steepest cost; mitigated by managed EKS, Terraform, and
  a possible simpler early-V1 footprint.
- **A few newer tools** (uv, LangGraph, OpenTofu) carry maturity risk; each has a mainstream
  fallback (Poetry, custom/LlamaIndex, Terraform).
- **AWS + managed secrets** create deliberate, contained coupling where reliability matters
  most.

## Alternatives Considered (summary)

Per-technology alternatives are documented in each decision above. At the **stack level** we
also considered:

1. **A JavaScript/TypeScript-everywhere stack** (Node backend). Rejected: it splits the team
   from the Python AI/ML ecosystem that is central to the product.
2. **A fully managed, single-vendor PaaS** (e.g., all-in on one provider's proprietary
   services). Rejected: fastest start but maximizes lock-in and long-term cost, conflicting
   with principle 3 and RSK-09.
3. **Maximal microservices from day one.** Rejected: premature operational complexity; we
   start with cohesive services on the agent/layer boundaries and split as metrics demand.

## Consequences

- **Phase 1 starts with a frozen standard.** Repository structure
  ([Repository Planning](../../planning/15-repository-planning.md)) will be realized in these
  technologies, organized on agent/layer boundaries.
- **Immediate Phase 1 kickoff tasks:** pin versions; choose deployment/tenancy topology
  (multi-tenant SaaS on shared cluster with Postgres RLS is the presumed default); stand up
  Terraform/OpenTofu baselines, CI/CD with security+eval gates, and the observability stack.
- **Provider abstractions are mandatory** for LLM, embeddings, vector DB, object storage, and
  secrets so the swap paths above remain real.
- **Open questions from the [Agent Architecture](../13-agent-architecture.md#9-open-architectural-questions-deferred-to-phase-1-design)
  are now partially resolved** (orchestration via LangGraph + RabbitMQ; deployment via
  Docker/K8s); cadence (real-time vs. batch) and exact tenancy remain Phase 1 design.
- **This ADR complements** ADRs [0004](0004-explainable-ai-mandate.md),
  [0005](0005-multi-agent-orchestration.md), [0006](0006-layer-over-systems-of-record.md),
  [0007](0007-ai-governance-framework.md), and [0008](0008-security-architecture.md); it
  supersedes none. Any future stack change requires a superseding ADR.
