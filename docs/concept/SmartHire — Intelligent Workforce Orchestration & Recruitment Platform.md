# SmartHire — Intelligent Workforce Orchestration & Recruitment Platform

TalentSphere Inc. is building SmartHire, a next-generation workforce orchestration and recruitment automation platform designed for fast-scaling enterprises, staffing agencies, and global HR teams. As the customer base has grown and hiring volume has accelerated, the organization has hit multiple limitations in their current systems:

- Job posting, candidate evaluation, and interview operations are heavily manual and slow.

- Recruiters struggle to identify top candidates because the platform lacks intelligent search, contextual ranking, and AI-driven candidate insights.

- Hiring workflows (screening, assessments, interview scheduling, updates) are inconsistent and error-prone due to scattered data and asynchronous processes.

- High traffic during hiring campaigns causes delays in interview scheduling, candidate shortlisting, and background task processing.

- Rich hiring data (assessment scores, candidate interactions, system logs) is not being utilized for insights, predictions, or recruiter assistance.

To address these challenges, TalentSphere is commissioning a new backend system for SmartHire with the following goals.

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

### An AI-powered recruitment assistant

- Recruiters can ask for candidate shortlists, resume summaries, recommendation scores, or job description enhancements.

- Candidates can ask questions about job roles or receive personalized guidance during application.

### Seamless real-time interactions

- AI-driven tasks (candidate ranking, descriptions, insights) may be long-running and must not block recruiters.

- The platform must gracefully handle high load during recruitment drives and campus hiring seasons.

### A foundation for long-term scale

- Support tens of thousands of concurrent applications and interview events.

- Background tasks must run reliably even during intense hiring periods.

## Core Functional Requirements

### 1. Job & Candidate Management

The platform must support:

- Creating and updating job postings, requirements, descriptions, and hiring stages.

- Candidate registration and profile creation.

- Candidate applications to jobs, with rules regarding:

    - Duplicate applications

    - Job-specific eligibility checks

    - Application limits

- Ensuring every update remains consistent across hiring stages, recruiter dashboards, and analytics.

### 2. Job Publishing Workflow

When a recruiter publishes or updates a job:

- Extract skills and keywords from the description for search and ranking.

- Break down the job description into components (requirements, responsibilities, benefits).

- Store structured data for fast retrieval, semantic search, and ranking models.

- Mark the job as ready only after all processing is complete.

- Partial failures must not corrupt the publishing pipeline.

### 3. Candidate Application Workflow

When a candidate applies to a job:

- Record the application and initialize the hiring workflow stages.

- Trigger candidate scoring (resume parsing, skills match score).

- Update analytics dashboards.

- Send notifications (e.g., “Application Received”).

- Workflow must handle:

    - Large volumes during hiring drives

    - Idempotency for duplicate submissions

    - Backpressure handling

    - Recovery from partial failures without losing application history

### 4. Intelligent Recruitment Assistant

SmartHire must include two AI-driven capabilities:

#### A. Recruiter Assistant

Recruiters can request:

- Top candidate recommendations

- Automatic resume summaries

- Job description optimization

- Candidate ranking explanations

The assistant retrieves relevant candidate/job data and generates meaningful responses.

#### B. Candidate Guidance Assistant

Candidates can ask:

- “Am I a good fit for this role?”

- “How should I improve my application?”

- “What does this requirement mean?”

The assistant provides context-aware, job-specific advice.
Responses may require streaming or long-running reasoning.

### 5. Distributed & Event-Driven Behaviors

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

### 6. Analytics Metrics for SmartHire

SmartHire must provide reporting for:

1. Total Candidates – Active users who have created profiles.

2. Total Recruiters – Recruiter accounts managing postings.

3. Total Jobs Published – Count of active job postings.

4. New Applications Over Time – Per day/week/month.

5. Application-to-Interview Rate – Conversion rate across jobs.

6. Average Time to Hire – Duration from application to final decision.

7. Most Applied Jobs – Jobs receiving the highest applications.

8. Average Applications per Candidate – Activity level metrics.

9. AI Assistant Usage – Count of recruiter queries, candidate queries, summaries generated.

10. Failed Workflows / System Errors – Failed tasks across scoring, notifications, indexing.

### 7. System Observability & Reliability Expectations

SmartHire must support:

- Clear separation of concerns between domain components

- Full observability (logs, metrics, traces) for:

    - Job publishing workflows

    - Application progression workflows

    - Intelligent assistant interactions

    - Background tasks

Failure in one part of the system must not affect global consistency.

## Tech Stack

### Backend

- Python, FastAPI

- PostgreSQL

- NoSQL DB

- Redis

- Celery + RabbitMQ

- Kafka + Schema Registry

- Temporal Workflows

### AI

- LangGraph

- LLM Provider (OpenAI / Groq / Anthropic)

- Vector Database

### Observability & Monitoring

- Prometheus + Grafana

- Jaeger

- OpenTelemetry

### DevOps

- Docker

- Docker Compose

## Expected Outcomes

By the end of the assignment, the SmartHire backend should:

- You must also create a Product Requirements Document (PRD) outlining:

    - Key use-cases

    - Functional and non-functional requirements

    - A proposed implementation timeline/milestones

    - Clear traceability between features, requirements, and deliverables

- Support all major job lifecycle operations from posting to application processing.

- Reliably execute background workflows (publishing, scoring, notifications, indexing).

- Provide a powerful intelligent assistant to both recruiters and candidates.

- Scale to support high-volume hiring campaigns.

- Demonstrate architectural excellence in:

    - Clean code

    - Modular design

    - Workflow orchestration

    - Fault tolerance

    - Documentation quality

    - Test coverage

- Additionally, this exercise is being given to upskill you, meaning the goal is not only to complete the required milestones, but also to deeply learn and understand the core concepts of the architectural patterns, design principles, and the underlying tech stack involved.
