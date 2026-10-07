# ADR 0002: Service Boundaries

Status: Proposed

## Purpose

Answers: **How should SmartHire's operations and data be grouped into services, and why?**

The [problem statement](../architecture/problem_statement.md) defines the operations and business rules. [ADR 0001](0001-architecture-style.md) explains the architecture style.

## 1. Identify the Business Concepts

This domain model describes the business concepts and their relationships.

| Concept | Meaning and Relationships |
| --- | --- |
| Account | A person's identity. An account can have candidate access and memberships in several organizations. |
| Organization | A tenant with memberships, jobs and private hiring records. |
| Membership | An account's owner or recruiter role within an organization. |
| Invitation | An offer to join an organization. Acceptance creates a membership. |
| Candidate Profile / Resume | Personal information and uploaded resumes used in applications. |
| Job | An organization's opportunity, with content revisions and hiring periods. |
| Job Revision | A preserved version of job content, requirements and stage definitions. Applications reference the submitted revision. |
| Hiring Period | A job's recruitment window, application limit, accepted count and acceptance status. |
| Application | A candidate's submission to a job revision during a hiring period. It has progress, notes and a final decision. |
| Stage History | Records each application's stage changes, actor and time. |
| Evaluation | A result based on submitted candidate information and a job revision. Hiring links the result to the application. |

## 2. Group Responsibilities into Services

Each service owns the operations of its listed capabilities. Capability names refer to the problem statement.

| Proposed Service | Capabilities | Data It Controls | Why Group This Work? |
| --- | --- | --- | --- |
| Identity & Organization Access | Identity & Authentication; Organizations & Access. | Accounts, credentials, sessions, candidate access, organizations, memberships, roles and invitations. | Membership, invitations and ownership enforce related access rules. |
| Candidate | Candidate Profiles & Resumes. | Profiles, skills, resumes and extracted information. | Personal profiles have a lifecycle separate from organization membership. |
| Job | Job Management & Publishing. | Job content, revisions, requirements, skills, stage definitions and processing status. | Content processing and job discovery need capacity separate from application handling. |
| Hiring | Applications & Hiring Progress. | Periods, limits, counts, acceptance status, accepted revision, applications, submitted information, progress, history, notes, decisions and evaluation links. | Acceptance, counting and closure enforce one capacity rule. Progress and decisions belong with application history. |
| Notification Service | Notifications. | Messages, templates, delivery requests, recipients, attempts and results. | Invitations and application receipts share delivery work. |
| Analytics Service | Hiring Reporting. | Derived report data and organization/platform scope. | Report queries and calculations need resources separate from operational hiring. |
| AI Service | Candidate Evaluation; Semantic Discovery; Recruitment Assistance. | Evaluations, search data, assistant interactions, recommendations, summaries, explanations and usage counts. | These tasks share recruitment intelligence and need resources separate from application handling. |

## 3. Define Ownership at Each Boundary

- Job controls revision readiness. Hiring controls application acceptance. A ready revision does not open a closed hiring period.
- Hiring preserves submitted candidate information and stage definitions. Later source changes must not change earlier applications.
- Candidate extracts resume information. AI computes evaluations. Hiring links results to applications. Evaluation does not decide acceptance or final hiring outcomes.
- Identity and Hiring decide when messages are needed. Notification controls delivery. Identity retains invitation validity.
- Analytics and AI own derived results. They do not own source jobs, profiles or hiring decisions.

## 4. Map Service Interactions

The arrows show information or work exchanged. They do not select a communication mechanism.

In this table, **Identity** means Identity & Organization Access.

| Operation | Exchange | Information or Work |
| --- | --- | --- |
| Create a profile or upload a resume | Identity → Candidate | Verified account identity and candidate access. |
| Perform a protected organization action | Identity → Job, Hiring, Analytics or AI | Current membership and role. Each receiving service checks permission for its own records. |
| Publish or update a job | Job → Hiring | Ready revision and stage definitions; the revision to use for new applications. |
| Apply to a job | Job, Candidate → Hiring | Published revision and submitted candidate/resume information. |
| Show job availability | Hiring → Job | Acceptance status. |
| Score an application | Hiring, Job, Candidate → AI → Hiring | Evaluation request, submitted revision, extracted resume information and result. |
| Send an application receipt | Hiring → Notification | Receipt delivery request. |
| Invite a recruiter | Identity → Notification | Invitation delivery request. Identity controls invitation validity. |
| Update reports | Identity, Candidate, Job, Hiring, AI → Analytics | Hiring facts and assistant usage. |
| Search or use an assistant | Job, Candidate, Hiring → AI | Permitted recruitment information for search and guidance. |

## 5. Record Costs and Remaining Decisions

Services add deployment work for one owner. They separate major capabilities, but do not isolate every internal operation.

Notification's separate deployment remains provisional. Separate workers may provide sufficient isolation.

Evaluation and delivery run in the background. Their failures must not undo accepted applications or recorded invitations. AI scoring can use basic skill matching without a large language model (LLM).

Further design must define:

- The publication handoff, without resetting capacity or reopening a closed hiring period.
- Immediate revocation across protected operations.
- Reliable work delivery.

Database, endpoint and messaging choices remain open. Test capacity, failure behavior and isolation across capabilities and tenants during implementation.
