# SmartHire Problem Statement

## Purpose

Answers: **What must SmartHire do to solve its business problems?**

## Business Problems

- Manual hiring work slows recruitment.
- Limited search and insights make suitable candidates hard to find.
- Scattered data and delayed updates produce inconsistent progress and reports.
- Hiring spikes delay user requests and background processing.
- Unreliable background work makes recovery difficult.
- Hiring data provides too few useful insights.

## Business Goals

Reduce manual hiring work. Help candidates find suitable jobs. Keep hiring progress reliable. Give recruiters useful insights.

## Actors and Organization Scope

| Actor / Role | Responsibility |
| --- | --- |
| Candidate | Maintain a personal profile, discover jobs, apply and track their applications. |
| Recruiter | Manage jobs and hiring in organizations where they have access. |
| Organization Owner | Manage organization access and perform authorized recruitment operations. |

An organization is a **tenant**. Keep its private recruitment data separate from other organizations. Shared identity and multiple tenants extend the assignment scope.

One account can have candidate access and recruiter or owner memberships in several organizations. A recruiter can apply to another organization as a candidate.

Their organization cannot see those applications through their recruiter membership. That membership does not grant access to the other organization's hiring data.

## System Operations

### Actor Requests

| Actor | Operations |
| --- | --- |
| Candidate / Recruiter | `register_candidate`, `register_recruiter`, `login`, `logout` |
| Prospective Organization Owner | `create_organization` |
| Organization Member | `view_organization`, `select_organization`, `leave_organization` |
| Organization Owner | `update_organization`, `list_memberships`, `update_membership`, `invite_recruiter`, `revoke_invitation`, `remove_recruiter`, `transfer_ownership` |
| Invited Recruiter | `accept_invitation` |
| Candidate | `create_candidate_profile`, `upload_resume`, `search_jobs`, `view_job`, `apply_to_job`, `track_application` |
| Recruiter / Owner | `post_job`, `update_job`, `upload_job_description`, `define_required_skills`, `manage_hiring_stages`, `publish_job` |
| Recruiter / Owner | `set_hiring_duration`, `set_application_limit`, `reopen_job` |
| Recruiter / Owner | `move_application_stage`, `record_interview_progress`, `record_recruiter_notes`, `record_hiring_decision` |
| Recruiter / Owner | `report_hiring_metrics` |
| Candidate / Recruiter / Owner | `semantic_search` |
| Recruiter / Owner | `recommend_candidates`, `summarize_resume`, `explain_candidate_ranking`, `enhance_job_description` |
| Candidate | `answer_job_questions`, `assess_role_fit`, `provide_application_guidance` |

### Automatic Processing

| Trigger | Operations | Outcome |
| --- | --- | --- |
| Job publishing or update | `extract_job_keywords`, `map_job_skills`, `structure_job_description`, `mark_job_ready` | Save structured content; mark ready only after required processing succeeds. |
| Candidate application | `parse_resume`, `score_candidate`, `send_application_notification` | Process the resume, score the match and confirm application receipt. |
| Organization invitation created | `send_invitation_notification` | Deliver the invitation to the intended recruiter. |
| Hiring period ends or capacity is reached | `close_job` | Close admission to further applications. |
| Hiring data changes | `update_analytics` | Update reports without losing or double-counting changes. |

This design includes core recruitment, semantic search and AI assistance. The source delivery plan separates Part A and Part B. Both remain in design scope.

## Business Capabilities

A capability groups related work and data. A capability does not require a separate service.

| Capability | Work | Data |
| --- | --- | --- |
| Identity & Authentication | Register accounts and control account access. | Accounts, credentials, candidate access and sessions. |
| Organizations & Access | Manage organizations, members and invitations. | Organizations, memberships, roles and invitations. |
| Candidate Profiles & Resumes | Create profiles and process resumes. | Profiles, skills, resumes and extracted information. |
| Job Management & Publishing | Prepare, publish and find jobs. | Jobs, revisions, descriptions, requirements, skills, stage definitions and processing status. |
| Applications & Hiring Progress | Accept applications and manage hiring. | Periods, limits, counts, acceptance status, submitted information, stages, history, notes, interview progress and decisions. |
| Candidate Evaluation | Score candidate matches. | Scores and the job/candidate information used. |
| Notifications | Deliver receipts and invitations. | Messages, recipients and delivery results. |
| Hiring Reporting | Calculate and present hiring measures. | Counts, trends, conversion, hiring time, candidate activity and failures. |
| Semantic Discovery | Find jobs or candidates by meaning. | Search data and relevance results. |
| Recruitment Assistance | Answer questions and provide advice. | Questions, recommendations, summaries, explanations and usage counts. |

## Business Rules

### Organization Access

- Recruiter registration alone does not grant organization access. Accepting a valid invitation establishes membership.
- Organization creation establishes the initial owner membership.
- Revoke organization access immediately when a recruiter is removed. This includes signed-in recruiters.
- Check current organization access before a scheduled recruiter action. If access was removed, defer the action. Do not advance the workflow.
- An owner can transfer ownership to another member of the same organization.
- The last owner must appoint another owner before leaving.
- Organizations cannot be deleted for now.

### Job Revisions

- Preserve each job revision and each application's submitted revision.
- During an update, keep the previous published revision available while the job accepts applications.
- Use the new revision for new applications when that revision is ready.
- Mark a revision ready only after all required processing succeeds.

### Applications and Capacity

- Check candidate access, acceptance status, hiring period, capacity and duplicates before accepting an application.
- Do not apply job-specific eligibility restrictions. Score candidates after acceptance.
- Allow one application per candidate per job revision. Reopening does not permit another application to the same revision.
- Applications cannot be withdrawn.
- Each job has hiring periods and application limits. Keep these separate from content revisions.
- Close acceptance when the period ends or the count reaches the limit. Concurrent submissions must not exceed the limit.
- During an active period, use the changed limit and current count to determine acceptance.
- Limit changes and revision updates do not reset the count or remove applications.
- Reopening starts a new hiring period with a zero count. Preserve earlier applications and their revision links.

### Hiring Progress

- Authorized recruiters and owners can skip stages or move backward.
- Record the previous stage, new stage, actor and time for each change.
- Final decisions cannot be corrected for now. Stage changes cannot reopen or change a final decision.

## Non-Functional Requirements

- Handle hiring spikes. Control incoming work when demand exceeds available capacity.
- Support tens of thousands of concurrent applications and interview events.
- Scale background work separately. Long tasks must not block user operations.
- Support streaming or other non-blocking AI responses.
- Handle concurrent requests, retries and partial failures without duplicate effects or lost history.
- Prevent overload in one capability or tenant from exhausting resources needed by others.
- Provide logs, metrics and traces. Make failures visible for recovery.
- Check organization and personal-data permissions in requests, workers, reports and AI retrieval.

Capacity remains a target to test. Numerical response-time, availability and recovery targets remain unspecified.

## Data and Reporting

### Data

- Keep business records durable and queryable.
- Keep personal profiles separate from organization hiring records.
- Candidates can see their own application status. Recruiters can see submitted information only with organization access and resource permission.
- Make published jobs discoverable across organizations. Keep resumes and private hiring records out of public search.
- Apply the same access rules to reports and AI results.
- Keep application state and history consistent. Update reports without lost or duplicate changes.

### Reports

Report these measures for the permitted organization or platform scope:

- Active candidates with profiles.
- Recruiters who manage postings.
- Active job postings.
- New applications by day, week and month.
- Application-to-interview conversion.
- Average time from application to final decision.
- Most-applied jobs and average applications per candidate.
- Failed workflows and system errors.
- AI assistant usage.

Dashboards must auto-refresh every 30 minutes.

## Sources and Next Document

Sources: [Overall requirements](../concept/SmartHire%20%E2%80%94%20Intelligent%20Workforce%20Orchestration%20%26%20Recruitment%20Platform.md) and [Part A](../concept/SmartHire%20-%20Part%20A.md).

This document includes agreed product choices. These choices exclude job-specific eligibility restrictions from the source requirements.

Next: [ADR 0001 — Architecture Style](../adrs/0001-architecture-style.md).
