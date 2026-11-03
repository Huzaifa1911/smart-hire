# Browse and View Jobs

**Purpose:** Return published jobs and their application acceptance status.

Candidate: `search_jobs`, `view_job`.

## Steps

```mermaid
flowchart TD
    A[Candidate actor searches or opens a job] --> B[Job: select published content]
    B --> C[Hiring: supply application acceptance status]
    C --> D{Job: status available?}
    D -->|Yes| E[Job: return published content with known<br/>status]
    D -->|No| F[Job: return published content with unknown<br/>status]
```

## Failure and Recovery

- Public browsing need not depend on Identity. Missing Hiring status must not be presented as open acceptance.
- A displayed status reserves no capacity. Hiring checks current admission when the candidate applies.

[Workflow index and shared execution rules](README.md)
