FROM python:3.12-slim AS builder

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./
COPY packages ./packages

RUN uv sync --all-packages --frozen --no-dev

COPY fixtures ./fixtures
COPY scenarios ./scenarios
COPY scripts ./scripts

FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/packages /app/packages
COPY --from=builder /app/fixtures /app/fixtures
COPY --from=builder /app/scripts /app/scripts
COPY --from=builder /app/pyproject.toml /app/pyproject.toml

ENV PATH="/app/.venv/bin:$PATH"
ENV FIXTURE_ROOT=/app/fixtures
ENV AVENIQ_SQLITE_PATH=/data/aveniq.db
ENV CONNECTOR_MODE=fixture
ENV INVESTIGATION_RUN_ENABLED=true
ENV AVENIQ_HOST=0.0.0.0
ENV AVENIQ_PORT=8000

RUN mkdir -p /data

EXPOSE 8000

CMD ["aveniq-api"]
