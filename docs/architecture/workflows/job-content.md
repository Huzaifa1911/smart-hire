# Post or Update a Job

**Purpose:** Prepare reviewed job content and publish a processed revision.

Recruiter or owner: `post_job`, `update_job`.

## Steps

```mermaid
flowchart TD
    A[Recruiter starts post or update] --> B{Job: access valid?}
    B -->|No| X[Job: refuse request]
    B -->|Yes| C{Input method?}
    C -->|Form| D[Recruiter enters job details]
    C -->|Document| E[Job: prepare editable details from uploaded<br/>description]
    D --> F[Recruiter reviews and completes job details]
    E --> F
    F --> G[Job: recheck access and save revision<br/>with processing work]
    G --> H[Job: confirm processing submission]
    G -.-> I[Job: process revision content]
    I --> J{Processing complete?}
    J -->|No| K[Job: keep new revision unavailable and record<br/>failure]
    J -->|Yes| L[Job: request publication handoff]
    L --> O[Hiring: adopt the ready revision without<br/>resetting capacity]
    O --> M[Job: confirm published content]
    M -.-> N[Analytics: update publication measures]
```

## Failure and Recovery

- Unreadable documents require correction or form entry. Reuse unchanged preparation results where possible.
- Failed processing must not replace the previous published revision. Resume unfinished work for the same submitted revision.
- Proposed handoff: Hiring prepares the switch and pauses admission. Job marks readiness; Hiring adopts the revision and clears the pause without resetting capacity.
- Lost replies resume the same switch. An abandoned pause requires reconciliation; a timeout must not silently restore an old revision.
- This handoff has no assumed cross-service transaction. Its enforcement and concurrency behavior still need validation.

[Workflow index and shared execution rules](README.md)
