# Hiring Periods and Capacity

**Purpose:** Control when a job accepts applications.

Recruiter or owner: `configure_hiring_period`, `reopen_job`. Hiring also closes acceptance automatically.

## Steps

```mermaid
flowchart TD
    A[Recruiter changes period or Hiring detects<br/>expiry or limit] --> B{Hiring: valid authorized change or current<br/>automatic closure?}
    B -->|No| X[Hiring: reject change or ignore stale work]
    B -->|Yes| C{Initial setup or authorized reopening?}
    C -->|Yes| D[Hiring: preserve earlier applications and<br/>initialize count at zero]
    C -->|No| E[Hiring: preserve current count]
    D --> F{Period active and capacity available?}
    E --> F
    F -->|Yes| G[Hiring: permit acceptance with an adopted<br/>ready revision]
    F -->|No| H[Hiring: save closed status]
    G -.-> I[Job: update displayed acceptance status]
    H -.-> I
    G -.-> J[Analytics: update period measures]
    H -.-> J
```

## Failure and Recovery

- Save period, count and acceptance status consistently with concurrent application admission.
- Failed changes must not partially reset capacity. Retrying reopening must not create another period or reset the count again.
- Ignore expiry work for an old period. A duration change must not bypass the reopening rules.

[Workflow index and shared execution rules](README.md)
