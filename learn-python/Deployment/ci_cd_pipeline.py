"""
Deployment: CI/CD pipeline configuration examples.
"""

# This file demonstrates CI/CD concepts and configuration

# === GitHub Actions Workflow ===
GITHUB_ACTIONS_YAML = '''
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
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

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run tests
        run: pytest --cov=src --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install ruff mypy
      - run: ruff check .
      - run: mypy src/

  deploy:
    needs: [test, lint]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
      - uses: actions/checkout@v4
      - name: Deploy to production
        run: echo "Deploying..."
'''

# === Makefile for development ===
MAKEFILE = '''
# Makefile
.PHONY: install test lint format clean run

install:
\tpip install -e ".[dev]"

test:
\tpytest tests/ -v --cov=src

lint:
\truff check .
\tmypy src/

format:
\truff format .

clean:
\tfind . -type d -name __pycache__ -exec rm -rf {} +
\trm -rf .pytest_cache .mypy_cache dist build *.egg-info

run:
\tuvicorn src.main:app --reload --port 8000
'''

# === Pre-commit hooks config ===
PRE_COMMIT_CONFIG = '''
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.9.0
    hooks:
      - id: mypy
'''

# === pyproject.toml ===
PYPROJECT_TOML = '''
[project]
name = "myproject"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "fastapi>=0.110",
    "uvicorn[standard]",
    "sqlalchemy>=2.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-cov",
    "ruff",
    "mypy",
    "pre-commit",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --strict-markers"

[tool.ruff]
target-version = "py312"
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]

[tool.mypy]
python_version = "3.12"
strict = true
'''

if __name__ == "__main__":
    configs = [
        ("GitHub Actions", GITHUB_ACTIONS_YAML),
        ("Makefile", MAKEFILE),
        ("Pre-commit Config", PRE_COMMIT_CONFIG),
        ("pyproject.toml", PYPROJECT_TOML),
    ]

    for name, content in configs:
        print(f"{'='*60}")
        print(f"  {name}")
        print(f"{'='*60}")
        print(content)
