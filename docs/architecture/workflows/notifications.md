# Notification Delivery

**Purpose:** Deliver application receipts and organization invitations.

Automatic work: Hiring requests receipts; Identity requests invitations. Notification owns delivery.

## Steps

```mermaid
flowchart TD
    A[Hiring: record receipt request] --> C[Notification: save message and recipient]
    B[Identity: record invitation delivery request] --> C
    C --> D[Notification: send through delivery provider]
    D --> E[Notification: save accepted, failed or<br/>uncertain outcome]
    E -.-> F[Analytics: update delivery failure measures]
```

## Failure and Recovery

- Provider acceptance does not prove recipient receipt. Delivery failure leaves the application or invitation unchanged.
- Retry confirmed temporary failures. Reconcile uncertain outcomes before resending because a timeout may follow a successful send.
- Provider deduplication and status-query capabilities remain to be selected; unresolved outcomes may need investigation.

[Workflow index and shared execution rules](README.md)
