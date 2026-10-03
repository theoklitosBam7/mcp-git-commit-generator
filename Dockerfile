# syntax=docker/dockerfile:1.7
FROM python:3.14.8-slim-trixie AS builder

COPY --from=ghcr.io/astral-sh/uv:0.12.21 /uv /uvx /bin/

WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0

COPY pyproject.toml uv.lock README.md ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project --no-dev --no-editable

COPY src ./src
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-editable

FROM python:3.14.8-slim-trixie AS runtime

LABEL org.opencontainers.image.source="https://github.com/theoklitosBam7/mcp-git-commit-generator" \
      org.opencontainers.image.description="Generate Conventional Commit messages from staged Git changes using MCP." \
      org.opencontainers.image.licenses="MIT"

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates git \
    && rm -rf /var/lib/apt/lists/* \
    && adduser --disabled-password --gecos '' --uid 1000 appuser

WORKDIR /app
COPY --from=builder --chown=appuser:appuser /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

USER appuser
ENTRYPOINT ["mcp-git-commit-generator"]
CMD ["--transport", "stdio"]
