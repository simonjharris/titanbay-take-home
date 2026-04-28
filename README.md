# Titanbay Take-Home: Private Markets Fund API

## Overview

REST API for managing private market funds and investor commitments.

**Stack:** Python 3.13, FastAPI, PostgreSQL, SQLAlchemy, Alembic, uv

---

## Quickstart

```shell
docker compose up
```

- Starts API on `http://localhost:8000` and PostgreSQL on `5432`
- Migrations run automatically on container start
- No manual setup required
- No seed data is provided, but the `POST /funds`, `POST /investors`, and `POST /funds/{fund_id}/investments` endpoints can be used to create test data, or interact via the Swagger UI at `http://localhost:8000/docs`. Data will persist in the database between runs. Tests create their own ephemeral data against a separate test database and clean up after themselves.

---

## Running Locally (without Docker)

Using docker compose is the recommended way to run this, but if you wish to run outside docker (maybe for easier debugging) then this can be done as follows.

The app requires a postgres database running. If you don't have a suitable one set up, you can run `docker compose up database` to run only the postgres container.

The `DATABASE_URL` environment variable must then be configured. Copy `.env.example` to `.env` and adjust as needed, or export it directly.

```shell
cp .env.example .env
uv sync
export DATABASE_URL=postgresql://titanbay:titanbay@localhost:5432/titanbay
uv run alembic upgrade head
uv run uvicorn main:app --reload
```

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/funds` | List all funds |
| `GET` | `/funds/{fund_id}` | Get fund by ID |
| `POST` | `/funds` | Create a fund |
| `PUT` | `/funds` | Update a fund (ID in request body, per spec — see note below) |
| `GET` | `/investors` | List all investors |
| `POST` | `/investors` | Create an investor |
| `GET` | `/funds/{fund_id}/investments` | List investments for a fund |
| `POST` | `/funds/{fund_id}/investments` | Create an investment |

> **Note on `PUT /funds`:** The spec places the fund `id` in the request body rather than the path. This is non-standard — a more conventional design would be `PUT /funds/{fund_id}` — but the spec was followed as-is.

Full schema: [API spec](https://storage.googleapis.com/interview-api-doc-funds.wearebusy.engineering/index.html)

Interactive docs available at:
  - `http://localhost:8000/docs` (Swagger UI).
  - `http://localhost:8000/redoc` (Redoc)

---

## Data Model

- **Fund** — `name`, `vintage_year`, `target_size_usd`, `status` (`Fundraising` | `Investing` | `Closed`)
- **Investor** — `name`, `investor_type` (`Individual` | `Institution` | `FamilyOffice`), `email` (unique)
- **Investment** — joins Fund and Investor; `amount_usd`, `investment_date`; 

---

## Error Handling

| Status | When                                                                             |
|--------|----------------------------------------------------------------------------------|
| `201 Created` | Successful resource creation                                                     |
| `400 Bad Request` | Business rule violation (e.g. investing in a non-Fundraising fund)               |
| `404 Not Found` | Resource with given ID does not exist                                            |
| `409 Conflict` | Application or database constraint violation (e.g. investor with existing email) |
| `422 Unprocessable Entity` | Request body fails input validation (missing fields, wrong types, etc.)          |

---

## Formatting, Linting and Type Checking

[uv](https://docs.astral.sh/uv/) is required for running the following commands.

The following command will install the project dependencies.
```shell
uv sync
```

Ruff is used for both formatting and linting.
```shell
uv run ruff format .
uv run ruff check .
```

Mypy is used for type checking, with strict mode enabled.

```shell
uv run mypy .
```

## Testing
Testing also requires a postgres database to be running with the TEST_DATABASE_URL environment set. This has a default set in `config.py` which may or may not be appropriate depending on how the database is running. This can be overridden in a `.env` file as per the `.env.example`.

```shell
uv run pytest --cov
```

---


## Design Decisions & Assumptions

Data models and routes were set up according to the provided [api spec](https://storage.googleapis.com/interview-api-doc-funds.wearebusy.engineering/index.html).

Additional data validation requirements were identified.

 - An investment can only be created in a fund if the fund status is "Fundraising".
 - A unique constraint was added to the `email` field on the `investors` table, meaning multiple investors can't share an email address.

The logic of these rules should be checked to see if that is the desired behaviour. Additional data validation requirements may exist, but require product input.

---

## AI Usage

The general project outline and endpoint stubs were created by hand using previous projects as a guide to enable quick set up of docker and testing setups. The `/funds` endpoints were mostly created by hand as a template for AI to follow to create the others.

Most of the business logic was written by AI, with a few iterations around better controlling the database transaction through the HTTP request lifecycle. 
Most of the tests were written by AI, after a few written by hand as a template.

AI was then used to review the project and find any bugs: one found (see commit `a0eb88cc`).
