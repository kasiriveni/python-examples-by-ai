"""
Deployment: Docker and containerization.
"""

# This file explains Docker deployment concepts with Python examples

DOCKERFILE_EXAMPLE = '''
# === Multi-stage Dockerfile for Python ===

# Stage 1: Build
FROM python:3.12-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Production
FROM python:3.12-slim

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
'''

DOCKER_COMPOSE_EXAMPLE = '''
# === docker-compose.yml ===
version: "3.9"

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    volumes:
      - ./app:/app
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  pgdata:
'''

DOCKERIGNORE_EXAMPLE = '''
# === .dockerignore ===
__pycache__
*.pyc
*.pyo
.git
.gitignore
.env
.venv
venv/
node_modules/
*.md
tests/
.pytest_cache/
.mypy_cache/
'''

# === Health check endpoint ===
def create_health_check():
    """Example health check for containerized apps."""
    import os
    return {
        "status": "healthy",
        "version": os.environ.get("APP_VERSION", "dev"),
        "environment": os.environ.get("ENV", "development"),
    }

# === Graceful shutdown ===
import signal
import sys

def graceful_shutdown(signum, frame):
    """Handle shutdown signals in containers."""
    print(f"Received signal {signum}, shutting down gracefully...")
    # Close database connections
    # Flush caches
    # Complete in-flight requests
    sys.exit(0)

# Register signal handlers
signal.signal(signal.SIGTERM, graceful_shutdown)
signal.signal(signal.SIGINT, graceful_shutdown)

if __name__ == "__main__":
    print("=== Dockerfile ===")
    print(DOCKERFILE_EXAMPLE)
    print("=== docker-compose.yml ===")
    print(DOCKER_COMPOSE_EXAMPLE)
    print("=== .dockerignore ===")
    print(DOCKERIGNORE_EXAMPLE)
    print("=== Health Check ===")
    print(create_health_check())
