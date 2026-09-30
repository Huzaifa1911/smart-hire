# iam-service

Identity and access management foundation for SmartHire.
It implements configuration, database infrastructure, request logging, error handling, and a
health endpoint. User registration, login, tenants, roles, JWT/JWKS, database models,
and migrations are future work; no authentication contract is introduced here.

## Structure

```text
iam-service/
├── app/
│   ├── __init__.py
│   ├── main.py                 # create_application(), lifespan, middleware
│   ├── core/                   # settings, database, logging, exceptions, constants
│   ├── api/v1/
│   │   ├── router.py           # central route registration
│   │   └── endpoints/health.py # health handler
│   ├── schemas/health.py       # Pydantic response contract
│   ├── models/                 # future SQLAlchemy models
│   ├── repositories/           # future data access
│   ├── services/               # future IAM business rules
│   ├── dependencies/           # future request-scoped IAM dependencies
│   └── middlewares/            # middleware registration and request logging
├── tests/
├── .env.example
├── .python-version
├── pyproject.toml
├── uv.lock
├── Makefile
├── Dockerfile
└── docker-compose.yml
```

Each Python package contains `__init__.py`, including the empty extension layers.
The intended request flow is endpoint → service → repository → model. Schemas define
API contracts; dependencies wire request-scoped resources. `core/database.py` provides
the async SQLAlchemy engine, session factory, declarative base, and `get_db` dependency.
Sessions do not auto-commit: future service operations must define their transaction
boundaries. PostgreSQL is the intended authoritative IAM store once models exist.

## Setup

Prerequisites: uv, Python 3.12 (uv can obtain it), and Docker with Compose for PostgreSQL.
Run these commands from `services/iam-service`:

```bash
cp .env.example .env
make setup
make db-up
make run
```

The API runs on port 8000 and PostgreSQL on port 5432. If these ports are occupied,
change the Compose host mappings, `IAM_DB_PORT`, and the local run port as appropriate.
The example database credentials are for local development.

To run both containers instead:

```bash
docker compose up --build -d
```

`make db-down` stops the Compose stack and retains its database volume.
If Compose is installed as the standalone `docker-compose` command, use
`make COMPOSE=docker-compose db-up` and `docker-compose up --build -d` instead.

## Configuration and API

Settings are validated through `pydantic-settings`; `.env` is read relative to the
service working directory. Service settings use `IAM_`; database settings use
`IAM_DB_`. Database user, password, and name are required. See [.env.example](.env.example).
`IAM_BASE_PATH` contains the complete API prefix and defaults to `/iam-service/v1`.
The paths below use that default.

- Health: `GET /iam-service/v1/health`
- Swagger UI: `/iam-service/v1/swagger`
- ReDoc: `/iam-service/v1/redoc`
- OpenAPI: `/iam-service/v1/openapi.json`

The health endpoint returns HTTP 200 with `status: UP` and
`database: up` when PostgreSQL responds, or `status: DEGRADED` and `database: down`
on connection failure. Callers must inspect the body; this is not a readiness probe
that returns HTTP 503. The engine is disposed on application shutdown.

Request logging emits method, path, status, elapsed time, and a generated request ID.
Responses returned through the middleware carry `X-Request-ID`; CORS exposes that
header to browser clients. 2xx/3xx responses log at INFO, 4xx/5xx at ERROR. Unhandled
exceptions log a 500 access line and are re-raised; their outer server-generated
responses are not stamped by this middleware. Timing excludes full body streaming.

## Development

```bash
make format
make lint
make test
```

Tests use a stubbed database ping and need no running PostgreSQL. They verify both
health outcomes, IAM documentation paths, configuration validation, and credential
handling. Middleware tests cover request IDs, status-based logging, and unhandled exceptions.
The service uses FastAPI, async SQLAlchemy/asyncpg, Pydantic settings, uvicorn, ruff, and pytest.
The Docker image installs runtime dependencies only and runs the installed uvicorn.

No migration command is provided until migration tooling and IAM models exist.
