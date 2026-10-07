# SmartHire project context and agent guidance

## Purpose and current state

SmartHire is TalentSphere Inc.'s Intelligent Workforce Orchestration & Recruitment Platform for fast-scaling enterprises, staffing agencies, and global HR teams. We are building a backend that manages jobs, candidates, and applications; reliably orchestrates hiring workflows; and later adds AI-assisted recruitment intelligence.

The business problems are manual hiring operations, scattered and inconsistent hiring data, poor candidate discovery, unreliable background processing, hiring-season traffic spikes, and underused recruitment data.

This is also a hands-on engineering assignment: understanding and explaining architecture, patterns, failure behavior, and tradeoffs is part of success.

The workspace contains four Markdown source documents in `docs/concept/` and a FastAPI foundation in `services/iam-service/`, adapted from the supplied SmartHire-main application-service structure. IAM includes a versioned health endpoint, validated settings, async SQLAlchemy infrastructure, logging/error handling, uv dependency metadata and lockfile, tests, and local Docker/PostgreSQL configuration. IAM now has User, Tenant, TenantMembership, and TenantInvitation ORM models and an async Alembic initial migration. Authentication and membership business logic are not implemented. IAM has thin async repositories for all four models; writes flush without committing, and services own authorization and transactions. Tenant-scoped membership/invitation lookups and optional row locking are available. IAM endpoint signatures and Pydantic contracts cover signup/login, current user, organizations, memberships, and invitations; these handlers validate requests and return 501 without authentication or persistence. Database constraints include the agreed owner/recruiter membership roles. Shared Python enums live in `app/core/enums.py`; ORM status/role columns use native PostgreSQL enums. The user has also generated an Nx React frontend workspace in `smart-hire-web/`, containing `apps/web` and `packages/core`, `components`, `ui`, `utils`, `types`, and `api`. Workspace dependencies follow the agreed import boundaries, with TypeScript project references synchronized by `nx sync`. The proposed platform admin app has not been generated. Candidate-service now has the matching FastAPI baseline: grouped CANDIDATE_ settings, async database infrastructure, health endpoint, request logging/CORS/error handling, uv metadata/lockfile, baseline tests, and Docker/PostgreSQL configuration (API port 8001, database host port 5433). Candidate domain models, migrations, profile/resume APIs, ownership checks, and file handling are not implemented. The job and application services remain empty entry-point/README placeholders. See `services/iam-service/README.md` for actual setup and validation commands.

## Source documents

Read the relevant source document before making detailed implementation decisions. This file is durable project context, not a replacement for the source requirements.

The Markdown files in `docs/concept/` are the source documentation. They were converted from the original Word documents, preserving document bodies and tracking tables while omitting the generated Word table of contents. The Word files have been removed.

| Document | Purpose |
| --- | --- |
| `docs/concept/SmartHire — Intelligent Workforce Orchestration & Recruitment Platform.md` | Overall product vision, combined requirements, stack, metrics, and expected outcomes. |
| `docs/concept/SmartHire - Part A.md` | Core recruitment backend, workflow orchestration, consistency, scale, and reliability; excludes GenAI. |
| `docs/concept/SmartHire - Part B.md` | AI assistants, semantic retrieval, ranking, and non-blocking AI execution. |
| `docs/concept/SmartHire — Guidelines.md` | Execution approach, five-week milestone plan, submission requirements, and evaluation criteria. |

Use Part A and Part B to interpret phase boundaries and the Guidelines to interpret milestone scope. If requirements conflict or leave an important decision open, document the ambiguity rather than silently inventing a requirement. Preserve the source documents unless asked to edit them.

## Product scope and users

- Recruiters create and update postings, define required skills and hiring stages, upload job descriptions, review candidates, and manage hiring progress. AI capabilities later help with shortlists, summaries, recommendations, explanations, and job-description improvements.
- Candidates register, create profiles, browse jobs, upload resumes, apply, and track application status. AI capabilities later provide role-specific guidance and application improvement suggestions.
- The backend maintains durable, queryable application states, interview progress, recruiter notes, and hiring decisions, and supplies reporting data for dashboards.

The assignment specifies a backend. No frontend framework, UI design, or separate frontend deliverable is specified. Interview scheduling and assessments appear in the business context, but detailed scheduling and assessment subsystems are not defined by the weekly plan; establish their scope before expanding implementation.

## Part A — core recruitment and orchestration

### Job and candidate management

- Support job and candidate management, candidate registration and profiles, job requirements, descriptions, and hiring stages.
- The source requires duplicate-application rules, job-specific eligibility checks, and application limits. The fresh user-defined scope retains duplicates/limits but explicitly excludes job-specific eligibility restrictions.
- Keep updates consistent across the authoritative hiring state and its dashboard and analytics representations.

### Job publishing workflow

On publishing or updating a job:

1. Extract skills and keywords.
2. Break the description into structured components such as requirements, responsibilities, and benefits.
3. Persist structured data for retrieval and downstream search/ranking.
4. Move the job through `processing` to `ready` only after required processing completes.

Temporal orchestrates the publishing workflow. Partial failures must not corrupt publishing state or incorrectly mark a job ready. The complete state machine, update/version behavior, and retry policy remain design decisions.

Part A mentions preparation for semantic indexing, but explicitly excludes GenAI. Build the reliable structured-data foundation here; embedding generation, vector retrieval, and AI ranking belong to Part B. The Week 3 scoring worker may use the basic simulation specified in the Guidelines.

### Candidate application workflow

When a candidate applies:

1. Validate application rules and durably record the application.
2. Initialize hiring stages and preserve application history.
3. Trigger candidate scoring, ultimately involving resume parsing and skill matching.
4. Trigger analytics updates and an application-received notification.

Handle duplicate submissions idempotently, concurrent applications, backpressure, and recovery from partial failures without losing history. Long-running downstream work must execute independently of the main API operation.

### Distributed processing and reliability

Background work includes skill extraction, scoring, analytics, notifications, and preparation for AI indexing and recommendations. It must be independently scalable, traceable, recoverable, and safe against duplicate effects.

The target scale is tens of thousands of concurrent applications and interview events. This is a requirement to design and validate against, not an achieved benchmark. Numerical latency, throughput, availability, and recovery objectives are not yet specified.

## Part B — recruitment intelligence

- Prepare job and resume/candidate data, generate embeddings, integrate a vector database, and build semantic retrieval and candidate-job matching.
- Build a recruiter assistant for candidate recommendations, automatic resume summaries, job-description optimization, and ranking explanations.
- Build a candidate assistant for questions such as role fit, improving an application, and understanding a job requirement.
- Ground assistant responses in relevant retrieved job and candidate data.
- Support streaming or other non-blocking execution for long-running responses.
- Observe assistant interactions and track recruiter queries, candidate queries, and summaries generated.
- Include prompt design, response quality, AI limitations, and evaluation in implementation and documentation.

The documents describe AI as assistance and recommendations; they do not specify autonomous final hiring decisions.

## Specified technology stack

| Area | Specified technologies |
| --- | --- |
| API/backend | Python, FastAPI |
| Data | PostgreSQL, a NoSQL database, Redis |
| Background tasks | Celery with RabbitMQ |
| Events | Kafka with Schema Registry |
| Durable orchestration | Temporal Workflows |
| AI orchestration | LangGraph |
| LLM provider | OpenAI, Groq, or Anthropic; selection is open |
| Semantic retrieval | A vector database; selection is open |
| Observability | OpenTelemetry, Jaeger, Prometheus, Grafana |
| Local infrastructure | Docker, Docker Compose |

Do not present an unselected vendor, library version, ORM, migration tool, or repository layout as an existing project choice. The NoSQL product and its storage responsibilities are also unspecified.

Keep the roles of Temporal, Kafka, and Celery explicit: durable workflow coordination, domain-event distribution, and background task execution respectively. Document ownership and handoffs so that overlapping tools do not create competing state machines or duplicate effects. These responsibility boundaries are implementation guidance; detailed service topology is not prescribed by the documents.

## Required analytics and observability

Product reporting must cover:

- Total candidates: active users who have created profiles.
- Total recruiters: recruiter accounts managing postings.
- Total jobs published: active job postings, per the overall document's definition.
- New applications over time: daily, weekly, and monthly.
- Application-to-interview conversion rate.
- Average time to hire: application to final decision, per the source definition.
- Most-applied jobs.
- Average applications per candidate.
- Failed workflows and system errors, including scoring, notifications, and indexing.
- AI assistant usage in Part B.

Define precise denominators, time windows, and event semantics before implementing aggregations. Do not quietly reinterpret the supplied metric names or definitions.

Provide logs, metrics, and traces across publishing, application progression, background tasks, and later assistant interactions. A component failure must not corrupt global hiring state.

## Delivery milestones

| Week | Scope | Expected deliverables |
| --- | --- | --- |
| 1 — Part A | Foundation and core management | Service structure, job/candidate database schema, management APIs, profile creation, basic posting flow, local environment. |
| 2 — Part A | Applications and publishing | Duplicate handling, eligibility checks, application tracking, reliable application flow, Temporal publishing pipeline, structured job content, processing-to-ready transitions. |
| 3 — Part A | Events and observability | Kafka job/application events; workers for simulated scoring, notifications, and analytics; initialized analytics pipeline; logging, tracing, and metrics. |
| 4 — Part B | Semantic layer | Prepared job/candidate data, job/resume embeddings, vector database integration, indexed data, working semantic search and retrieval. |
| 5 — Part B | Assistants and recommendations | Recruiter and candidate assistants, contextual recommendations and guidance, end-to-end AI operation, streaming or non-blocking responses. |

These are proposed weekly modules, not calendar deadlines or evidence of completion. The intended loop is implementation, mentor review, discussion, refinement, then the next module. Do not claim mentor review has occurred without evidence.

## Documentation and final deliverables

- Create a PRD with key use cases, functional and non-functional requirements, proposed timeline/milestones, and traceability between requirements, features, and deliverables.
- Maintain a clean, modular GitHub repository with meaningful commit messages and organized services/components.
- Provide a README with a project overview, architecture diagram, setup instructions, API overview, and explanation of the technology stack.
- Document services and workflows, data and event flows, important design decisions, assumptions, and tradeoffs.
- Deliver working end-to-end workflows and meaningful test coverage; complete and review all modules.
- Be able to explain system design, failure handling, and technology choices. Evaluation covers design clarity, code quality, stack usage, edge cases, observability, reliability, and depth of understanding.

## Guidance for future implementation work

- Inspect the current repository before acting; keep this file aligned with real implementation and agreed decisions.
- Progress through the foundation before adding AI dependencies to core recruitment flows. Keep domain behavior separate from API, persistence, orchestration, event transport, and AI integration concerns.
- Explicitly identify the authoritative store and transaction boundaries for jobs, applications, stages, and decisions. Document how asynchronous projections converge and recover; do not assume cross-system atomicity.
- Design idempotency at both API submission and worker/event-consumer boundaries. Retries and event redelivery must not duplicate applications, notifications, or analytics effects.
- Define timeout, retry, failure visibility, and recovery behavior for each workflow and external integration. Treat job readiness as an invariant.
- Consider mechanisms such as database constraints, transactional outbox delivery, and deduplication when designing reliability. These are candidate implementation patterns, not already mandated or implemented architecture.
- Correlate API operations, workflows, events, and worker execution in observability. Avoid exposing resume contents, personal candidate data, or secrets in logs and traces.
- Test meaningful behavior: eligibility and limits, concurrent duplicates, state transitions, retry/redelivery, partial failure recovery, and end-to-end flows. For AI, evaluate retrieval relevance, grounded answers, and non-blocking response handling.
- Record actual setup and validation commands once tools exist. Report what was verified and what remains unverified; do not describe simulated behavior as production integration or unmeasured scale as proven capacity.
- Keep PRD traceability, README instructions, architecture notes, and this context file current when behavior or decisions change.

## Open decisions to resolve when relevant

The current architecture study is documented in `docs/architecture/problem_statement.md`
and `docs/adrs/0001-architecture-style.md` / `0002-service-boundaries.md`. The problem
statement records agreed product rules; the ADRs propose architecture and service
boundaries. Keep this work focused on responsibilities,
operations, data and reasons for grouping; defer implementation mechanisms.

Read the study in this order: problem statement, ADR 0001, then ADR 0002.
Use short sentences, active voice, consistent terms and one topic per paragraph.
Apply ASD-STE100 writing principles without claiming formal compliance.
Keep named operations in the problem statement; ADR 0002 assigns capabilities to
services instead of repeating operation lists.

The study includes common identity and multi-tenancy. One account can have candidate
access and recruiter/owner memberships in multiple organizations. Candidate information
is personal; recruitment records are organization-scoped. Recruiter membership must
not expose applications made to another organization.

Key agreed rules:

- Recruiter removal revokes access immediately. Scheduled actions check current access;
  removed access defers execution without advancing the workflow.
- Owners may transfer ownership to another organization member. The last owner must
  appoint another before leaving; organizations cannot be deleted for now.
- Applications bind to preserved job revisions and are unique per candidate/job revision.
  Previous published content remains available while an update processes; new
  applications use the new revision once ready.
- Capacity belongs to the hiring period, independent of revisions. Close at the limit
  or period end. Limit changes affect acceptance without resetting the count;
  reopening starts a new period with zero count and preserves earlier applications.
- Applications cannot be withdrawn. No job-specific eligibility restrictions apply;
  scoring follows acceptance.
- Authorized recruiters/owners may skip stages or move backward; record stage changes
  with actor and time. Final decisions cannot be corrected.
- Dashboard auto-refresh is every 30 minutes. File/retention questions and detailed
  scheduling/assessments are outside the current architecture discussion.

Proposed services are Identity & Organization Access, Candidate, Job, Hiring,
Notification, Analytics and AI services. AI computes evaluations; Hiring owns
applications and their association with evaluation results. Notification delivers
application receipts and organization invitations; Hiring and Identity retain the
business rules that trigger them. AI, semantic retrieval and assistant usage are in
the current design scope. Hiring groups acceptance with periods, limits, counts and
accepting/closed status; Job retains content, revisions and publishing readiness.
ADR 0002 maps service dependencies and the information/work exchanged. Job and
Hiring coordinate the revision used for admission. Keep timing, dependency-failure
behavior and separate boundary-review tables out of this map; they belong to later
workflow/reliability design.
ADR 0002 includes the domain model and reasons supporting the proposed groupings;
there are no separate domain-model or boundary-validation documents.
Notification's independent deployment remains provisional. Publication handoff and
immediate-revocation enforcement still need design; runtime isolation is unverified.
The ADRs remain Proposed. Existing IAM endpoints must not determine fresh boundaries.
Earlier database and expiry-only authorization proposals do not reflect all current
rules; no implementation or migration was requested.

### Earlier Database Proposal

`docs/db-schema.md` records an earlier design: four separate
service databases; global users with organization memberships and independent candidate
capability; event-free IAM; preserved job/resume revisions; local immutable application
pipeline snapshots with relational current state and history; business-key application
uniqueness without an application idempotency-key column; versioned scoring runs.
Notification and reporting workers are proposed modules in application-service, with
IAM reporting data obtained through explicit reconciliation rather than IAM events.
`docs/schema/` contains proposed DDL and role/RLS templates, not deployed tables or
migrations. Product defaults and unresolved policies are explicitly marked in the design.
The repository directory remains `job-service`; the user calls it `jobs-service`.

### Further Design Topics

The source documents leave the following topics unspecified. The agreed product rules
above settle some of them for the current scope; this list must not reopen those rules
or block the service-boundary discussion:

- Service/deployment boundaries, repository structure, API contracts, and detailed data schemas.
- Authentication, recruiter/candidate authorization, organization or tenant isolation, and administrative roles.
- Exact duplicate/reapplication policy, eligibility rules, application limits, stage transitions, and interview scope.
- Ownership of data across PostgreSQL, NoSQL, Redis, and the vector store.
- Resume/job-description file storage, supported formats, parsing strategy, and retention requirements.
- Event schemas, schema evolution, delivery guarantees, idempotency-key design, workflow versioning, and failure recovery policies.
- Provider/vendor choices, embedding model, ranking/scoring method, AI evaluation criteria, and streaming transport.
- Notification provider, deployment destination, CI tooling, security/privacy requirements, and numerical performance targets.

Resolve ordinary implementation choices within the authorized task and document the rationale. Seek clarification when an unresolved choice materially changes product behavior or scope. Do not turn this list into invented requirements or assume every item blocks initial foundation work.

Earlier authentication design: access tokens have a 15-minute lifetime and include organization memberships/roles and candidate capability. Organization requests select context with `X-Tenant-ID`, validated against signed memberships; `/auth/context` has been removed. Its proposal to retain membership access until token expiry is superseded by the immediate-revocation rule in the fresh design. Enforcement remains to be designed and implemented. Refresh tokens must load current authorization state; refresh contracts and implementation remain pending.

Frontend architecture scaffold follows the ros-frontend-core-main reference: web uses src/app with config/services/routing/layouts/pages and injects platform adapters into AppCoreProvider. Core has context/provider/query-client/hooks modules. API has APIClient facade, Axios RequestHandler, empty IamApiClient, auth lifecycle/store/refresh extension points, and transport utils. Types are grouped under api/common/services; interfaces/types use type-only exports, and fixed value sets use exported string enums; utils has common/phone/schemas extension points. Components and feature pages now implement the account/workspace screen UI; UI follows the reference ui-web structure with per-component folders/barrels, shared utils/styles and components.json. It implements Button/Card/Input/Label, form and phone wrappers, icons, themed toast infrastructure, AlertActions and cn; OTP input is excluded. Tailwind 4 theme styles are compiled by the web Vite plugin. Phone helpers live in utils and require international country calling codes. No endpoint methods are implemented. Web storage/navigation/alert adapters are implemented with localStorage, named React Router navigation and Sonner/native confirmation. Auth initialization is a no-op and route guards remain unwired. Account/workspace screens are UI only: props supply display data and callbacks, web pages compose features and wire navigation, React Hook Form and shared fields handle form UI, and utils owns field validation functions. No mock accounts, memberships, seeded invitation data, simulated authentication, account-flow provider/hooks or success toasts remain. All screen routes are directly accessible. Backend actions and form submissions remain disabled until callbacks are supplied. Candidate workspace switching is a presentation prop and hidden by default. Frontend ESLint enforces separated library/workspace/local import groups and code spacing; workspace boundaries cover TS/JS module extensions as well. Provider context uses individual dependencies to preserve stable values. Reference architecture is adopted but reference business behavior/contracts are not copied. See smart-hire-web/README.md for connections and validation commands.
