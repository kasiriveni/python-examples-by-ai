"""
Deployment: CI/CD pipeline patterns with Docker, health checks, and migrations.
"""
import os
import json
import hashlib
import subprocess
from pathlib import Path
from dataclasses import dataclass, field
from typing import Callable

# ═══════════════════════════════════════════
# 1. Docker patterns
# ═══════════════════════════════════════════
DOCKERFILE_PYTHON = """
# Multi-stage build for minimal production image
# ─────────────────────────────────────────────
FROM python:3.11-slim AS base

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \\
    curl ca-certificates && \\
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ─────────────────────────────────────────
FROM base AS builder

# Install build deps
RUN pip install --upgrade pip

# Cache dependency layer separately from app code
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ─────────────────────────────────────────
FROM base AS production

# Copy only installed packages (not build tools)
COPY --from=builder /install /usr/local

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser
WORKDIR /app
RUN chown appuser:appuser /app

USER appuser

# Copy application
COPY --chown=appuser:appuser . .

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8000/health || exit 1

# Signal handling for graceful shutdown
STOPSIGNAL SIGTERM

EXPOSE 8000
CMD ["python", "-m", "gunicorn", "app:application", \\
     "--bind", "0.0.0.0:8000", \\
     "--workers", "2", \\
     "--worker-class", "uvicorn.workers.UvicornWorker"]
"""

DOCKER_COMPOSE = """
version: "3.9"

services:
  app:
    build:
      context: .
      target: production
    ports:
      - "8000:8000"
    environment:
      - APP_ENV=production
      - DATABASE_URL=postgresql://user:pass@db:5432/app
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    restart: unless-stopped
    networks:
      - backend

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: app
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d app"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - backend

  redis:
    image: redis:7-alpine
    networks:
      - backend

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/ssl/certs:ro
    depends_on:
      - app
    networks:
      - backend

volumes:
  pgdata:

networks:
  backend:
    driver: bridge
"""

# ═══════════════════════════════════════════
# 2. Database migration runner
# ═══════════════════════════════════════════
@dataclass
class Migration:
    version: str
    description: str
    up_sql:   str
    down_sql: str

    def checksum(self) -> str:
        return hashlib.sha256(self.up_sql.encode()).hexdigest()[:16]

@dataclass
class MigrationRunner:
    """Tracks and applies database migrations."""
    migrations: list[Migration] = field(default_factory=list)
    applied: set[str] = field(default_factory=set)

    def add(self, migration: Migration) -> "MigrationRunner":
        self.migrations.append(migration)
        return self

    def pending(self) -> list[Migration]:
        return [m for m in self.migrations if m.version not in self.applied]

    def run_up(self, dry_run: bool = False) -> list[str]:
        """Apply all pending migrations in order."""
        applied = []
        for m in self.pending():
            if dry_run:
                print(f"  [DRY RUN] Would apply {m.version}: {m.description}")
            else:
                print(f"  Applying {m.version}: {m.description}")
                # Would execute: conn.execute(m.up_sql)
                self.applied.add(m.version)
                applied.append(m.version)
        return applied

    def rollback(self, steps: int = 1, dry_run: bool = False) -> list[str]:
        """Roll back the most recently applied migrations."""
        rolled = []
        applied_sorted = sorted(
            [m for m in self.migrations if m.version in self.applied],
            key=lambda m: m.version, reverse=True
        )
        for m in applied_sorted[:steps]:
            if dry_run:
                print(f"  [DRY RUN] Would rollback {m.version}")
            else:
                print(f"  Rolling back {m.version}: {m.description}")
                self.applied.discard(m.version)
                rolled.append(m.version)
        return rolled

# ═══════════════════════════════════════════
# 3. Health check framework
# ═══════════════════════════════════════════
from enum import Enum

class HealthStatus(str, Enum):
    HEALTHY   = "healthy"
    DEGRADED  = "degraded"
    UNHEALTHY = "unhealthy"

@dataclass
class HealthCheck:
    name: str
    check: Callable[[], bool]
    timeout_ms: int = 5000
    critical: bool = True

@dataclass
class HealthResult:
    name: str
    status: HealthStatus
    latency_ms: float = 0.0
    message: str = ""
    critical: bool = True

def run_health_checks(checks: list[HealthCheck]) -> dict:
    import time
    results: list[HealthResult] = []

    for hc in checks:
        start = time.perf_counter()
        try:
            ok = hc.check()
            latency = (time.perf_counter() - start) * 1000
            status = HealthStatus.HEALTHY if ok else HealthStatus.UNHEALTHY
            msg = "ok" if ok else "check returned False"
        except Exception as e:
            latency = (time.perf_counter() - start) * 1000
            status = HealthStatus.UNHEALTHY
            msg = str(e)

        results.append(HealthResult(hc.name, status, round(latency, 2), msg, hc.critical))

    # Overall status
    if any(r.status == HealthStatus.UNHEALTHY and r.critical for r in results):
        overall = HealthStatus.UNHEALTHY
    elif any(r.status != HealthStatus.HEALTHY for r in results):
        overall = HealthStatus.DEGRADED
    else:
        overall = HealthStatus.HEALTHY

    return {
        "status": overall.value,
        "checks": [
            {"name": r.name, "status": r.status.value,
             "latency_ms": r.latency_ms, "message": r.message}
            for r in results
        ],
    }

# ═══════════════════════════════════════════
# 4. Deploy script skeleton
# ═══════════════════════════════════════════
DEPLOY_SCRIPT = """#!/usr/bin/env bash
set -euo pipefail

IMAGE="${DOCKER_REGISTRY}/${APP_NAME}:${VERSION}"

echo "=== Building image ==="
docker build --target production -t "$IMAGE" .

echo "=== Running tests ==="
docker run --rm "$IMAGE" python -m pytest tests/ -q

echo "=== Pushing image ==="
docker push "$IMAGE"

echo "=== Deploying ==="
kubectl set image deployment/${APP_NAME} app="$IMAGE" --record

echo "=== Waiting for rollout ==="
kubectl rollout status deployment/${APP_NAME} --timeout=120s

echo "=== Health check ==="
sleep 5
curl -f "${APP_URL}/health" || { kubectl rollout undo deployment/${APP_NAME}; exit 1; }

echo "=== Deploy complete ==="
"""

if __name__ == "__main__":
    print("=== Dockerfile (multi-stage build) ===")
    print(DOCKERFILE_PYTHON[:400], "...\n")

    print("=== Docker Compose ===")
    print(DOCKER_COMPOSE[:300], "...\n")

    print("=== Migration Runner ===")
    runner = MigrationRunner()
    runner.add(Migration("001", "Create users table",
                         "CREATE TABLE users (id SERIAL PRIMARY KEY, email TEXT)",
                         "DROP TABLE users"))
    runner.add(Migration("002", "Add created_at column",
                         "ALTER TABLE users ADD COLUMN created_at TIMESTAMP",
                         "ALTER TABLE users DROP COLUMN created_at"))
    runner.add(Migration("003", "Create posts table",
                         "CREATE TABLE posts (id SERIAL, user_id INT, body TEXT)",
                         "DROP TABLE posts"))

    print(f"  Pending (before): {len(runner.pending())}")
    runner.run_up()
    print(f"  Pending (after up): {len(runner.pending())}")
    runner.rollback(steps=1)
    print(f"  After rollback(1): applied={runner.applied}")

    print("\n=== Health Checks ===")
    checks = [
        HealthCheck("database",   lambda: True,  critical=True),
        HealthCheck("redis",      lambda: True,  critical=True),
        HealthCheck("disk_space", lambda: True,  critical=False),
        HealthCheck("api_upstream", lambda: False, critical=False),  # degraded
    ]
    result = run_health_checks(checks)
    print(json.dumps(result, indent=2))

    print("\n=== Deploy Script Snippet ===")
    print(DEPLOY_SCRIPT[:400])
