# ADR 0002: Service Boundaries

Status: Proposed

## Purpose

Group operations and data by business responsibility. Keep related decisions together and separate capabilities that benefit from independent scaling or isolation.

## Proposed Boundaries

| Service | Operations | Data It Controls | Reason for the Boundary |
| --- | --- | --- | --- |
| Identity & Organization Access | `register_candidate`, `register_recruiter`, `login`, `logout`, `create_organization`, `view_organization`, `select_organization`, `update_organization`, `list_memberships`, `update_membership`, `invite_recruiter`, `revoke_invitation`, `accept_invitation`, `remove_recruiter`, `transfer_ownership`, `leave_organization` | Accounts, credentials, sessions, candidate access, organizations, memberships, roles and invitations. | One identity serves candidates and recruiters. Membership and ownership rules belong together. |
| Candidate | `create_candidate_profile`, `upload_resume`, `parse_resume` | Personal profiles, skills, resumes and parsing results. | Candidate information has its own lifecycle. Profile changes are separate from account and membership changes. |
| Job | `post_job`, `update_job`, `upload_job_description`, `define_required_skills`, `manage_hiring_stages`, `publish_job`, `extract_job_keywords`, `map_job_skills`, `structure_job_description`, `mark_job_ready`, `search_jobs`, `view_job` | Job descriptions, revisions, requirements, skills, stage definitions and publishing progress. | These define the advertised opportunity. Content processing and browsing can scale separately from application handling. |
| Hiring | `set_hiring_duration`, `set_application_limit`, `reopen_job`, `close_job`, `apply_to_job`, `track_application`, `move_application_stage`, `record_interview_progress`, `record_recruiter_notes`, `record_hiring_decision` | Hiring periods, limits, counts, accepting/closed status, the revision used for admission, applications, stage history, interview progress, notes, decisions and links to evaluation results. | Capacity and the decision to accept an application belong together. Hiring also controls its progression and decisions. |
| Notification Service | `send_application_notification`, `send_invitation_notification` | Message templates, delivery requests, recipients, attempts and delivery outcomes. | Application receipts and organization invitations share delivery responsibilities; provider failures should be separate from hiring and membership changes. |
| Analytics Service | `update_analytics`, `report_hiring_metrics` | Derived hiring metrics and reporting data, with organization/platform scope. | Reporting queries and aggregation should have capacity separate from operational hiring. |
| AI Service | `score_candidate`, `semantic_search`, `recommend_candidates`, `summarize_resume`, `explain_candidate_ranking`, `enhance_job_description`, `answer_job_questions`, `assess_role_fit`, `provide_application_guidance` | Evaluation results, derived search data, assistant interactions, recommendations, summaries, explanations and usage counts. | Skill matching, ranking, retrieval and assistance share recruitment intelligence. Their computation can evolve and scale separately from application handling. |

## Important Distinctions

- **Identity versus Candidate:** Identity controls who a person is and their access. Candidate controls their profile and resume. One person can recruit for one organization and apply to another.
- **Job versus Hiring:** Job controls content and revision readiness. Hiring controls accepting/closed status, capacity, the revision used for admission and applications. Job and Hiring coordinate publication. A ready revision does not by itself mean the job is accepting applications.
- **Stage definitions versus stage progress:** Job defines available stages. Hiring records each application's actual stage and history.
- **Resume parsing versus evaluation:** Candidate controls parsed resume information. AI computes evaluation results; Hiring associates the relevant result with the application and job revision. Scoring does not determine application acceptance.
- **Notification intent versus delivery:** Hiring decides when an application receipt is needed; Identity decides when an invitation is needed. Notification Service delivers both and records the outcome. Invitation validity remains Identity's responsibility.
- **Source data versus derived results:** Analytics owns reporting data; AI owns evaluation and assistant results. Both use authorized source information without owning jobs, profiles or hiring decisions.

## Interaction Map

These are information and work dependencies; they do not specify communication mechanisms.

| Operation | Services Involved | Information or Work Exchanged |
| --- | --- | --- |
| Create a profile or upload a resume | Identity → Candidate | Verified identity and candidate access. |
| Protected organization action | Identity → Job, Hiring, Analytics or AI | Current organization membership and role; each service checks its own resource permissions. |
| Publish or update a job | Job → Hiring | Published revision and stage definitions; agreement on the revision used for new applications. |
| Apply to a job | Job, Candidate → Hiring | Published revision and submitted candidate/resume information. |
| Show job availability | Hiring → Job | Accepting/closed status. |
| Score an application | Hiring, Job, Candidate → AI → Hiring | Evaluation request, submitted job revision, parsed resume and evaluation result. |
| Send an application receipt | Hiring → Notification | Application receipt delivery request. |
| Invite a recruiter | Identity → Notification | Invitation delivery request; Identity retains invitation validity and membership rules. |
| Update and read reports | Identity, Candidate, Job, Hiring, AI → Analytics | Recruitment facts and assistant usage for reporting. |
| Search or use an assistant | Job, Candidate, Hiring → AI | Authorized recruitment information for retrieval and guidance. |

## Scope and Tradeoffs

These are proposed service groupings, not one service per actor or tenant. Evaluation and delivery run in the background; their failures must not undo accepted applications or recorded invitations. AI includes ordinary skill matching as well as AI-assisted functions; scoring need not use an LLM.

The proposal adds deployment work for one owner. It separates major capabilities but does not isolate every operation inside a service. Job browsing/publishing and AI retrieval/assistance may need finer separation if their workloads justify it.

Business rules are recorded in the [problem statement](../architecture/problem_statement.md). The map defines required collaboration; delivery guarantees, access-check ordering and publication handoff still need detailed design. No database, endpoint or messaging choice is made here. Capacity and failure isolation have not been verified.
