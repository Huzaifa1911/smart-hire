# ADR 0002: Service Boundaries

**Status:** Proposed

**Purpose:** Assign business responsibilities and data to services, and explain the grouping.

## Domain Model

| Concept | Relationship |
| --- | --- |
| Account | Can have candidate access, a personal profile, resumes and organization memberships. |
| Organization | Contains owner/recruiter memberships, invitations and jobs. |
| Job revision | Preserves job content, requirements and stage definitions. A job can have several revisions. |
| Hiring period | Defines a job's duration, capacity and accepted count independently of its revisions. |
| Application | Binds a candidate to a job revision, hiring period and preserved submission. |
| Hiring history | Records an application's progress, notes, interview progress and final decision. |
| Score | Records a result based on the application's submitted resume and job revision. |

## Service Ownership

| Service | Owns | Reason for the Boundary |
| --- | --- | --- |
| Identity & Organization Access | Accounts, sessions, organizations, memberships, roles and invitations. | Account access, membership and ownership rules belong together. |
| Candidate | Personal profiles, skills, resume files and parsing results. | Personal information has a lifecycle independent of organization membership. |
| Job | Job content, revisions, requirements, stage definitions and publishing readiness. | Content processing and discovery need resources separate from application admission. |
| Hiring | Periods, limits, counts, accepted revisions, applications, submission snapshots, progress, history and scores. | Admission and capacity enforce one rule. Progress and scoring use the preserved submission. |
| Notification | Delivery requests, messages, recipients, attempts and outcomes. | Invitations and application receipts share delivery behavior. |
| Analytics | Derived reports and reporting progress. | Reporting queries and calculations need resources separate from operational hiring. |

Identity is the short name for Identity & Organization Access.
Candidate retains personal source data; Hiring preserves what was submitted. Job readiness and Hiring acceptance are separate states.
Notification delivers messages; Identity and Hiring retain the rules that trigger them.

## Service Interactions

Protected services need verified identity and current access information. The enforcement mechanism is not selected.
These exchanges describe information ownership, not endpoints or transport choices.

| From → To | Information or Work |
| --- | --- |
| Job → Hiring | Processed revision content and stage definitions for adoption; preserved revision content for scoring. |
| Hiring → Job | Revision-adoption outcome and application acceptance status. |
| Candidate → Hiring | Submitted candidate information and saved resume parsing results. |
| Identity → Notification | Invitation delivery request. |
| Hiring → Notification | Application receipt request. |
| Identity → Analytics | Account and membership facts. |
| Candidate → Analytics | Profile facts. |
| Job → Analytics | Publication facts. |
| Hiring → Analytics | Hiring-period, acceptance, application, progress and decision facts. |
| Notification → Analytics | Delivery outcomes. |

## Consequences

These boundaries add deployments for one owner. They allow separate resources for major capabilities, not guaranteed isolation of every internal operation.
Notification's independent deployment remains provisional; separate workers may provide sufficient isolation.

Next: [Business workflows](../architecture/workflows/README.md). The [architecture](../architecture/high_level_architecture.md) assigns runtime components to these responsibilities.
