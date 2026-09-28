# SmartHire — Intelligent Workforce Orchestration & Recruitment Platform [Part - A]

TalentSphere Inc. is building SmartHire, a next-generation workforce orchestration and recruitment automation platform designed for fast-scaling enterprises, staffing agencies, and global HR teams. As the customer base has grown and hiring volume has accelerated, the organization has hit multiple limitations in their current systems:

- Job posting, candidate evaluation, and interview operations are heavily manual and slow.

- Recruiters struggle to identify top candidates because the platform lacks intelligent search, contextual ranking, and AI-driven candidate insights.

- Hiring workflows (screening, assessments, interview scheduling, updates) are inconsistent and error-prone due to scattered data and asynchronous processes.

- High traffic during hiring campaigns causes delays in interview scheduling, candidate shortlisting, and background task processing.

- Rich hiring data (assessment scores, candidate interactions, system logs) is not being utilized for insights, predictions, or recruiter assistance.

To address these challenges, TalentSphere is commissioning a new backend system for SmartHire with the following goals.

## Description / Problem Statement

This part focuses on building the core recruitment and workflow orchestration system of SmartHire. It addresses challenges around scalability, consistency, workflow automation, and reliability in job publishing, candidate applications, and hiring pipelines.

The goal is to solve:

- Manual and slow hiring workflows

- Data inconsistency across jobs, candidates, and hiring stages

- High latency during hiring spikes

- Unreliable background task execution

- Lack of observability and failure recovery

This layer ensures a scalable, event-driven, and consistent backend system, excluding GenAI capabilities.

## Business Goals & Vision

SmartHire must deliver:

### A powerful job & candidate management system

- Recruiters can create job postings, define required skills, upload job descriptions, and manage hiring stages.

- Candidates can browse jobs, apply, upload resumes, and track application status.

### A scalable hiring workflow automation engine

- Creating or updating a job should trigger processes like keyword extraction, skills mapping, and semantic indexing.

- Candidate applications should trigger stage initialization, scoring, notifications, and analytics updates.

### Reliable consolidated hiring data

- Application states, interview progress, recruiter notes, and decisions must be durable, queryable, and always consistent.

### Seamless real-time interactions

- The platform must gracefully handle high load during recruitment drives and campus hiring seasons.

### A foundation for long-term scale

- Support tens of thousands of concurrent applications and interview events.

- Background tasks must run reliably even during intense hiring periods.

## Core Functional Requirements

### 1. Job & Candidate Management

- Creating and updating job postings, requirements, descriptions, and hiring stages

- Candidate registration and profile creation

- Candidate applications to jobs, with rules regarding:

    - Duplicate applications

    - Job-specific eligibility checks

    - Application limits

Ensuring every update remains consistent across hiring stages, recruiter dashboards, and analytics.

### 2. Job Publishing Workflow

When a recruiter publishes or updates a job:

- Extract skills and keywords from the description for search and ranking.

- Break down the job description into components (requirements, responsibilities, benefits).

- Store structured data for fast retrieval, search, and ranking models.

- Mark the job as ready only after all processing is complete.

- Partial failures must not corrupt the publishing pipeline.

### 3. Candidate Application Workflow

When a candidate applies to a job:

- Record the application and initialize the hiring workflow stages.

- Trigger candidate scoring (resume parsing, skills match score).

- Update analytics dashboards.

- Send notifications (e.g., “Application Received”).

Workflow must handle:

- Large volumes during hiring drives

- Idempotency for duplicate submissions

- Backpressure handling

- Recovery from partial failures without losing application history

### 4. Distributed & Event-Driven Behaviors

Certain actions trigger dependent background tasks, such as:

- Skill extraction after job publishing

- Candidate scoring post-application

- Analytics updates

- Email notifications

- Data preparation for AI ranking and recommendations

These tasks must:

- Run independently from main API operations

- Be traceable and recoverable

- Avoid double-processing

- Gracefully handle failure

- Scale during hiring spikes

### 5. Analytics Metrics for SmartHire

- Total Candidates

- Total Recruiters

- Total Jobs Published

- New Applications Over Time

- Application-to-Interview Rate

- Average Time to Hire

- Most Applied Jobs

- Average Applications per Candidate

- Failed Workflows / System Errors

### 6. System Observability & Reliability Expectations

SmartHire must support:

- Clear separation of concerns between domain components

- Full observability (logs, metrics, traces) for:

    - Job publishing workflows

    - Application progression workflows

    - Background tasks

Failure in one part of the system must not affect global consistency.

## Expected Outcomes

- Support full job lifecycle operations

- Reliable workflow execution (publishing, scoring, notifications)

- High scalability during hiring spikes

- Strong consistency and fault tolerance

- Clean, maintainable architecture

- PRD Requirement

    - Key use-cases

    - Functional and non-functional requirements

    - Timeline / milestones

    - Traceability between features and deliverables

## Tech Stack

### Backend:

- Python, FastAPI

- PostgreSQL

- NoSQL DB

- Redis

- Celery + RabbitMQ

- Kafka + Schema Registry

- Temporal Workflows

### Observability:

- Prometheus + Grafana

- Jaeger

- OpenTelemetry

### DevOps:

- Docker

- Docker Compose
