SHELL := /bin/bash
.DEFAULT_GOAL := help
.PHONY: help setup install format lint test run db-up db-down migrate clean
COMPOSE ?= docker compose

help:
	@echo "iam-service — commands"
	@echo "  make setup     - create Python 3.12 venv and install all dependencies (uv)"
	@echo "  make install   - sync all dependency groups"
	@echo "  make format    - format and autofix with ruff"
	@echo "  make lint      - check formatting and lint"
	@echo "  make test      - run tests without a database"
	@echo "  make run       - run the service on :8000 with reload"
	@echo "  make db-up     - start local Postgres on :5432"
	@echo "  make migrate   - apply IAM Alembic migrations"
	@echo "  make db-down   - stop the local Compose stack"

setup:
	@command -v uv >/dev/null 2>&1 || { echo "Install uv before running make setup."; exit 1; }
	@uv venv --python 3.12
	@uv sync --locked --all-groups

install:
	@uv sync --locked --all-groups

format:
	@uv run --locked ruff format ./app ./tests
	@uv run --locked ruff check --fix ./app ./tests

lint:
	@uv run --locked ruff format --check ./app ./tests
	@uv run --locked ruff check ./app ./tests

test:
	@uv run --locked pytest

run:
	@uv run --locked uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

db-up:
	@$(COMPOSE) up -d iam-postgres

migrate:
	@uv run --locked alembic upgrade head

db-down:
	@$(COMPOSE) down

clean:
	@rm -rf .venv .pytest_cache .ruff_cache .coverage
