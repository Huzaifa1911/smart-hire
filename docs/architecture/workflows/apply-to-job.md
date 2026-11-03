# Apply to a Job

**Purpose:** Accept an application without duplicates or exceeding capacity.

Candidate: `apply_to_job`.

## Steps

```mermaid
flowchart TD
    A[Candidate actor applies] --> B{Hiring: candidate access valid?}
    B -->|No| X[Hiring: refuse request]
    B -->|Yes| C[Hiring: read adopted revision and stages]
    C --> D[Candidate: supply owned submission information]
    D --> E{Hiring: duplicate for this revision?}
    E -->|Yes| F[Hiring: return existing application without<br/>increasing count]
    E -->|No| G{Hiring: ready revision and acceptance valid?}
    G -->|No| X
    G -->|Yes| H[Hiring: save application, history, count,<br/>required closure and follow-up work]
    H --> I[Hiring: confirm acceptance]
    H -.-> J[Hiring: score submitted information]
    H -.-> K[Notification: deliver application receipt]
    H -.-> L[Analytics: update application reports]
```

When acceptance reaches capacity, Hiring also updates Job's displayed status. Scoring follows the [evaluation workflow](candidate-evaluation.md).

## Failure and Recovery

- At save, recheck the ready adopted revision, any switch pause, period, capacity and duplicates. Save required closure with the count; earlier reads reserve nothing.
- Resume an uncertain submission from its saved outcome. A retry must not consume capacity or create follow-up work twice.
- Parsing, scoring, receipt or reporting failures must not undo acceptance or block independent follow-up work.

[Workflow index and shared execution rules](README.md)
