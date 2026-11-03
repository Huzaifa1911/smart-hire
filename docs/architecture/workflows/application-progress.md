# Application Tracking and Hiring Progress

**Purpose:** Read personal application status and record recruiter actions.

Candidate: `track_application`. Recruiter or owner: `move_application_stage`, `record_interview_progress`, `record_recruiter_notes`, `record_hiring_decision`.

## Steps

```mermaid
flowchart TD
    A[Actor requests application operation] --> B{Hiring: actor permitted for this operation<br/>and application?}
    B -->|No| X[Hiring: refuse request]
    B -->|Yes| C{Read or change?}
    C -->|Read| D[Hiring: return candidate-visible status]
    C -->|Change| E{Hiring: requested change obeys final-decision<br/>rule?}
    E -->|No| X
    E -->|Yes| F[Hiring: save change and required history]
    F -.-> G[Analytics: update progress measures]
```

## Failure and Recovery

- Save stage changes and history together, including actor and time. Retrying must not duplicate history or overwrite a final decision.
- Use the submitted stage definitions. Candidate-visible status must exclude private recruiter notes and other candidates' records.

[Workflow index and shared execution rules](README.md)
