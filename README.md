# PFM Backend Demo

A sanitized personal finance backend demo built with FastAPI, PostgreSQL, SQLAlchemy, Alembic, Docker Compose, Ruff, and GitHub Actions.

This repository is intentionally separated from the original product codebase. It demonstrates backend architecture, data integrity, authentication, testing, and containerized local development without exposing private business logic, real banking integrations, tokens, or user data.

## What This Demo Shows

- FastAPI application structure with routers, schemas, models, and services.
- JWT-based authentication flow.
- PostgreSQL persistence with SQLAlchemy models.
- Alembic migrations for database schema management.
- Budget and transaction domain examples.
- Database-level uniqueness constraints for financial records.
- Health checks for app and database readiness.
- Docker Compose local environment.
- Ruff linting and automated tests in GitHub Actions.

## What Was Removed

- Real bank provider integrations.
- Production secrets and `.env` values.
- Client-specific business logic.
- Real user data.
- Private product names and implementation details.

## Tech Stack

- Python 3.12
- FastAPI
- SQLAlchemy 2
- Alembic
- PostgreSQL 16
- Pydantic Settings
- Ruff
- unittest
- Docker Compose
- GitHub Actions

## Quick Start

Copy the environment template:

```bash
cp backend/.env.example backend/.env
```

Start the stack:

```bash
docker compose up --build
```

Open:

```text
http://localhost:8000/docs
http://localhost:8000/health
http://localhost:8000/health/db
```

## Local Backend Checks

From `backend/`:

```bash
poetry install
poetry run ruff check app tests
poetry run python -m unittest discover -s tests
```

## Example API Flow

Register:

```http
POST /auth/register
```

Login:

```http
POST /auth/login
```

Create a monthly budget:

```http
POST /budgets
```

List mock transactions:

```http
GET /transactions
```

Read monthly summary:

```http
GET /summary?month=2026-09
```

## Portfolio Note

This demo focuses on code organization and backend engineering practices. It is not a full production product and does not contain proprietary integrations or private business logic.
