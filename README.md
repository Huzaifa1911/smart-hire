# SmartHire

Backend for **SmartHire** — a multi-tenant workforce-orchestration and recruitment platform.

This repository is **Part A**: the core recruitment and workflow-orchestration system — job and
candidate management, job-publishing and application workflows, event-driven background processing,
analytics, and observability. The GenAI layer (Part B) is out of scope here.

Recruiters (tenant staff) post jobs and run hiring pipelines; candidates (global) register, apply,
and track status. It's a set of event-driven microservices, each owning its own database.

## Repository structure

```
smart-hire/
├── services/
│   ├── iam-service/           # tenants, users (recruiter/candidate), auth (JWT + JWKS)
│   ├── job-service/           # jobs + publishing workflow
│   ├── candidate-service/     # candidate profiles, resumes, skills
│   └── application-service/   # applications, stages, interviews, scoring
├── docs/
│   ├── architecture.md        # system design
│   └── db-schema.md           # data model (ERD)
├── Makefile                   # repo-wide targets (pre-commit hooks)
├── .pre-commit-config.yaml    # shared lint/format hooks (scoped per stack)
└── smart-hire.code-workspace
```

Each service is a FastAPI application with its own `Makefile` (`make setup`, `run`, `test`,
`migrate`), `Dockerfile`, and `docker-compose.yml`.

`notification-service` and `kpi-service` are part of the design (see `docs/architecture.md`) but are
not yet scaffolded.

## Documentation

- **Architecture** — [`docs/architecture.md`](docs/architecture.md)
- **Database schema** — [`docs/db-schema.md`](docs/db-schema.md)

## Stack

Python · FastAPI · PostgreSQL · MongoDB · Redis · Celery + RabbitMQ · Kafka · Temporal ·
OpenTelemetry (Jaeger / Prometheus / Grafana / Loki) · Docker Compose.
