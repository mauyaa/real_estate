# Payments & Escrow Design

This document deep-dives on the fintech surface area of the platform. It expands on how we will collect rent, manage escrow balances, reconcile M-Pesa transactions, and protect users through strong compliance controls.

## 1. Scope & Objectives

- Support recurring rent payments, security deposits, and agency commissions with optional split payments for roommates.
- Maintain a tamper-proof double-entry ledger that powers statements, audits, and dispute resolution.
- Integrate with Safaricom's Daraja APIs in a production-ready manner that handles retries, reversals, and reconciliation.
- Enforce KYC/AML policies, fraud detection, and regulatory reporting to meet Kenya Data Protection Act and CBK expectations.

## 2. Payment Flows

### 2.1 Rent & Deposit Collection

1. Tenant initiates payment from consumer app or via M-Pesa STK push.
2. Payments Service validates booking/lease context and creates an `EscrowTransaction` record with pending status.
3. Ledger Service posts double-entry movements: debit Tenant Wallet, credit Escrow Holding Account.
4. Webhook listener receives Daraja confirmation and updates transaction state to `funded`.
5. Automatic receipts and notifications are sent to tenant, agent, and internal ops.
6. Funds are released to agents/landlords upon viewing completion or lease execution, subject to dispute locks.

### 2.2 Split & Partial Payments

- Each roommate has a sub-account linked to the primary lease.
- Ledger keeps individual sub-ledgers and enforces that aggregate payments meet deposit amount before release.
- Reminder engine triggers nudges and late fee rules (configurable per agency).

### 2.3 Refunds & Chargebacks

- Dispute Service can place a hold on transactions, preventing release.
- Refund workflow posts reversing entries (credit Tenant Wallet, debit Escrow Holding) and triggers Daraja reversal APIs.
- Partial refunds use memo lines to document rationale and reference case IDs.

## 3. System Components

| Component | Responsibilities | Key Notes |
| --- | --- | --- |
| Payments API | Initiate charges, handle callbacks, expose status | Idempotent request keys, HMAC verification |
| Ledger Service | Double-entry bookkeeping, statements, balance snapshots | ACID transactions in Postgres partitioned by month |
| Escrow Orchestrator | State machine for Pending → Funded → Released/Refunded | Uses event bus for downstream notifications |
| Notification Service | SMS/WhatsApp/email receipts and reminders | Template localization (en/sw) |
| Risk Engine | Velocity rules, device/IP scoring, manual review queue | Shares signals with Trust & Safety team |

## 4. Data Model Highlights

- **Accounts**: represent wallets (tenant, agent, platform fee) and system holding accounts. Fields include `account_id`, `type`, `currency`, `status`, `owner_ref`.
- **Ledger Entries**: immutable double-entry rows with `entry_id`, `transaction_id`, `account_id`, `direction`, `amount`, `currency`, `memo`, `created_at`.
- **Transactions**: tie business context to ledger movements. Includes `transaction_type` (rent, deposit, refund), `status`, `metadata` (booking ID, dispute ID).
- **Reconciliation Batches**: store import logs from Daraja statements with `external_id`, `amount`, `matched_transaction_id`, `variance`.

Row-level security ensures agencies see only their payouts, while finance operators have read-only cross-tenant access.

## 5. Integration with Daraja (M-Pesa)

- **Authentication**: Use short-lived OAuth tokens cached securely and rotated automatically.
- **Idempotency**: Pass platform-generated UUIDs in `AccountReference` or metadata to deduplicate retries.
- **Webhook Handling**: Validate origin IPs, check HMAC signatures, enqueue processing to avoid blocking threads.
- **Timeouts & Retries**: Implement exponential backoff and reconciliation jobs to sweep stuck `pending` transactions.
- **Paybill/Till Support**: Configure dedicated channels for rent vs. ancillary services to simplify settlement accounting.

## 6. Reconciliation & Reporting

- Daily automated reconciliation compares Daraja statements with ledger balances; mismatches create `ReconciliationIssue` tasks.
- Finance dashboards track inflows, outflows, outstanding balances, and fee accruals.
- Monthly statements available for tenants, agents, and regulators with exportable CSV/PDF formats.

## 7. Compliance & Risk Controls

- Tiered KYC: verify national ID, proof of residence/income before enabling high-value transactions.
- AML screening: run names against sanctioned lists and CRB checks via approved partners.
- Audit trails: immutable logs for all ledger adjustments, approvals, and overrides.
- Segregation of duties: finance ops approve payouts; support cannot trigger payouts without dual control.
- Data retention: align with Kenya DPA, retaining financial records for minimum statutory periods.

## 8. Observability & SLAs

- Metrics: transaction success rate, STK timeout rate, reconciliation completion time, dispute resolution SLA.
- Alerts: trigger on error spikes, reconciliation variances, ledger imbalance, or delayed webhook processing.
- Runbooks: documented steps for Daraja outage handling, ledger rollback, and manual payout processing.

## 9. Roadmap Hooks

- Release 0: Deliver core rent collection, ledger MVP, reconciliation automation.
- Release 1: Add split payments, configurable reminders, and improved dispute locking.
- Release 2: Introduce dynamic fee schedules, partner payouts, and advanced risk scoring.
- Release 3: Launch multi-currency support and cross-border remittance experiments.

## 10. Open Questions

1. What is the appetite for offering tenant financing or rent advance features in partnership with lenders?
2. Should escrow interest earnings be shared with tenants/agents or retained as platform revenue?
3. How do we support offline M-Pesa payments (USSD) while maintaining real-time reconciliation accuracy?

