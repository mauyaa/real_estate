 # Real Estate Platform Product Vision

## 0. Executive Summary

The Kenya-focused platform must simultaneously delight renters and buyers, empower agencies, and give internal teams confident control over compliance, payments, and quality. The vision we are pursuing is a multi-sided marketplace with fintech-grade reliability, AI-accelerated workflows, and data-rich intelligence. This document reframes the initial feature list into a mission-oriented charter, adds context on personas, and sequences delivery so that each release compounds value for the ecosystem.

### Core Outcomes

| Audience | Primary Goal | Supporting Themes |
| --- | --- | --- |
| Consumers (buyers & renters) | Reduce time-to-trustworthy match | Deep discovery, personalized recs, transparent pricing, seamless bookings |
| Agents & agencies | Accelerate deal velocity and marketing ROI | Inventory automation, CRM workflows, omnichannel comms, performance insights |
| Internal ops & compliance | Maintain safety, payments integrity, and regulatory posture | Moderation, escrow management, KYC/AML, auditing |

### Guiding Principles

1. **Trust by design** – verification, moderation, and escrow must be default behaviors, not premium add-ons.
2. **Kenya-native experiences** – design for matatu routes, M-Pesa, and local compliance ahead of global parity features.
3. **Assistive AI, human control** – AI should draft, recommend, and flag; humans approve, configure, and override.
4. **Instrumentation everywhere** – every launch includes analytics, alerts, and experiment hooks.

### Key Personas & Jobs to Be Done

- **Grace (First-time renter, Nairobi)** – wants fast search, verified listings, commute clarity, and safe digital payments.
- **Samuel (Agency owner in Westlands)** – needs a single workspace for listing uploads, lead routing, staff performance, and payouts.
- **Mercy (Marketplace operations lead)** – requires auditable queues for KYC, disputes, and configuration to maintain regulatory compliance.

## 1. Consumer Experience

### 1.1 Deep Search & Discovery

**Now (MVP)**
- Polygon, radius, and commute-time searches backed by PostGIS with tuned GIST indices.
- Geo overlays for core POIs (schools, hospitals, matatu stages) with amenity filters.
- Listing detail pages with price history charts (3-year minimum) and comparable listings.

**Next**
- Market heatmaps and micro-neighborhood guides combining internal data with KNBS statistics.
- Saved search alerts that summarize deltas (new listings, price drops, expiring offers).

**Later**
- Interactive investment calculators factoring commute vs rent trade-offs and vacancy trends.

### 1.2 Personalization & Recommendations

- Hybrid collaborative + content-based ranking that balances budget, location affinity, and amenities.
- “Because you viewed…” carousel, homepage quick picks, and MLS-style cross-sells.
- Preference learning from dwell time, shortlists, and inquiry outcomes with guardrails for fairness.

### 1.3 Viewing & Booking Journey

- End-to-end viewing scheduler aligned to agent availability calendars (Google/Microsoft sync where possible).
- SMS/WhatsApp reminders enriched with route time, traffic advisories, and reschedule self-service.
- Post-viewing feedback prompts to capture satisfaction and update ranking signals.

### 1.4 Trust, Documentation & Compliance

- Verified badges triggered by document submissions (ownership proof, utility bill) and staff approvals.
- Standardized deposit/lease templates with DocuSign/HelloSign integration and secure document vault.
- Tenant KYC with tiered requirements (ID, proof of income) and storage policies aligned to Kenya Data Protection Act.

### 1.5 Payments & Collections

- Recurring rent mandates, partial payments, and roommate split flows with automated receipts.
- Dispute center linked to escrow service, allowing evidence attachments and structured resolutions.

### 1.6 Omnichannel Reach

- Installable PWA with offline saved listings and update queuing.
- WhatsApp Business API for alerts and agent chat, USSD flows for search snapshots, and SMS updates for bookings.

### 1.7 Accessibility & Internationalization

- WCAG 2.2 AA baselines (contrast, keyboard nav, transcripts).
- English/Swahili parity at launch; RTL-ready layout tokens for regional expansion.

## 2. Agent & Agency Workspace (SaaS)

### 2.1 Inventory Management

- Bulk CSV uploads with validation, AI quality checks (blurry detection, watermark removal suggestions), and geo-tagging.
- Auto-captioning using property attributes and AI summarization, with edit history.
- Duplicate detection leveraging similarity search on images, copy, and geo coordinates.

### 2.2 Lead & Pipeline Management

- Territory-based lead routing, SLA timers, and escalation nudges for slow responses.
- Hot-lead scoring derived from consumer engagement signals and agent response behavior.
- Task board with follow-ups, document requests, and auto-generated reminders.

### 2.3 Communications Hub

- Unified inbox aggregating web chat, WhatsApp, SMS, and call logs with consented recordings.
- AI-assisted replies with tone controls and auto-translated templates.
- Conversation tagging and sync with CRM events for downstream analytics.

### 2.4 Team Operations & Branding

- Multi-tenant roles (Owner, Admin, Agent, Photographer) with granular permissions and audit trails.
- Brand themes influencing microsites, email templates, and watermark overlays.
- White-label microsites per agency with SEO controls and curated listings.

### 2.5 Performance Analytics

- Dashboards for response times, close rates, listing velocity, and marketing ROI per channel.
- Benchmarking vs. market averages to encourage healthy competition.

## 3. Mapping & Data Intelligence

- Unified spatial model linking properties, buildings, parcels, and road networks with topology rules.
- Demand heatmaps, price/bedroom density surfaces, and ward/sub-county time series dashboards.
- External data ingestion for KNBS socioeconomics, zoning, property taxes, hazard/flood zones, and land registry hooks.
- Isochrone-based commute visualizations and rent vs commute cost trade-off calculators.

## 4. Payments, Escrow & Fintech

- Production-grade Daraja (M-Pesa) integration with idempotent STK, retries, reconciliation, dynamic QR, and HMAC webhooks.
- Wallets and ledgers supporting KES primary with extensible multi-currency support, double-entry accounting, configurable fees, chargebacks, and payouts to agents.
- Billing workflows covering invoices, VAT support, KRA PIN capture, downloadable statements, and automated reminders.
- Risk & compliance stack: KYC/AML (ID, CRB), fraud scoring, velocity rules, and manual review queues.

## 5. AI-Driven Experiences

- Natural-language assistant (LangChain/OpenAI or local) for filters, neighborhood Q&A, and policy FAQs with citations.
- Content automation: listing description generation, chat summarization, prohibited content detection, face/license-plate blurring.
- Pricing intelligence blending comparables, seasonality, and vacancy risk to suggest rent/price adjustments.
- Routing automation to classify leads, propose viewing times, and draft follow-ups from knowledge base.

## 6. Trust, Safety & Moderation

- Listing verification workflows with document uploads, agency office visits, and risk scoring.
- Moderation pipeline for images (NSFW/model detection), spam/duplicate detection, anomaly pricing alerts, and reputation scores.
- Dispute management with case threads, evidence uploads, timers, structured outcomes (refund/partial/deny), and auditor visibility.

## 7. Admin & Operations

- Ops console for escrow stages (Pending → Funded → Released/Refunded), KYC queues, moderation queue, and SLA breach dashboards.
- Config store managing feature flags, ranking knobs, fee tables, and marketing banners with approval gates.
- Auditing fabric capturing who did what and when, producing tamper-evident logs and regulator-ready exports.
- Staff access secured via SSO, RBAC, and environment toggles to hide admin modules from public builds.

## 8. Data Platform & Analytics

- Event taxonomy covering search, filter_applied, listing_view, chat_started, escrow_initiated/succeeded, viewing_booked, rent_paid, and more.
- Warehouse + dbt modeling into curated marts feeding cohort, funnel, and performance dashboards (Looker/Superset).
- Experimentation with feature flags, exposure logging, sequential testing, and guardrail metrics.
- ML Ops with feature store, model registry, CI/CD for models, and Airflow orchestrated retraining.

## 9. Architecture & Scale

- Event-driven microservice architecture with services for search, payments, chat, listings, and users communicating via Kafka/NATS and the outbox pattern.
- Search powered by Meilisearch/Elastic with incremental updates, synonyms for Kenyan locales, and failover indexing.
- Redis caching for sessions, rate limits, and query caching to guarantee fast TFRR.
- Storage + delivery: S3/MinIO with signed URLs, CDN distribution, Kubernetes orchestration, GitHub Actions for CI/CD, Terraform IaC, blue/green deployments.
- Observability stack with OpenTelemetry traces, Prometheus/Grafana metrics, Sentry error capture, and SLO dashboards for API/search/checkout latency and uptime.

## 10. Security & Compliance

- Kenya Data Protection Act alignment through consent tracking, data maps, deletion workflows, and DPO tooling.
- PCI-DSS SAQ A posture via tokenized payments, encryption at rest (KMS) and in transit, WAF, and bot protection.
- Secret management with Vault/SSM, short-lived credentials, per-service KMS keys, and least-privilege IAM.
- Backups/DR including PITR for Postgres, cross-region snapshots, rehearsed runbooks, and chaos testing.

## 11. Monetization

- Agency subscriptions with seat-based tiers and feature add-ons (priority placement, brand pages).
- Promoted listings governed by fair ranking rules, transparent disclosures, and spend controls.
- Lead packs (pre-paid) and performance-based billing (CPL/CPA) with ROI analytics.
- Ancillary revenue through partner marketplaces (moving services, insurance, cleaning/repairs).

## 12. Success Metrics & Health KPIs

| Metric | Baseline (est.) | Target | Notes |
| --- | --- | --- | --- |
| Time to First Relevant Result (TFRR) | >15s | <7s | Track by persona, device, and network condition. |
| Search → Contact conversion | 12% | ≥15.6% (+30%) | Derived from logged events and CRM sync. |
| Contact → Viewing conversion | 20% | ≥24% (+20%) | Requires accurate booking + attendance capture. |
| Viewing → Escrow conversion | 10% | ≥11.5% (+15%) | Influenced by payments UX and agent follow-up. |
| Agent P95 response time | 15 min | ≤2 min | Enforced via SLAs and nudges. |
| Payment success rate | 90% | ≥97% | Watch failure reasons (insufficient funds, timeouts). |
| Dispute resolution median time | 7 days | ≤3 days | Powered by workflows in trust module. |
| Core Web Vitals (Android mid-tier) | LCP 4s / INP 350ms / CLS 0.2 | LCP <2.5s, INP <200ms, CLS <0.1 | Monitor via RUM + lab tests. |

### Feedback Loops

- Weekly marketplace health review synthesizing KPIs, NPS, qualitative feedback, and support themes.
- Growth and compliance squads own cross-functional OKRs aligned to the above targets.

## 13. Delivery Considerations

### Sequencing Philosophy

1. **Trust & supply first** – verify listings, onboard agencies, and ensure payment + dispute infrastructure before driving mass demand.
2. **Delight core flows** – invest in search, personalization, and viewing bookings to reduce renter friction.
3. **Amplify with AI & analytics** – layer intelligence and automation once baseline data quality is established.

### Dependencies

- Reliable property data ingestion to unlock search, personalization, and analytics.
- Regulatory approvals for KYC providers, CRB checks, and document signing where local regulations apply.
- Partnerships for payments (Safaricom), insurance, and moving services.

### Risks & Mitigations

- **Data quality drift** → nightly audits, duplicate detection, human review budgets.
- **Agent adoption** → onboarding academy, incentive programs tied to response SLAs.
- **Payment outages** → multi-provider strategy, proactive monitoring, customer-facing status page.

## 14. Open Questions

1. Level of integration with land registry APIs and feasibility of real-time title checks.
2. Appetite for tenant credit scoring in partnership with CRBs versus privacy expectations.
3. Phasing of monetization levers (subscriptions vs. promoted listings) relative to marketplace liquidity.

## 15. Appendices

- [Delivery Roadmap](./delivery_roadmap.md) – phased plan with releases, ownership, and instrumentation gates.
- [Architecture Overview](./architecture_overview.md) – high-level system topology, data flows, and integration points.
- [Payments & Escrow Design](./payments_escrow_design.md) – detailed flows, ledger model, and compliance controls for rent collection.

