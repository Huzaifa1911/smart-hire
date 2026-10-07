# SmartHire Problem Statement

## Problems / Challenges

- Manual posting, candidate evaluation and interview operations slow hiring.
- Limited search and candidate insights make suitable candidates hard to identify.
- Scattered data and asynchronous updates produce inconsistent hiring progress and reports.
- Hiring spikes delay user requests and background processing.
- Unreliable background work and limited failure visibility make recovery difficult.
- Hiring data is underused for measuring outcomes and supporting decisions.

## Business Goals

Reduce manual hiring work, help candidates find suitable jobs, keep hiring progress reliable, and give recruiters useful insights.

## Actors and Organization Scope

| Actor / Role | Responsibility |
| --- | --- |
| Candidate | Maintain a personal profile, discover jobs, apply and track their applications. |
| Recruiter | Manage jobs and hiring in organizations where they have access. |
| Organization Owner | Manage organization access and perform authorized recruitment operations. |

An organization is a **tenant**: its private recruitment data is separate from other organizations. Shared identity and multi-tenancy are product extensions beyond the assignment.

One account can have candidate access and recruiter/owner memberships in multiple organizations. A recruiter can apply to another organization as a candidate. Their recruiting membership does not expose those applications to their organization or grant access to the other organization's hiring data.

## System Operations

### Actor Requests

| Actor | Operations | Outcome |
| --- | --- | --- |
| Candidate / Recruiter | `register_candidate`, `register_recruiter`, `login`, `logout` | Create or use a common account. Recruiter registration alone grants no organization access. |
| Prospective Organization Owner | `create_organization` | Create an organization and its initial owner membership. |
| Organization Member | `view_organization`, `select_organization`, `leave_organization` | View, work within or leave an authorized organization. |
| Organization Owner | `update_organization`, `list_memberships`, `update_membership`, `invite_recruiter`, `revoke_invitation`, `remove_recruiter`, `transfer_ownership` | Manage organization details and access. |
| Invited Recruiter | `accept_invitation` | Join the intended organization through a valid invitation. |
| Candidate | `create_candidate_profile`, `upload_resume`, `search_jobs`, `view_job`, `apply_to_job`, `track_application` | Maintain candidate information, discover jobs and follow applications. |
| Recruiter / Owner | `post_job`, `update_job`, `upload_job_description`, `define_required_skills`, `manage_hiring_stages`, `publish_job` | Define and publish job opportunities. |
| Recruiter / Owner | `set_hiring_duration`, `set_application_limit`, `reopen_job` | Manage hiring periods and capacity. |
| Recruiter / Owner | `move_application_stage`, `record_interview_progress`, `record_recruiter_notes`, `record_hiring_decision` | Manage hiring progress and outcomes. |
| Recruiter / Owner | `report_hiring_metrics` | View authorized organization reports. |
| Candidate / Recruiter / Owner | `semantic_search` | Find relevant jobs or authorized candidate information. |
| Recruiter / Owner | `recommend_candidates`, `summarize_resume`, `explain_candidate_ranking`, `enhance_job_description` | Support candidate evaluation and improve descriptions. |
| Candidate | `answer_job_questions`, `assess_role_fit`, `provide_application_guidance` | Receive advice grounded in job and candidate information. |

### Automatic Processing

| Trigger | Operations | Outcome |
| --- | --- | --- |
| Job publishing or update | `extract_job_keywords`, `map_job_skills`, `structure_job_description`, `mark_job_ready` | Save structured content; mark ready only after required processing succeeds. |
| Candidate application | `parse_resume`, `score_candidate`, `send_application_notification` | Process the resume, score the match and confirm application receipt. |
| Organization invitation created | `send_invitation_notification` | Deliver the invitation to the intended recruiter. |
| Hiring period ends or capacity is reached | `close_job` | Close admission to further applications. |
| Hiring data changes | `update_analytics` | Update reports without losing or double-counting changes. |

The architecture covers core recruitment, semantic retrieval and AI assistance. The source delivery phases separate core workflows (Part A) from recruitment intelligence (Part B); both are included in this design.

## Business Capabilities

Capabilities group related operations and data. They do not prescribe service boundaries.

| Capability | Operations | Business Data |
| --- | --- | --- |
| Identity & Authentication | `register_candidate`, `register_recruiter`, `login`, `logout` | Accounts, credentials, candidate access and sessions. |
| Organizations & Access | `create_organization`, `view_organization`, `select_organization`, `update_organization`, `list_memberships`, `update_membership`, `invite_recruiter`, `revoke_invitation`, `accept_invitation`, `remove_recruiter`, `transfer_ownership`, `leave_organization` | Organizations, memberships, roles and invitations. |
| Candidate Profiles & Resumes | `create_candidate_profile`, `upload_resume`, `parse_resume` | Profiles, skills, resumes and extracted information. |
| Job Management & Publishing | `post_job`, `update_job`, `upload_job_description`, `define_required_skills`, `manage_hiring_stages`, `publish_job`, `extract_job_keywords`, `map_job_skills`, `structure_job_description`, `mark_job_ready`, `search_jobs`, `view_job` | Jobs, revisions, descriptions, requirements, skills, stage definitions and publishing progress. |
| Applications & Hiring Progress | `set_hiring_duration`, `set_application_limit`, `reopen_job`, `close_job`, `apply_to_job`, `track_application`, `move_application_stage`, `record_interview_progress`, `record_recruiter_notes`, `record_hiring_decision` | Periods, limits, counts, admission status, applications, submitted revision/resume information, stages, history, notes, interview progress and decisions. |
| Candidate Evaluation | `score_candidate` | Application scores and the job/candidate information used to calculate them. |
| Notifications | `send_application_notification`, `send_invitation_notification` | Application receipts, invitation messages, recipients and delivery outcomes. |
| Hiring Reporting | `update_analytics`, `report_hiring_metrics` | Hiring counts, trends, conversion, time to final decision, candidate activity and workflow failures. |
| Semantic Discovery | `semantic_search` | Searchable job/candidate information and relevance results. |
| Recruitment Assistance | `recommend_candidates`, `summarize_resume`, `explain_candidate_ranking`, `enhance_job_description`, `answer_job_questions`, `assess_role_fit`, `provide_application_guidance` | Questions, recommendations, summaries, explanations and usage counts. |

## Business Rules

| Area | Rule |
| --- | --- |
| Recruiter removal | Revoke organization access immediately, including for signed-in recruiters. |
| Scheduled recruiter actions | Check the recruiter's current organization access before execution. Removed access defers the action without advancing to the next workflow item. |
| Ownership | Owners may transfer ownership to another member of the same organization. The last owner must appoint another before leaving. |
| Job revisions | Preserve revisions and each application's submitted revision. While an update processes, the previous published revision remains available while admission is open. New applications use the new revision once it is ready. |
| Application acceptance | Check authorized candidate access, job acceptance status, hiring period, capacity and duplicates. Enforce no job-specific eligibility restrictions; scoring follows acceptance. |
| Duplicates | At most one application per candidate per job revision. Reopening alone does not bypass this rule. |
| Withdrawal | Applications cannot be withdrawn; their hiring status can still progress. |
| Hiring duration and capacity | Each job has hiring periods and limits, independent of revisions. Close admission when the period ends or capacity is reached. Concurrent submissions must not exceed capacity. |
| Limit changes | During an active period, acceptance reflects the new limit and current count. A limit change or revision update does not reset the count or remove applications. |
| Reopening | Start a new hiring period with a zero application count. Preserve earlier applications and revision links. |
| Stage changes | Authorized recruiters and owners may skip stages or move backward. Record the previous/new stage, actor and time. |
| Final decisions | Final decisions cannot be corrected for now. Stage movement does not reopen or change a final decision. |
| Organization deletion | Organizations cannot be deleted for now. |

## Non-Functional Requirements

- Handle hiring surges and backpressure; target tens of thousands of concurrent applications and interview events.
- Scale background work separately and keep long-running tasks from blocking user operations. Support non-blocking or streaming AI responses.
- Handle concurrent requests, retries and partial failures without duplicate effects, lost history or incorrect job readiness.
- Protect unrelated capabilities and tenants from resource exhaustion caused by overload elsewhere.
- Provide logs, metrics and traces for publishing, application progress, background tasks and assistants; expose failures for recovery.
- Enforce organization and personal-data permissions across requests, workers, reports and AI retrieval.

Capacity is a target to validate. Numerical response-time, availability and recovery objectives remain unspecified.

## Data and Reporting

- Keep accounts, memberships, jobs, profiles, applications, history, notes and decisions durable and queryable.
- Keep personal profiles separate from organization recruitment records. Candidates see their own application status; recruiters see submitted candidate information only when authorized.
- Published jobs are discoverable across organizations; resumes and private hiring information are not public. Derived data must preserve the same access restrictions.
- Keep application state and history consistent, and reflect changes in reporting without losing or duplicating updates.
- Report active candidates with profiles, recruiters managing postings, active job postings, daily/weekly/monthly applications, interview conversion, time from application to final decision, most-applied jobs, applications per candidate, workflow errors and assistant usage. Distinguish organization figures from platform totals.
- Dashboards auto-refresh every 30 minutes.

Sources: [Overall requirements](../concept/SmartHire%20%E2%80%94%20Intelligent%20Workforce%20Orchestration%20%26%20Recruitment%20Platform.md) and [Part A](../concept/SmartHire%20-%20Part%20A.md). The rules above include user-defined product choices; job-specific eligibility checks from the source are excluded from this scope.
