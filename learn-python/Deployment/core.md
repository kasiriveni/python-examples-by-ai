# Core Python Concepts

## Core Themes
- CI and CD pipelines, containerization, and runtime configuration.
- Server deployment with Docker, Gunicorn, Nginx, and Kubernetes.
- Monitoring, metrics, code quality, and production operations.

## Core Theme Examples
- Example 1: Write GitHub Actions workflows for test and build steps.
- Example 2: Create Dockerfiles with layers and Nginx reverse proxy config.
- Example 3: Configure logging and collect application metrics.

## Files and Concepts
- cicd_automation.py: GitHub Actions style automation, tests, deployment scripting
- ci_cd_pipeline.py: pipeline configuration, matrix testing, automated delivery flows
- code_quality_tools.py: ruff linting, mypy type checking, code-analysis tooling
- config_management.py: environment-specific config, dataclass-based settings
- docker_and_migrations.py: multi-stage Docker builds, health checks, migration patterns
- docker_deployment.py: Dockerfile design, docker-compose, service containerization
- gunicorn_and_nginx.py: WSGI and ASGI serving, reverse proxy setup, worker tuning
- kubernetes_patterns.py: deployment manifests, pod resources, cluster deployment basics
- monitoring_and_metrics.py: JSON logging, metrics collection, production observability

## Core Example
This example loads environment-based configuration and emits a startup log.

```python
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app")

environment = os.getenv("APP_ENV", "development")
port = int(os.getenv("PORT", "8000"))
logger.info("starting env=%s port=%s", environment, port)
```
