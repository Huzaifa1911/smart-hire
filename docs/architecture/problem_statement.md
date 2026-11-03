# SmartHire Requirements

**Purpose:** Define the business outcomes, operations and rules the system must support.

## Problems and Goals

Manual hiring, scattered records and unreliable background work slow recruitment. Hiring spikes increase delays, and limited search and reporting hide useful information.
SmartHire must make recruitment easier to manage, keep records consistent and provide useful hiring reports.

## Actors and Scope

| Actor | Responsibility |
| --- | --- |
| Candidate | Maintain personal information, find jobs, apply and track applications. |
| Recruiter | Manage jobs and hiring within permitted organizations. |
| Organization owner | Manage organization access and perform recruitment operations. |

An organization is a **tenant**. One account can have candidate access and owner or recruiter memberships in several organizations.
A recruiter can apply elsewhere as a candidate. Their employer's membership must not expose those applications.
Common identity and multi-tenancy are agreed additions to the assignment.
Detailed interview scheduling, assessments, file formats and retention are outside this design discussion.

## Operations by Capability

These names describe user outcomes, not endpoints. Submission fields and automatic work are not separate user operations.

| Capability | Actor | Operations |
| --- | --- | --- |
| Account access | Candidate or recruiter | `register_account`, `login`, `logout` |
| Organization creation | Prospective owner | `create_organization` |
| Organization details | Member | `view_organization` |
| Organization details | Owner | `update_organization` |
| Membership and ownership | Owner | `list_memberships`, `update_membership`, `transfer_ownership`, `remove_recruiter` |
| Membership departure | Member | `leave_organization` |
| Invitations | Owner | `invite_recruiter`, `revoke_invitation` |
| Invitations | Invited account | `accept_invitation` |
| Candidate information | Candidate | `create_candidate_profile`, `upload_resume` |
| Job discovery | Candidate | `search_jobs`, `view_job` |
| Job content | Recruiter or owner | `post_job`, `update_job` |
| Hiring periods | Recruiter or owner | `configure_hiring_period`, `reopen_job` |
| Applications | Candidate | `apply_to_job`, `track_application` |
| Hiring progress | Recruiter or owner | `move_application_stage`, `record_interview_progress`, `record_recruiter_notes`, `record_hiring_decision` |
| Reporting | Recruiter or owner | `report_hiring_metrics` |

## Business Rules

### Access and Privacy

- Candidate registration enables personal candidate access. Recruiter registration alone grants no organization membership.
- Creating an organization establishes its initial owner. Accepting a valid invitation establishes membership.
- Selecting an organization grants no permission. Check current membership and resource permission for private recruitment records.
- Removal revokes organization access immediately, including signed-in access. Scheduled recruiter actions must recheck access and defer without advancing if access was removed.
- Owners may transfer ownership to an existing organization member. Role changes and departure must preserve at least one owner.
- Leaving or removal preserves the account, candidate access, other memberships and hiring history. Organizations cannot be deleted.
- Published jobs are public. Profiles, resumes, recruiter notes and hiring records are private. Candidates see only their own application status. Recruiters need organization and resource permission to read submitted information.

### Job Content and Resumes

- A job submission includes title, description, required skills and hiring stages. Accept form entry or an uploaded description.
- An uploaded description produces editable details. The recruiter reviews and completes them before submission; uploading alone does not publish.
- Submission automatically starts keyword extraction, skill mapping and content structuring. Processing must not silently replace confirmed requirements or stages.
- Preserve job revisions. Keep the previous published revision available during an update. Use the new revision for subsequent applications once ready.
- Required processing must succeed before readiness. No additional publish action is required.
- Resume upload automatically starts parsing. Save the result against that resume; scoring consumes it without starting another parse.

### Applications and Capacity

- Accept only with candidate access, a ready adopted revision, an active hiring period and available capacity. Do not impose job-specific eligibility filters.
- Allow one application per candidate per job revision, including after reopening. Applications cannot be withdrawn.
- Preserve the submitted job revision, resume information and stage definitions. Later source changes must not alter earlier applications.
- Each hiring period has a duration, limit and accepted count. Close acceptance at the limit or period end; concurrent submissions must not exceed capacity.
- During an active period, limit changes use the existing count. Neither limit changes nor content revisions reset capacity or remove applications.
- Reopening starts a new period with zero count and preserves earlier applications. Extending an ended period must not bypass reopening.
- Acceptance initializes hiring history and records background scoring, receipt delivery and reporting work. It does not wait for parsing or scoring.
- Basic or simulated scoring uses the submitted information. Scores do not decide eligibility or final hiring outcomes.

### Hiring Progress

- Authorized recruiters and owners may skip stages or move backward. Record the previous stage, new stage, actor and time.
- Final decisions cannot be corrected. Stage changes cannot reopen or change a final decision.

## Reliability and Scale

- Keep business records durable, queryable and consistent, including application history.
- Handle tens of thousands of concurrent applications and interview events. Control incoming work when capacity is exhausted.
- Scale background processing separately. Overload in one capability or tenant must not exhaust resources needed by others.
- Handle retries and partial failures without duplicate effects or lost work. Make failures visible through logs, metrics and traces.
- Apply access rules to APIs, workers and reports.

These are design targets, not measured results. Numerical latency, availability and recovery objectives remain unspecified.

## Required Reports

Reports use the permitted organization or platform scope:

- Count of active candidates who have profiles.
- Counts of recruiters managing postings and active job postings.
- New applications by day, week and month.
- Application-to-interview conversion.
- Average time from application to final decision.
- Most-applied jobs and average applications per candidate.
- Failed workflows and system errors.

Dashboards auto-refresh every 30 minutes. This does not define a maximum delay in source-data updates.

Sources: [Overall requirements](../concept/SmartHire%20%E2%80%94%20Intelligent%20Workforce%20Orchestration%20%26%20Recruitment%20Platform.md) and [Part A](../concept/SmartHire%20-%20Part%20A.md).
The access, revision, capacity and submission-review rules include agreed product choices.

Next: [Architecture style](../adrs/0001-architecture-style.md).
