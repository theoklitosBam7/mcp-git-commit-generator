# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS uv

# Install the project into `/app`
WORKDIR /app

# First copy only the required files for dependency installation
COPY pyproject.toml uv.lock ./

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev --no-editable

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-editable

RUN uv pip install .

FROM python:3.13-slim-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/* \
    && adduser --disabled-password --gecos '' --uid 1000 appuser
COPY --from=uv --chown=appuser:appuser /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

RUN chown -R appuser:appuser /app
USER appuser

ENTRYPOINT ["mcp-git-commit-generator", "--transport", "stdio"]
