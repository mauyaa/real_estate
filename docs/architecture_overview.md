# Architecture Overview

This document summarizes the technical system needed to deliver the product vision. It highlights the service topology, data flows, integrations, and guardrails required to operate at scale in the Kenyan market.

## 1. Layered Architecture

| Layer | Scope | Technologies & Notes |
| --- | --- | --- |
| Experience | Web, PWA, USSD, WhatsApp surfaces, Admin console | React/Next.js or Remix with design system tokens, Service Worker for offline cache, Twilio/Sinch for SMS/WhatsApp, USSD gateway integration |
| Edge & APIs | API gateway, rate limiting, auth | NGINX/Envoy, OAuth 2.0 + JWT, IP allowlists for admin, WAF + bot mitigation |
| Domain Services | Listings, Search, Agents, Payments, Chat, Trust, Notifications | Node.js/TypeScript or Kotlin microservices with REST + gRPC endpoints, event-first APIs |
| Data & Intelligence | Postgres + PostGIS, Elastic/Meilisearch, Redis, Kafka/NATS, BigQuery/Snowflake | Outbox pattern, CDC pipelines, dbt transformations, Feature Store (Feast/Tecton) |
| Operations & Observability | Monitoring, tracing, alerting, logging | Prometheus, Grafana, OpenTelemetry, Loki/ELK, PagerDuty, Sentry |

## 2. Service Topology

```
            ┌───────────────────────┐
            │    Client Surfaces    │
            │ Web / PWA / Admin /   │
            │ WhatsApp / USSD       │
            └──────────┬────────────┘
                       │
                ┌──────▼───────┐
                │  API Edge    │  AuthN/Z, rate limiting,
                │  Gateway     │  JWT issuance
                └──────┬───────┘
                       │
        ┌──────────────┼────────────────────┬──────────────┐
        │              │                    │              │
┌───────▼──────┐┌──────▼──────┐     ┌───────▼──────┐┌───────▼──────┐
│ Listings Svc ││ Search Svc  │ ... │ Payments Svc ││ Trust Svc    │
│ CRUD, media  ││ Index sync   │     │ Escrow, M-Pesa││ KYC, disputes │
└───────┬──────┘└──────┬──────┘     └───────┬──────┘└───────┬──────┘
        │              │                    │              │
        └──────────────┴──────────┬──────────┴──────────────┘
                                   │
                             ┌─────▼─────┐
                             │  Event    │
                             │  Bus      │ Kafka/NATS
                             └─────┬─────┘
                                   │
                 ┌─────────────────┴──────────────────┐
                 │                                    │
         ┌───────▼──────┐                      ┌──────▼──────┐
         │ Data Lake /  │                      │ Feature     │
         │ Warehouse    │◄──────ETL/dbt────────│ Store       │
         └───────┬──────┘                      └──────┬──────┘
                 │                                    │
           ┌─────▼─────┐                        ┌─────▼─────┐
           │ Analytics │                        │ ML Models │
           │ Dashboards│                        │ Serving   │
           └───────────┘                        └───────────┘
```

## 3. Data Stores & Contracts

- **Postgres + PostGIS:** Canonical source for listings, users, agencies, bookings, payments. Enforce referential integrity, row-level security for multi-tenancy, partitioning for large history tables.
- **Object Storage (S3/MinIO):** Listing media, verification documents, signed URLs with expiry and optional watermarking.
- **Search Index (Elastic/Meilisearch):** Denormalized documents, synonyms for Kenyan locales, incremental updates via change events.
- **Redis:** Session storage, rate limits, cache of computed recommendations, feature flag evaluation.
- **Warehouse (BigQuery/Snowflake):** Ingest CDC + event streams, transformed via dbt into marts for product analytics, monetization insights, and regulatory reporting.
- **Feature Store:** Durable store for personalization, pricing models, and lead scoring features with online/offline parity.

## 4. Integration Points

| Integration | Purpose | Notes |
| --- | --- | --- |
| Safaricom Daraja (M-Pesa) | STK push, Paybill/Till payments, transaction status | Use idempotency keys, retry policies, webhook signature verification |
| DocuSign/HelloSign | E-sign for leases and deposits | Map to tenant/agent accounts, store signed PDFs in S3 |
| WhatsApp Business API | Agent-consumer communication, alerts | Template registration, compliance logging |
| SMS Gateway | Booking reminders, status updates | Failover provider strategy |
| CRB/KYC providers | Identity verification, credit checks | Tokenize responses, maintain audit trail |
| Mapping data (OpenStreetMap, KNBS, county zoning) | Spatial enrichment, heatmaps | Periodic refresh jobs, licensing compliance |

## 5. Security & Compliance Controls

- Central secrets management (Vault/SSM) with rotation policies and short-lived service credentials.
- End-to-end encryption (TLS 1.2+) and field-level encryption for sensitive PII (e.g., national IDs).
- Consent and deletion workflows orchestrated via Trust service with audit logs persisted immutably.
- Role-Based Access Control enforced across services; admin console hidden behind SSO + conditional access.
- Data residency review ensuring Kenyan storage requirements are met; cross-region replication for DR with encryption.
- Logging and monitoring for anomaly detection (velocity, IP reputation) feeding fraud scoring models.

## 6. Operational Excellence

- **Deployment:** GitHub Actions CI/CD with canary + blue/green strategies, automated smoke tests, infrastructure codified in Terraform.
- **Observability:** OpenTelemetry instrumentation across services, trace sampling configured for payments paths, Grafana dashboards with SLO burn-down alerts.
- **Reliability:** Rate limiting, circuit breakers, and bulkheads between services; readiness/liveness probes in Kubernetes; chaos drills quarterly.
- **Incident Response:** PagerDuty rotations, runbooks, customer status page, post-incident review template emphasizing remediation actions.

## 7. Data Governance

- Data catalog (e.g., Atlan/Amundsen) documenting schema, owners, and data quality SLAs.
- PII tagging within warehouse with access policies enforced via IAM + row-level security.
- GDPR/Kenya DPA-compliant consent capture, including minors handling and data subject access request timelines.
- Version-controlled dbt models with automated tests (schema, null checks, freshness).

## 8. Future Extensions

- **Marketplace APIs:** External API access for verified partners (property managers, lenders) with scoped OAuth clients.
- **Offline-first Agent App:** Native Android app with offline media capture, sync queue, and background uploads.
- **Machine Learning Ops:** Model explainability dashboards, bias audits for pricing and recommendation models, champion/challenger framework.
- **Infrastructure Scaling:** Edge caching for static assets in African regions, multi-cloud readiness for regulatory contingencies.
