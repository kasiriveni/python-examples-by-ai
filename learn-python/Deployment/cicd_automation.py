"""
Deployment: CI/CD pipeline configuration and automation patterns.
"""
# This file contains configuration templates, shell command recipes,
# and Python-based CI/CD helpers — all runnable without external deps.

import subprocess
import os
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

# ═══════════════════════════════════════════
# 1. GitHub Actions workflow templates
# ═══════════════════════════════════════════
CI_WORKFLOW = """
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, dev]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: "pip"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov ruff mypy

      - name: Lint (ruff)
        run: ruff check .

      - name: Type check (mypy)
        run: mypy src/ --ignore-missing-imports

      - name: Run tests
        run: pytest tests/ -v --cov=src --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml

  publish:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    permissions:
      id-token: write     # OIDC trusted publishing (no API key)
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: "3.12"}
      - run: pip install build
      - run: python -m build
      - uses: pypa/gh-action-pypi-publish@release/v1
"""

CD_DEPLOY_WORKFLOW = """
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    tags: ["v*.*.*"]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production

    steps:
      - uses: actions/checkout@v4

      - name: Build Docker image
        run: docker build -t myapp:${{ github.ref_name }} .

      - name: Push to registry
        run: |
          echo "${{ secrets.REGISTRY_PASS }}" | docker login -u ${{ secrets.REGISTRY_USER }} --password-stdin
          docker tag myapp:${{ github.ref_name }} registry.example.com/myapp:${{ github.ref_name }}
          docker push registry.example.com/myapp:${{ github.ref_name }}

      - name: Deploy via SSH
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.PROD_HOST }}
          username: ${{ secrets.PROD_USER }}
          key: ${{ secrets.SSH_KEY }}
          script: |
            cd /opt/myapp
            docker compose pull
            docker compose up -d --remove-orphans
            docker system prune -f
"""

# ═══════════════════════════════════════════
# 2. GitLab CI template
# ═══════════════════════════════════════════
GITLAB_CI = """
# .gitlab-ci.yml
image: python:3.12

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

cache:
  paths: [.cache/pip]

stages:
  - lint
  - test
  - build
  - deploy

lint:
  stage: lint
  script:
    - pip install ruff mypy
    - ruff check .
    - mypy src/ --ignore-missing-imports

test:
  stage: test
  script:
    - pip install -r requirements.txt pytest pytest-cov
    - pytest tests/ -v --cov=src --cov-report=term-missing
  coverage: '/TOTAL.*\\s+(\\d+%)$/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml

build:
  stage: build
  script:
    - pip install build
    - python -m build
  artifacts:
    paths: [dist/]
  only:
    - tags

deploy:
  stage: deploy
  script:
    - echo "Deploying version $CI_COMMIT_TAG"
    - ./scripts/deploy.sh $CI_COMMIT_TAG
  environment:
    name: production
    url: https://myapp.example.com
  only:
    - tags
"""

# ═══════════════════════════════════════════
# 3. Python-based release automation
# ═══════════════════════════════════════════
@dataclass
class ReleaseConfig:
    repo_path: Path = field(default_factory=Path.cwd)
    changelog_file: str = "CHANGELOG.md"
    version_file: str = "src/__init__.py"
    main_branch: str = "main"

def run_cmd(cmd: list[str], cwd: Path | None = None, dry_run: bool = True) -> str:
    """Run a shell command (dry_run prints but doesn't execute)."""
    display = " ".join(cmd)
    if dry_run:
        print(f"  [DRY-RUN] {display}")
        return f"(dry-run output for: {display})"
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, check=True)
    return result.stdout.strip()

class ReleaseAutomation:
    STEPS: list[tuple[str, Callable]] = []

    def __init__(self, version: str, cfg: ReleaseConfig | None = None, dry_run: bool = True):
        self.version = version
        self.cfg = cfg or ReleaseConfig()
        self.dry_run = dry_run
        self._log: list[str] = []

    def _run(self, cmd: list[str]) -> str:
        return run_cmd(cmd, cwd=self.cfg.repo_path, dry_run=self.dry_run)

    def bump_version(self) -> None:
        print(f"\n  [Step] Bump version to {self.version}")
        self._run(["sed", "-i", f"s/__version__ = .*/__version__ = '{self.version}'/",
                   self.cfg.version_file])
        self._log.append(f"Bumped version to {self.version}")

    def run_tests(self) -> None:
        print(f"\n  [Step] Run tests")
        self._run(["python", "-m", "pytest", "tests/", "-q"])
        self._log.append("Tests passed")

    def build_package(self) -> None:
        print(f"\n  [Step] Build distribution")
        self._run(["python", "-m", "build"])
        self._log.append("Package built")

    def tag_release(self) -> None:
        tag = f"v{self.version}"
        print(f"\n  [Step] Git tag {tag}")
        self._run(["git", "add", "-A"])
        self._run(["git", "commit", "-m", f"chore: release {tag}"])
        self._run(["git", "tag", "-a", tag, "-m", f"Release {tag}"])
        self._run(["git", "push", "origin", self.cfg.main_branch, "--tags"])
        self._log.append(f"Tagged {tag}")

    def publish_pypi(self, repository: str = "pypi") -> None:
        print(f"\n  [Step] Publish to {repository}")
        self._run(["python", "-m", "twine", "upload",
                   "--repository", repository, "dist/*"])
        self._log.append(f"Published to {repository}")

    def release(self) -> None:
        print(f"\n{'='*50}")
        print(f"  Release automation for v{self.version}")
        print(f"  Mode: {'DRY RUN' if self.dry_run else 'LIVE'}")
        print(f"{'='*50}")
        for step in [self.run_tests, self.bump_version, self.build_package,
                     self.tag_release, self.publish_pypi]:
            step()
        print(f"\n  ✓ Release complete: {self._log}")

# ═══════════════════════════════════════════
# 4. Environment parity check
# ═══════════════════════════════════════════
def env_parity_check(expected_vars: list[str]) -> dict[str, bool]:
    """Verify required environment variables are set."""
    return {var: var in os.environ and bool(os.environ[var]) for var in expected_vars}

REQUIRED_PROD_VARS = [
    "DATABASE_URL", "SECRET_KEY", "REDIS_URL",
    "ALLOWED_HOSTS", "SENTRY_DSN", "AWS_ACCESS_KEY_ID"
]

if __name__ == "__main__":
    print("=== CI/CD Configuration Templates ===")
    print(f"\n--- GitHub Actions CI ---")
    print(CI_WORKFLOW[:400], "...\n")

    print(f"\n--- GitLab CI ---")
    print(GITLAB_CI[:300], "...\n")

    print("\n=== Release Automation (dry-run) ===")
    automator = ReleaseAutomation(version="1.2.3", dry_run=True)
    automator.release()

    print("\n=== Environment Parity Check ===")
    results = env_parity_check(REQUIRED_PROD_VARS)
    for var, present in results.items():
        status = "✓" if present else "✗ MISSING"
        print(f"  {var:30s}: {status}")
    missing = [v for v, ok in results.items() if not ok]
    if missing:
        print(f"\n  WARNING: {len(missing)} env vars missing (expected for dev environment)")
