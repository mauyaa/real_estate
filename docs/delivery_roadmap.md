# Delivery Roadmap

The roadmap provides a sequencing lens that balances marketplace trust, delightful demand-side experiences, and monetization. Each release must ship with instrumentation, operational playbooks, and rollout safeguards.

## Release 0 – Foundations (Months 0–3)

| Track | Milestones | Owners | Launch Readiness Gates |
| --- | --- | --- | --- |
| Supply onboarding | Agency verification workflow, document intake, duplicate detection MVP | Marketplace Ops, Trust & Safety | 10 pilot agencies onboarded, verification SLA < 24h |
| Consumer search | Polygon/radius search, POI overlays, responsive listing detail pages | Product, Search Eng | TFRR P95 < 9s on 3G, usability test ≥ 80% task success |
| Payments & escrow | Daraja STK integration (sandbox + prod), escrow ledger skeleton, dispute intake form | Payments Eng, Finance Ops | Successful end-to-end rent payment dry run, reconciliation report automation |
| Analytics | Event taxonomy v1, BigQuery/Looker pipeline for search & lead funnel | Data Eng, Analytics | Dashboard signed off by GTM, data freshness < 6h |

## Release 1 – Marketplace Acceleration (Months 4–6)

| Track | Milestones | Owners | Launch Readiness Gates |
| --- | --- | --- | --- |
| Personalization | Hybrid recommendation engine, “Because you viewed…” carousel, saved search alerts | Product, Data Science | A/B experimentation harness ready, lift detection plan | 
| Viewing journey | Calendar sync, viewing scheduler v1, automated reminders, feedback capture | Product, Agent Success | Pilot NPS ≥ 30, agent adoption ≥ 70% |
| Agent workspace | Lead routing rules, SLA timers, unified inbox MVP (web + WhatsApp) | Agency Success, Platform Eng | Hot-lead response P95 ≤ 5 min, QA playbook completed |
| Compliance | Tenant KYC tiers, consent logging, audit trail exports | Trust & Safety, Legal | Regulatory review sign-off, retention schedule documented |

## Release 2 – Intelligence & Monetization (Months 7–9)

| Track | Milestones | Owners | Launch Readiness Gates |
| --- | --- | --- | --- |
| AI assistant | Natural-language search assistant, listing auto-description, moderation triage | AI/ML, Support | Human-in-the-loop review SLA < 2h, hallucination scorecard |
| Pricing intelligence | Dynamic pricing insights, rent increase guidance, vacancy risk dashboards | Data Science, Monetization | Pricing adoption ≥ 30% of active agencies, ROI survey |
| Monetization | Agency subscriptions, promoted listings beta, lead packs | GTM, Billing | Billing accuracy 100% in UAT, revenue recognition policy approved |
| Ops console | Escrow board, moderation + KYC queues, SLA alerting | Internal Tools, Ops | Playbooks published, on-call training completed |

## Release 3 – Scale & Expansion (Months 10–12)

| Track | Milestones | Owners | Launch Readiness Gates |
| --- | --- | --- | --- |
| Platform resilience | Multi-region DR drills, blue/green deploys, status page | Platform Eng, SRE | Chaos test pass rate ≥ 90%, RTO ≤ 1h |
| Partner ecosystem | Moving/insurance marketplace launch, API partner program | BizDev, Partnerships | Partner SLAs signed, integration docs published |
| Advanced analytics | Ward/sub-county investment reports, cohort retention dashboards, experimentation suite v2 | Data Eng, Strategy | Exec adoption, experiment analysis SLA < 48h |
| Accessibility/i18n | WCAG AA audit, Swahili localization QA, RTL readiness | Design, Frontend | Accessibility score ≥ 95, translation coverage 100% |

## Cross-Cutting Requirements

- **Instrumentation:** Every release must include logging, dashboards, and alerting with owner sign-off.
- **Ops playbooks:** Runbooks, escalation paths, and QA test suites are mandatory before GA.
- **Change management:** Feature flags, staged rollouts, and rollback plans are non-negotiable for risky launches.
- **Customer education:** In-app tours, knowledge base updates, and GTM enablement happen in parallel with engineering.

## KPI Tracking Rhythm

- Weekly KPI review across growth, supply, and payments with red/amber/green status.
- Monthly deep-dives into trust & safety metrics with fraud/chargeback retrospectives.
- Quarterly board narrative summarizing product delivery, monetization performance, and regulatory posture.
