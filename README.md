# SmartHire

Backend for TalentSphere Inc.'s workforce orchestration and recruitment platform.
The current scope covers core recruitment workflows and reliable background processing.

Read the [architecture guide](docs/architecture/README.md) for requirements, decisions, workflows and the target system.

## Current repository

```text
smart-hire/
├── services/
│   ├── iam-service/           # runnable FastAPI foundation and local PostgreSQL config
│   ├── job-service/           # empty main.py and README placeholders
│   └── candidate-service/     # FastAPI foundation and local PostgreSQL config
├── docs/
│   ├── concept/              # four preserved source requirements documents
│   ├── architecture/         # reading guide, requirements, workflows and component view
│   └── adrs/                 # architecture decisions and service boundaries
├── AGENTS.md
└── smart-hire.code-workspace
```

IAM currently provides configuration, async database infrastructure, logging, error
handling, and a versioned health endpoint. Authentication and recruitment business
APIs, workflows, events and analytics are not implemented yet.

## IAM foundation

See [IAM setup, API, and development commands](services/iam-service/README.md).

IAM uses the same baseline structure as Candidate. Its API runs on port 8000, with
PostgreSQL on host port 5432. Domain models, migrations, repositories, authentication
and business endpoints are not implemented.

```text
HTTP client → IAM health endpoint → PostgreSQL connectivity check
```

The endpoint reports `UP` when the database responds and `DEGRADED` otherwise.

## Candidate foundation

See [candidate setup, API, and development commands](services/candidate-service/README.md).
Candidate-service provides the same settings, database-session, logging/middleware, and
health foundation. Its API runs locally on port 8001, with PostgreSQL on host port 5433.
Candidate models, migrations, profiles, resumes, and ownership enforcement remain future work.

The scaffold uses Python 3.12, FastAPI, Pydantic settings, async SQLAlchemy with asyncpg,
PostgreSQL, uv, ruff, pytest, and Docker Compose. Future request handlers will follow
endpoint → service → repository → model. Those extension layers currently have no
business implementation. Database transactions for IAM business operations remain
undefined until those operations are built.

## Requirements and delivery

The source documents live in [docs/concept](docs/concept/). They specify PostgreSQL,
a NoSQL database, Redis, Celery/RabbitMQ, Kafka/Schema Registry, Temporal, and
observability tooling for the platform. This scaffold
does not integrate those additional systems. Vendor choices and product policies
remain open where the sources do not settle them.
