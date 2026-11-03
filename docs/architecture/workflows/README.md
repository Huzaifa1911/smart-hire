# Business Workflows

**Purpose:** Show the steps of each business process and how it recovers from failure.

[Requirements](../problem_statement.md) define the rules. [ADR 0002](../../adrs/0002-service-boundaries.md) defines ownership.
Each workflow keeps a flow diagram, followed by its specific failure behavior. Detailed sequence diagrams and contracts are deferred to implementation.

## Workflow Index

| Workflow | Owner |
| --- | --- |
| [Account access](account-access.md) | Identity |
| [Organization management](organizations.md) | Identity |
| [Membership and ownership](memberships.md) | Identity |
| [Recruiter invitations](invitations.md) | Identity |
| [Remove a recruiter](remove-recruiter.md) | Identity |
| [Candidate profile and resume](candidate-profile.md) | Candidate |
| [Post or update a job](job-content.md) | Job |
| [Browse and view jobs](job-discovery.md) | Job |
| [Hiring periods and capacity](hiring-periods.md) | Hiring |
| [Apply to a job](apply-to-job.md) | Hiring |
| [Application tracking and progress](application-progress.md) | Hiring |
| [Candidate scoring](candidate-evaluation.md) | Hiring |
| [Notification delivery](notifications.md) | Notification |
| [Hiring reports](reporting.md) | Analytics |

Identity means Identity & Organization Access. In diagrams, Candidate actor is the person; Candidate is the service.
Solid arrows show business steps. Dotted arrows show work that does not delay the user result.

## Shared Execution Rules

1. Apply the [access rules](../problem_statement.md#access-and-privacy) in APIs and workers. Missing authorization must not grant permission.
2. Confirm changes only after saving them durably with their required follow-up work. This does not assume a transaction across services or file storage.
3. On retries or timeouts, inspect the recorded outcome before repeating an effect. Apply source changes once; older changes must not replace newer current state.
4. Save original inputs, progress and completed results. After a crash, resume unfinished work and reuse completed results.
5. Retry temporary failures with delays and bounded attempts. Preserve exhausted or invalid work for investigation or correction.
6. A background failure must not undo an accepted source change. Missing dependencies leave work pending or return an unavailable outcome.

The files describe required behavior. Transport, persistence, retry timing and abandoned-work detection still need implementation design.

Next: [High-level architecture](../high_level_architecture.md).
