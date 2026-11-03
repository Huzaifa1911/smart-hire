# Account Access

**Purpose:** Register an account or start and end a session.

Candidate or recruiter: `register_account`, `login`, `logout`.

## Steps

```mermaid
flowchart TD
    A[Person requests account access] --> B{Identity: requested operation?}
    B -->|Register| C[Identity: validate details and create common<br/>account]
    B -->|Sign in| D[Identity: verify credentials and establish<br/>permitted context]
    B -->|Sign out| E[Identity: end current session]
    C --> F[Identity: return outcome]
    D --> F
    E --> F
```

## Failure and Recovery

- Reject invalid credentials. Login must not restore removed organization access.
- Recover the original account or session outcome after a timeout. A retry must not create another account or session effect.

[Workflow index and shared execution rules](README.md)
