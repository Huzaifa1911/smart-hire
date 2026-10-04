# iam-service

Identity and access management foundation for SmartHire.
It implements configuration, database infrastructure, request logging, error handling, and a
health endpoint, four IAM database models, and Alembic migrations. Registration, login,
JWT/JWKS, and membership authorization business logic are not implemented. Their API
contracts are declared with Pydantic request/response schemas; new IAM handlers return 501.

## Structure

```text
iam-service/
├── app/
│   ├── __init__.py
│   ├── main.py                 # create_application(), lifespan, middleware
│   ├── core/                   # settings, database, logging, exceptions, constants
│   ├── api/v1/
│   │   ├── router.py           # central route registration
│   │   └── endpoints/         # health plus IAM contract-only handlers
│   ├── schemas/               # Pydantic health/auth/user/organization/invitation contracts
│   ├── models/                 # user, tenant, membership, invitation models
│   ├── repositories/           # async CRUD and entity-specific lookups
│   ├── services/               # future IAM business rules
│   ├── dependencies/           # future request-scoped IAM dependencies
│   └── middlewares/            # middleware registration and request logging
├── migrations/                 # async Alembic environment and versioned schema
├── alembic.ini
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
boundaries. PostgreSQL is the authoritative IAM store. Schema changes are applied explicitly through
Alembic, never through application startup `create_all`.

## Setup

Prerequisites: uv, Python 3.12 (uv can obtain it), and Docker with Compose for PostgreSQL.
Run these commands from `services/iam-service`:

```bash
cp .env.example .env
make setup
make db-up
make migrate
make run
```

The API runs on port 8000 and PostgreSQL on port 5432. If these ports are occupied,
change the Compose host mappings, `IAM_DB_PORT`, and the local run port as appropriate.
The example database credentials are for local development.

To run both containers instead:

```bash
docker compose up --build -d
docker compose exec iam-service /app/.venv/bin/alembic upgrade head
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

## Database models and migrations

- `User`: global account, normalized case-insensitive email uniqueness, independent candidate access.
- `Tenant`: organization name, unique lowercase slug, and lifecycle status.
- `TenantMembership`: one membership per user/organization, with `owner` or `recruiter` role.
- `TenantInvitation`: hashed invitation token, expiry, acceptance state, and inviter membership.

The organization creator must receive an owner membership in the eventual signup transaction;
the database does not automatically create memberships or enforce a single owner.
The inviter foreign key includes the organization ID, preventing cross-organization references.
Pending invitations are unique per organization and normalized email. Expired invitations must
be transitioned out of pending before replacements can be inserted. Authorization, email
verification, token hashing, and invitation acceptance transactions remain service-layer work.

Shared Python enums live in `app/core/enums.py` and can be reused by Pydantic schemas.
SQLAlchemy maps status/role columns to named PostgreSQL enums using their lowercase values,
and returns enum members on reads. The initial migration creates these types; its downgrade
drops them after the tables. Future enum changes require reviewed migrations.
UUIDs are generated on ORM insertion. Creation/update timestamps default in PostgreSQL;
`updated_at` is refreshed by SQLAlchemy updates, not a database trigger. Raw SQL updates must
set it explicitly. Foreign keys restrict deletion of referenced records; no cascade deletion is used.
IAM publishes no events and has no outbox or candidate profile table.

Run from this service directory after configuring `.env`:

```bash
uv run --locked alembic upgrade head
uv run --locked alembic current
uv run --locked alembic check
# After editing models, generate and review the next migration:
uv run --locked alembic revision --autogenerate -m "describe schema change"
# Inspect migration SQL without a PostgreSQL connection:
uv run --locked alembic upgrade head --sql
```

`make migrate` applies pending migrations. Migration files are included in the Docker image.
Migrations use the existing `IAM_DB_*` settings, with no credentials stored in `alembic.ini`.
Unit tests inspect mapping invariants and offline PostgreSQL migration SQL; they do not prove
live PostgreSQL behavior. Run migrations and `alembic check` against PostgreSQL to verify it.


## IAM endpoint contracts

All paths below are relative to `/iam-service/v1`. Health is implemented. These new
routes validate request shape and return `501` with `{"error": "This endpoint is not
implemented yet"}`. Authentication, permission checks, persistence, token issuance,
and invitation delivery are not wired. Swagger documents intended success responses,
not working behavior. Shared contracts live in `schemas/base.py`: `RequestSchema`, `ORMResponse`,
`SuccessResponse[T]`, `ErrorResponse`, and `Page[T]`. Success contracts use
`SuccessResponse[T]` (`success`, `data`);
501 responses use the existing application error shape. Invalid inputs return FastAPI 422.

| Method | Path | Intended behavior |
| --- | --- | --- |
| POST | `/auth/candidate-signup` | Create account with candidate access |
| POST | `/auth/organization-signup` | Create new account, organization, and owner membership |
| POST | `/auth/login` | Authenticate and return account, memberships, and access token |
| GET | `/users/me` | Read current account |
| PATCH | `/users/me` | Update full name |
| PUT | `/users/me/candidate-access` | Idempotently enable candidate access |
| GET | `/users/me/memberships` | List current account's memberships with organization details |
| POST | `/tenants` | Existing user creates an organization with an owner membership |
| GET | `/tenants/{tenant_id}` | Read organization details |
| PATCH | `/tenants/{tenant_id}` | Owner updates organization name |
| GET | `/tenants/{tenant_id}/memberships` | Owner lists organization memberships |
| PATCH | `/tenants/{tenant_id}/memberships/{membership_id}` | Owner changes role/status |
| POST | `/tenants/{tenant_id}/invitations` | Owner invites a recruiter by email |
| GET | `/tenants/{tenant_id}/invitations` | Owner lists invitations |
| POST | `/tenants/{tenant_id}/invitations/{invitation_id}/revoke` | Owner revokes a pending invitation |
| POST | `/invitations/accept` | Authenticated intended recipient accepts an invitation |

List contracts use `offset` (default 0) and `limit` (default 20, maximum 100).
Responses contain `items`, `total`, `offset`, and `limit` inside `data`.
Organization requests select their workspace using `X-Tenant-ID`. The agreed token design
includes organization memberships and roles in a signed access token with a 15-minute
lifetime. Each service must validate the token and selected membership. Refresh must reload
current authorization state; refresh-token contracts and implementation remain future work.
Passwords and invitation tokens use `SecretStr` in request models. Output schemas
exclude password hashes and token hashes. Password strength and account verification
policies remain unresolved; only a nonempty password is required by this contract.
Signup does not accept roles/status flags supplied by clients. Organization signup
is for new accounts; logged-in existing users use `POST /tenants`.

Proposed owner permissions and last-owner protection are described in route contracts;
they must be enforced in the eventual service transactions. Candidate profiles remain
owned by candidate-service. Platform-admin endpoints, token refresh/logout, password
reset, email verification endpoints, tenant lifecycle changes, and slug changes are
outside these initial contracts. Invitation acceptance must eventually verify email,
expiry, state, and intended recipient before changing membership.

Organization slugs accept one lowercase DNS label (1–63 characters, letters/digits
and interior hyphens). `admin`, `api`, `www`, and `auth` are reserved in request
validation. The existing database slug constraint is weaker and has not changed.

## Repositories

Each repository takes an `AsyncSession`. `BaseRepository` provides get, ordered list,
add, save, delete, and count. Writes flush and refresh as needed but never commit or
roll back. The service owns the transaction so account/organization/membership creation
and invitation acceptance can commit atomically. After database errors, the caller must
roll back the transaction. `save` expects a session-managed object.

- `UserRepository`: normalized email lookup/existence and organization-user listing
  through memberships, since users do not have a tenant column.
- `TenantRepository`: slug lookup/existence.
- `TenantMembershipRepository`: tenant-scoped membership lookups, lookup by tenant/user,
  paginated lists/counts by user or tenant, and optional status filters. User listings
  eagerly load organizations for `UserMembershipResponse` without async lazy-loading.
- `TenantInvitationRepository`: tenant-scoped invitation lookup, token-hash lookup,
  pending-email lookup, and paginated lists/counts by tenant and optional status.

`get(..., for_update=True)` and entity-specific locked lookups use `SELECT FOR UPDATE`.
Locks last until the caller's transaction ends. Locked reads refresh an existing
identity-map object. These are building blocks, not complete invitation acceptance or
last-owner protection. Service logic must still validate authorization and transitions.
Existence lookups do not prevent races; database uniqueness constraints remain authoritative.
Pending-email lookup includes expired invitations whose stored status is still pending,
matching the partial unique index and allowing the service to expire them explicitly.

Generic get/list/count methods are global internal operations. Organization endpoints
must use tenant-scoped lookups and enforce access in the service. Repositories do not
perform authentication or authorize callers. No database changes or endpoint wiring were
introduced by the repository layer.

Repository tests validate transaction ownership and PostgreSQL query scope/locking SQL
using mocked sessions. Schema tests serialize actual ORM instances and inspect OpenAPI.
They do not validate live PostgreSQL execution, concurrency, or lock behavior.
