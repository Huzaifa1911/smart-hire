# SmartHire — Execution Guidelines

## 1. Objective of This Assignment

This assignment is designed as a hands-on learning experience to help engineers across Backend, Frontend, QA, DevOps, and Platform roles build real-world system design skills.

The goal is not just to implement features, but to:

- Understand how large-scale recruitment systems are designed

- Learn workflow orchestration and event-driven architecture

- Build systems that handle scale, consistency, and failures

- Gain confidence working with the defined tech stack

- Apply practical design principles in real scenarios

Think of this as an opportunity to learn by building production-like systems.

## 2. Execution Approach

### Module-Based Progression

The assignment is divided into weekly modules.

To get the best learning outcome:

- Try to complete one module per week

- Share your work for mentor feedback

- Refine your implementation based on feedback before moving forward

This ensures a strong foundation before building advanced features.

### Weekly Milestone Flow

Each week can follow this simple loop:

1. Work on the assigned milestone

2. Submit your implementation for review

3. Discuss feedback with your mentor

4. Refine your solution

5. Proceed to the next module

This approach encourages continuous learning and iteration.

### Mentor Collaboration

Mentors are here to guide you. During reviews:

- Walk through your design decisions

- Explain your approach

- Share challenges or tradeoffs

Reviews will focus on:

- Clarity of design

- Correct use of patterns

- Understanding of system behavior

## 3. Submission Guidelines

### GitHub Repository

- Maintain a clean and modular codebase

- Use meaningful commit messages

- Keep services/components well organized

### README

Your README should include:

- Project overview

- Architecture diagram

- Setup instructions

- API overview

- Tech stack explanation

### Technical Documentation

Include documentation covering:

- Service and workflow breakdown

- Data flow and event flow

- Key design decisions

- Assumptions and tradeoffs

## 4. Learning Expectations

Focus on understanding the “why” behind the system design, not just implementation.

### For Part A (Core Recruitment Platform)

- Event-driven architecture

- Workflow orchestration (Temporal)

- Idempotency and consistency

- Async processing (Kafka, Celery)

- Handling high-load systems

### For Part B (GenAI Layer)

- Embeddings and semantic search

- Candidate-job matching (RAG-like patterns)

- Prompt design and response quality

- Streaming responses

- AI limitations and evaluation

## 5. Part A — Execution Plan (3 Weeks)

### Focus: Core Recruitment Platform + Workflow Orchestration

This part focuses on building a scalable and reliable hiring system, handling job lifecycle and candidate workflows.

### 🟢 Week 1 — Foundation + Core Management

#### Scope

- Initial architecture setup

- Job & Candidate management (CRUD)

- Candidate profile creation

- Basic job posting flow

#### Deliverables

- Service structure defined

- Database schema for jobs and candidates

- APIs for job and candidate management

- Local environment setup

### 🟡 Week 2 — Application Workflow + Publishing Pipeline

#### Scope

- Candidate application workflow:

    - Duplicate handling

    - Eligibility checks

    - Application tracking

- Job publishing workflow (Temporal):

    - processing → ready lifecycle

- Job content breakdown (skills, requirements, etc.)

#### Deliverables

- Application workflow working reliably

- Publishing workflow orchestrated

- Job state transitions handled

### 🔴 Week 3 — Event-Driven System + Observability

#### Scope

- Kafka-based event system:

    - job published events

    - application events

- Background workers:

    - candidate scoring (basic simulation)

    - notifications

    - analytics updates

- Observability:

    - logging

    - tracing

    - metrics

#### Deliverables

- Event-driven workflows operational

- Analytics pipeline initialized

- Basic observability setup

### Part A — Weekly Tracking Table

| Week | Focus Area | What to Aim For | Done |
| --- | --- | --- | --- |
| Week 1 | Foundation & Management | Job + candidate APIs, DB schema, system setup |  |
| Week 2 | Application & Workflows | Stable application flow + publishing workflow |  |
| Week 3 | Events & Observability | Async processing + system visibility |  |

## 6. Part B — Execution Plan (2 Weeks)

### Focus: AI-Powered Recruitment Intelligence

This part enhances the platform with intelligent matching, recommendations, and assistance.

### 🟣 Week 4 — Data Preparation + Semantic Layer

#### Scope

- Job and candidate data preparation

- Embedding generation (jobs + resumes)

- Vector database integration

- Semantic retrieval setup

#### Deliverables

- Jobs and candidates indexed

- Semantic search working

- Retrieval pipeline functional

### 🔵 Week 5 — AI Assistant + Recommendations

#### Scope

- Recruiter assistant:

    - candidate recommendations

    - resume summaries

- Candidate assistant:

    - job guidance

    - application improvement suggestions

- Streaming or non-blocking responses

#### Deliverables

- AI assistant working end-to-end

- Context-aware recommendations

- Smooth response handling

### Part B — Weekly Tracking Table

| Week | Focus Area | What to Aim For | Done |
| --- | --- | --- | --- |
| Week 4 | Semantic Layer | Indexed data + working retrieval system |  |
| Week 5 | AI Assistant | End-to-end recommendations + guidance |  |

## 7. Final Deliverables Checklist

Before completing the assignment:

- All modules are completed and reviewed

- Codebase is clean and well-structured

- README and documentation are complete

- End-to-end workflows are working

- You can confidently explain your system

## 8. Evaluation Approach

Evaluation will consider:

- System design clarity

- Code quality and structure

- Use of the tech stack

- Handling of edge cases

- Observability and reliability

- Depth of understanding
