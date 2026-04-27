FROM python:3.13-slim
ENV TZ=Europe/London
WORKDIR /app
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY uv.lock pyproject.toml /app
RUN uv sync --no-install-project
COPY . /app
EXPOSE 8000
CMD uv run alembic upgrade head && uv run uvicorn main:app --host 0.0.0.0