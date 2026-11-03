# Recruiter Invitations

**Purpose:** Invite an account and establish membership through acceptance.

Owner: `invite_recruiter`, `revoke_invitation`. Intended recipient: `accept_invitation`.

## Steps

```mermaid
flowchart TD
    A[Owner requests invitation] --> B[Identity: authorize and save invitation with<br/>delivery work]
    B --> C[Identity: confirm invitation recorded]
    B -.-> D[Notification: deliver invitation]
    E[Recipient accepts] --> F{Identity: recipient and invitation valid?}
    F -->|Yes| G[Identity: save membership and acceptance<br/>together]
    F -->|No| H[Identity: refuse acceptance]
    I[Owner revokes invitation] --> J[Identity: authorize and invalidate invitation]
```

## Failure and Recovery

- Delivery failure leaves the invitation recorded; Notification retries independently.
- Identity must order acceptance against revocation. A delivered message does not prove validity, and repeated acceptance must not duplicate membership.
- Revoking an accepted invitation does not remove an established membership.

[Workflow index and shared execution rules](README.md)
