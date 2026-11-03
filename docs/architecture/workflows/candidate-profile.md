# Candidate Profile and Resume

**Purpose:** Save personal information and automatically parse uploaded resumes.

Candidate: `create_candidate_profile`, `upload_resume`.

## Steps

```mermaid
flowchart TD
    A[Candidate actor submits personal information] --> B{Candidate: access and ownership valid?}
    B -->|No| X[Candidate: refuse request]
    B -->|Yes| C{Profile or resume?}
    C -->|Profile| D[Candidate: save profile and skills]
    D --> E[Candidate: confirm profile saved]
    D -.-> F[Analytics: update profile measures]
    C -->|Resume| G[Candidate: store file and parsing work]
    G --> H[Candidate: confirm upload]
    G -.-> I[Candidate: parse stored resume and save result]
```

Hiring reads the saved parsing result in the [scoring workflow](candidate-evaluation.md). Application submission does not start parsing.

## Failure and Recovery

- Do not confirm an upload unless its file and record are durable. Reconcile partial file storage before repeating an upload.
- Parsing failure leaves the uploaded file stored. Resume parsing against that same file; preserve earlier submitted resumes.

[Workflow index and shared execution rules](README.md)
