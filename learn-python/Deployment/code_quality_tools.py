"""
Deployment: Static analysis and code quality tooling configuration.
"""
# All config shown as string templates — runnable for demo output.

# ═══════════════════════════════════════════
# 1. pyproject.toml tool sections
# ═══════════════════════════════════════════
PYPROJECT_QUALITY = """
[tool.ruff]
target-version = "py311"
line-length = 100

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
    "S",   # flake8-bandit (security)
    "ANN", # flake8-annotations (type hints)
    "SIM", # flake8-simplify
]
ignore = ["ANN101", "ANN102", "E501"]

[tool.ruff.lint.per-file-ignores]
"tests/*" = ["S101", "ANN"]  # allow assert in tests

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
line-ending = "auto"

[tool.mypy]
python_version = "3.11"
strict = true
ignore_missing_imports = true
disallow_untyped_defs = true
disallow_any_generics = true
warn_return_any = true
warn_unused_ignores = true
exclude = ["tests/"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --tb=short -p no:warnings"
markers = [
    "slow: marks tests as slow",
    "integration: marks integration tests",
    "unit: marks unit tests",
]

[tool.coverage.run]
source = ["src"]
omit = ["tests/*", "*/migrations/*"]
branch = true

[tool.coverage.report]
show_missing = true
fail_under = 80
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
    "@abstractmethod",
]
"""

# ═══════════════════════════════════════════
# 2. pre-commit hooks
# ═══════════════════════════════════════════
PRE_COMMIT_CONFIG = """
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-toml
      - id: check-merge-conflict
      - id: detect-private-key
      - id: no-commit-to-branch
        args: [--branch, main]

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.3.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.9.0
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]

  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.7
    hooks:
      - id: bandit
        args: [-r, src/, -ll]  # -ll = medium severity and above

  - repo: local
    hooks:
      - id: pytest-check
        name: pytest
        entry: pytest tests/ -q --no-header
        language: system
        pass_filenames: false
        always_run: true
"""

# ═══════════════════════════════════════════
# 3. Makefile / task runner
# ═══════════════════════════════════════════
MAKEFILE = """
# Makefile for Python project
.PHONY: install lint format type-check test cov clean build

install:
\tpip install -e ".[dev]"
\tpre-commit install

lint:
\truff check .
\tbandit -r src/ -ll

format:
\truff format .
\truff check --fix .

type-check:
\tmypy src/

test:
\tpytest tests/ -v

cov:
\tpytest tests/ --cov=src --cov-report=html --cov-report=term-missing
\t@echo "Open htmlcov/index.html"

clean:
\trm -rf dist/ build/ .eggs/ *.egg-info
\trm -rf .mypy_cache .pytest_cache .ruff_cache htmlcov
\tfind . -type d -name __pycache__ -exec rm -rf {} +

build: clean
\tpython -m build

release: build
\tpython -m twine upload dist/*
"""

# ═══════════════════════════════════════════
# 4. Bandit security scan helper
# ═══════════════════════════════════════════
import ast
import re

SECURITY_PATTERNS = {
    "hardcoded_password":       re.compile(r'(password|passwd|secret|api_key)\s*=\s*["\'][^"\']+["\']', re.I),
    "sql_format_string":        re.compile(r'execute\s*\(["\'].*%(s|d).*["\']'),
    "subprocess_shell_true":    re.compile(r'subprocess\.(run|call|check_output).*shell\s*=\s*True'),
    "debug_mode":               re.compile(r'debug\s*=\s*True', re.I),
    "md5_sha1":                 re.compile(r'hashlib\.(md5|sha1)\b'),
    "assert_in_production":     re.compile(r'^\s*assert\b', re.M),
    "random_not_secrets":       re.compile(r'\brandom\.(randint|choice|random)\b'),
}

def scan_source(code: str, filename: str = "<source>") -> list[dict]:
    findings = []
    for rule_name, pattern in SECURITY_PATTERNS.items():
        for match in pattern.finditer(code):
            line_no = code[:match.start()].count("\n") + 1
            findings.append({
                "rule":     rule_name,
                "file":     filename,
                "line":     line_no,
                "snippet":  match.group()[:80].strip(),
                "severity": "HIGH" if "password" in rule_name or "sql" in rule_name else "MEDIUM",
            })
    return findings

# ═══════════════════════════════════════════
# 5. Complexity checker
# ═══════════════════════════════════════════
def cyclomatic_complexity(source: str) -> dict[str, int]:
    """Estimate cyclomatic complexity per function."""
    BRANCH_NODES = (ast.If, ast.For, ast.While, ast.ExceptHandler,
                    ast.With, ast.Assert, ast.BoolOp)
    results = {}
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            complexity = 1
            for child in ast.walk(node):
                if isinstance(child, BRANCH_NODES):
                    complexity += 1
                elif isinstance(child, ast.BoolOp):
                    complexity += len(child.values) - 1
            results[node.name] = complexity
    return results

SAMPLE_CODE = '''
import random

password = "admin123"  # hardcoded!

def login(user, pw):
    import subprocess
    subprocess.run(["ls", "-la"], shell=True)
    if user == "admin":
        assert pw == password
    return True

def fetch(query):
    db.execute("SELECT * FROM users WHERE name = %s" % query)
'''

if __name__ == "__main__":
    print("=== pyproject.toml quality config ===")
    print(PYPROJECT_QUALITY[:400], "...\n")

    print("=== pre-commit config ===")
    print(PRE_COMMIT_CONFIG[:300], "...\n")

    print("=== Makefile ===")
    print(MAKEFILE[:300], "...\n")

    print("=== Security Scanner ===")
    findings = scan_source(SAMPLE_CODE, "sample.py")
    for f in findings:
        print(f"  [{f['severity']:6}] {f['rule']:30} line {f['line']}: {f['snippet']!r}")

    print("\n=== Cyclomatic Complexity ===")
    code = '''
def simple(x):
    return x + 1

def complex_fn(a, b, c):
    if a > 0:
        for i in range(b):
            if i % 2 == 0 or c:
                try:
                    pass
                except ValueError:
                    pass
    return a
'''
    for fn, cc in cyclomatic_complexity(code).items():
        risk = "low" if cc <= 5 else "medium" if cc <= 10 else "HIGH"
        print(f"  {fn}: CC={cc} ({risk})")
