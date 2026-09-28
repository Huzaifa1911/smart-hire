# SmartHire — Intelligent Workforce Orchestration & Recruitment Platform [Part - B]

TalentSphere Inc. is building SmartHire, a next-generation workforce orchestration and recruitment automation platform designed for fast-scaling enterprises, staffing agencies, and global HR teams. As the customer base has grown and hiring volume has accelerated, the organization has hit multiple limitations in their current systems:

- Job posting, candidate evaluation, and interview operations are heavily manual and slow.

- Recruiters struggle to identify top candidates because the platform lacks intelligent search, contextual ranking, and AI-driven candidate insights.

- Hiring workflows (screening, assessments, interview scheduling, updates) are inconsistent and error-prone due to scattered data and asynchronous processes.

- High traffic during hiring campaigns causes delays in interview scheduling, candidate shortlisting, and background task processing.

- Rich hiring data (assessment scores, candidate interactions, system logs) is not being utilized for insights, predictions, or recruiter assistance.

To address these challenges, TalentSphere is commissioning a new backend system for SmartHire with the following goals.

## Description / Problem Statement

This part focuses on enabling AI-driven recruitment intelligence in SmartHire.

The goal is to solve:

- Difficulty in identifying top candidates

- Lack of contextual candidate-job matching

- No automated recruiter assistance

- Poor candidate guidance during application

- Underutilized hiring data

This layer introduces:

- AI-powered candidate ranking and recommendations

- Resume summarization and job optimization

- Context-aware candidate guidance

- Semantic understanding using embeddings

- Streaming AI responses

## Business Goals & Vision

### An AI-powered recruitment assistant

- Recruiters can ask for candidate shortlists, resume summaries, recommendation scores, or job description enhancements.

- Candidates can ask questions about job roles or receive personalized guidance during application.

### Seamless real-time interactions

- AI-driven tasks (candidate ranking, descriptions, insights) may be long-running and must not block recruiters.

## Core Functional Requirements

### Job Publishing Workflow (GenAI Scope)

When a recruiter publishes or updates a job:

- Extract skills and keywords from the description for semantic search and ranking.

- Store structured data for semantic search and ranking models.

- Data preparation for AI ranking and recommendations

### Intelligent Recruitment Assistant

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

- Responses may require streaming or long-running reasoning

### Analytics Metrics

- AI Assistant Usage – Count of recruiter queries, candidate queries, summaries generated

### System Observability & Reliability

- Observability for intelligent assistant interactions

## Expected Outcomes

- AI-powered recruiter assistant

- Intelligent candidate guidance system

- Semantic search and ranking

- Scalable AI processing with non-blocking execution

- PRD Requirement

    - Key use-cases

    - Functional and non-functional requirements

    - Timeline / milestones

    - Traceability between features and deliverables

## Tech Stack

- LangGraph

- LLM Provider (OpenAI / Groq / Anthropic)

- Vector Database
