# ── Builder ───────────────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# Install dependencies before copying source for better layer caching
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY maze_solver_with_python/ ./maze_solver_with_python/
RUN uv sync --frozen --no-dev

# ── Runtime ───────────────────────────────────────────────────────────────────
FROM python:3.12-slim

# Tcl/Tk shared libraries required by tkinter
RUN apt-get update \
    && apt-get install -y --no-install-recommends python3-tk \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY maze_solver_with_python/ ./maze_solver_with_python/

# DISPLAY is forwarded from the host at runtime
ENV DISPLAY=:0 \
    PATH="/app/.venv/bin:$PATH"

CMD ["maze"]
