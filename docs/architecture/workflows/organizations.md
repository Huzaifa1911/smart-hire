# Organization Management

**Purpose:** Create an organization and maintain its details.

Account: `create_organization`. Member: `view_organization`. Owner: `update_organization`.

## Steps

```mermaid
flowchart TD
    A[Account requests organization operation] --> B{Identity: request permitted?}
    B -->|No| X[Identity: refuse request]
    B -->|Yes| C{Identity: requested operation?}
    C -->|Create| D[Identity: save organization and initial owner<br/>together]
    C -->|View| E[Identity: read permitted details]
    C -->|Update| F[Identity: save permitted details]
    D --> G[Identity: return outcome]
    E --> G
    F --> G
```

Identity checks account access for creation, membership for viewing and owner access for updates.

## Failure and Recovery

- Never confirm creation without a durable initial owner membership.
- Recover the original creation outcome after a timeout; do not create another organization.

[Workflow index and shared execution rules](README.md)
