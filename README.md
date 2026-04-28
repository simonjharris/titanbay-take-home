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

---

## Running Locally (without Docker)

Using docker compose is the recommended way to run this, but if you wish to run outside docker (maybe for easier debugging) then this can be done as follows.

The app requires a postgres database running. If you don't have a suitable one set up, you can run `docker compose up database` to run only the postgres container.

The `DATABASE_URL` environment variable must then be configured. This can also be set with a `.env` file in the project root.


```shell
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
| `PUT` | `/funds` | Update a fund |
| `GET` | `/investors` | List all investors |
| `POST` | `/investors` | Create an investor |
| `GET` | `/funds/{fund_id}/investments` | List investments for a fund |
| `POST` | `/funds/{fund_id}/investments` | Create an investment |

Full schema: [API spec](https://storage.googleapis.com/interview-api-doc-funds.wearebusy.engineering/index.html)

Interactive docs available at:
  - `http://localhost:8000/docs` (Swagger UI).
  - `http://localhost:8000/redoc` (Redoc)

---

## Data Model

- **Fund** — `name`, `vintage_year`, `target_size_usd`, `status` (`Fundraising` | `Investing` | `Closed`)
- **Investor** — `name`, `investor_type` (`Individual` | `Institution` | `FamilyOffice`), `email` (unique)
- **Investment** — joins Fund and Investor; `amount_usd`, `investment_date`; one investment per investor per fund (enforced)

---

## Testing
Testing also requires a postgres database to be running with the TEST_DATABASE_URL 

```shell
uv run pytest --cov
```

---

## Design Decisions & Assumptions

[...]

---

## AI Usage

[...]
