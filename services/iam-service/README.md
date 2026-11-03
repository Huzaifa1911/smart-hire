# iam-service

SmartHire IAM service foundation for accounts, organizations, and access management.
Currently implements validated configuration, async PostgreSQL session infrastructure,
request logging, error handling, CORS, and a versioned health endpoint. Domain models,
migrations, repositories, authentication, membership logic, and business endpoints
are not implemented.

## Structure

```text
iam-service/
├── app/
│   ├── main.py                 # application factory and engine lifecycle
│   ├── api/v1/router.py        # centralized route registration
│   ├── api/v1/endpoints/health.py
│   ├── core/                   # settings, database, logging, exceptions
│   ├── middlewares/            # CORS and request logging
│   ├── schemas/                # shared contracts and health response
│   ├── models/                 # future IAM persistence models
│   ├── repositories/           # future IAM data access
│   ├── services/               # future business logic
│   └── dependencies/           # future authentication/authorization dependencies
├── tests/
├── .env.example
├── .python-version
├── pyproject.toml
├── uv.lock
├── Makefile
├── Dockerfile
└── docker-compose.yml
```

## Local setup

Prerequisites: uv, Python 3.12, and Docker with Compose for PostgreSQL. Run from this
service directory:

```bash
cp .env.example .env
make setup
make db-up
make run
```

The local API runs on port 8000. PostgreSQL runs on host port 5432, with a dedicated
iam database and persistent volume. Example credentials are local-development
values. Change host ports and matching settings if they are occupied.

Alternatively run both containers:

```bash
docker compose up --build -d
```

Compose maps API host port 8000 to container port 8000. The API container connects to
`iam-postgres:5432`; the local Python process connects to `localhost:5432`.
`make db-down` stops the stack while retaining its database volume. Use
`make COMPOSE=docker-compose db-up` if your installation uses standalone Compose.

## Configuration and API

Settings read `.env` relative to the service working directory. Service variables use
`IAM_`; database variables use `IAM_DB_`. Database user, password, and name
are required. The database URL uses SQLAlchemy URL construction to preserve special
characters and redact passwords in its string representation.

`IAM_BASE_PATH` contains the complete prefix, defaulting to `/iam-service/v1`.
There is no separate API-prefix setting.

| Endpoint | Purpose |
| --- | --- |
| `/iam-service/v1/health` | Service and database health |
| `/iam-service/v1/swagger` | Swagger UI |
| `/iam-service/v1/redoc` | ReDoc |
| `/iam-service/v1/openapi.json` | OpenAPI document |

Health returns HTTP 200 with `UP`/`database: up` or `DEGRADED`/`database: down`.
Clients must inspect the body; it is not a readiness probe that returns HTTP 503.
Database sessions do not automatically commit; future services own transactions.
The engine is disposed on application shutdown. No tables are created on startup.

Request logging records method, path, status, duration, and a generated request ID.
2xx/3xx use INFO; 4xx/5xx use ERROR. Query strings and bodies are not logged.
Middleware responses carry `X-Request-ID`, exposed through CORS. Unhandled exceptions
are logged and re-raised; outer server-generated error responses are not stamped.
Timing excludes full body streaming. The default wildcard CORS setting is for the
baseline; configure explicit origins for deployed clients.

## Validation

```bash
make lint
make test
```

Tests require no PostgreSQL server. They validate health outcomes using a stubbed
ping, service-specific paths, settings and credential handling, request IDs, log levels,
and exception propagation. These checks do not prove live database connectivity or
Docker startup. No migration commands exist until IAM models and migration
tooling are introduced.
