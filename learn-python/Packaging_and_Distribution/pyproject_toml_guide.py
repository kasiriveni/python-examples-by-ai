"""
Packaging and Distribution: pyproject.toml patterns and PEP 517/518 build system.
"""

# ─────────────────────────────────────────────────────────
# PYPROJECT.TOML examples
# ─────────────────────────────────────────────────────────

PYPROJECT_MODERN = '''
# pyproject.toml — Modern Python packaging (PEP 518 / 621)
# Build with: python -m build
# Install   : pip install .
# Upload    : twine upload dist/*

[build-system]
requires      = ["hatchling"]
build-backend = "hatchling.build"

[project]
name            = "mypackage"
version         = "1.2.3"
description     = "A concise one-line description"
readme          = "README.md"
license         = { file = "LICENSE" }
authors         = [{ name = "Your Name", email = "you@example.com" }]
maintainers     = [{ name = "Your Name", email = "you@example.com" }]
keywords        = ["python", "packaging", "example"]
classifiers     = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Typing :: Typed",
]
requires-python = ">=3.10"
dependencies    = [
    "httpx>=0.25.0",
    "pydantic>=2.0.0",
    "click>=8.1.0",
]

[project.optional-dependencies]
dev  = ["pytest>=7.0", "ruff", "mypy", "coverage"]
docs = ["mkdocs", "mkdocs-material"]
all  = ["mypackage[dev,docs]"]

[project.urls]
Homepage      = "https://github.com/example/mypackage"
Documentation = "https://mypackage.readthedocs.io"
Repository    = "https://github.com/example/mypackage.git"
Changelog     = "https://github.com/example/mypackage/blob/main/CHANGELOG.md"

[project.scripts]
mypackage = "mypackage.cli:main"

[project.entry-points."mypackage.plugins"]
default = "mypackage.plugins:DefaultPlugin"

# ── Hatchling build config ────────────────────────────
[tool.hatch.build.targets.wheel]
packages = ["src/mypackage"]

[tool.hatch.build.targets.sdist]
include = ["src/", "tests/", "README.md", "CHANGELOG.md"]

# ── Ruff linter / formatter ───────────────────────────
[tool.ruff]
line-length    = 88
target-version = "py310"
select         = ["E", "F", "W", "I", "N", "UP", "B", "SIM"]
ignore         = ["E501"]

[tool.ruff.isort]
known-first-party = ["mypackage"]

# ── Mypy type checker ─────────────────────────────────
[tool.mypy]
python_version         = "3.11"
strict                 = true
ignore_missing_imports = true

# ── Pytest ────────────────────────────────────────────
[tool.pytest.ini_options]
testpaths    = ["tests"]
addopts      = "-v --tb=short --cov=src/mypackage --cov-report=term-missing"
asyncio_mode = "auto"

# ── Coverage ──────────────────────────────────────────
[tool.coverage.run]
source = ["src/mypackage"]
omit   = ["tests/*", "**/__init__.py"]

[tool.coverage.report]
show_missing = true
fail_under   = 80
'''

# ─────────────────────────────────────────────────────────
# SETUP.PY legacy (still supported)
# ─────────────────────────────────────────────────────────
SETUP_PY = '''
# setup.py  — Legacy but still works
# Used when you need custom build logic outside pyproject.toml

from setuptools import setup, find_packages

setup(
    name="mypackage",
    version="1.2.3",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.10",
    install_requires=[
        "httpx>=0.25",
        "pydantic>=2",
    ],
    extras_require={
        "dev": ["pytest", "ruff"],
    },
    entry_points={
        "console_scripts": [
            "mypackage=mypackage.cli:main",
        ],
    },
)
'''

# ─────────────────────────────────────────────────────────
# MANIFEST.IN (sdist file inclusion rules)
# ─────────────────────────────────────────────────────────
MANIFEST = '''
# MANIFEST.in — controls what goes into source distribution
include README.md
include LICENSE
include CHANGELOG.md
include pyproject.toml

recursive-include src *.py *.pyi
recursive-include tests *.py
recursive-include docs *.md *.rst *.png

global-exclude *.pyc *.pyo __pycache__ .DS_Store *.so
prune .git
prune dist
prune build
prune *.egg-info
'''

# ─────────────────────────────────────────────────────────
# PACKAGE STRUCTURE
# ─────────────────────────────────────────────────────────
PACKAGE_LAYOUT = """
mypackage/
├── pyproject.toml          # Single source of truth for build config
├── README.md               # PyPI landing page
├── CHANGELOG.md
├── LICENSE
├── MANIFEST.in             # Sdist inclusions (legacy)
├── src/
│   └── mypackage/
│       ├── __init__.py     # Public API surface
│       ├── py.typed        # PEP 561 marker (signals typed package)
│       ├── cli.py          # Entry point for scripts
│       ├── core.py
│       ├── models.py
│       └── _internal/      # Private subpackage
│           └── __init__.py
└── tests/
    ├── conftest.py
    ├── test_core.py
    └── test_cli.py
"""

# ─────────────────────────────────────────────────────────
# __init__.py with controlled public API
# ─────────────────────────────────────────────────────────
INIT_PY = '''
# src/mypackage/__init__.py
"""
MyPackage: A professional Python package example.
"""
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("mypackage")
except PackageNotFoundError:
    __version__ = "unknown"

__all__ = ["MyClass", "helper_function", "__version__"]

from .core import MyClass            # noqa: F401 (re-exported)
from .utils import helper_function   # noqa: F401
'''

# ─────────────────────────────────────────────────────────
# CLI entrypoint
# ─────────────────────────────────────────────────────────
CLI_PY = '''
# src/mypackage/cli.py
"""Command-line interface for mypackage."""
import argparse
import sys
from . import __version__

def main(argv=None):
    parser = argparse.ArgumentParser(prog="mypackage", description="MyPackage CLI")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command")

    # Sub-command: run
    run_parser = subparsers.add_parser("run", help="Run something")
    run_parser.add_argument("input", help="Input value")
    run_parser.add_argument("--verbose", "-v", action="store_true")

    args = parser.parse_args(argv)

    if args.command == "run":
        if args.verbose:
            print(f"Processing: {args.input}")
        print(f"Done: {args.input}")
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
'''

if __name__ == "__main__":
    print("=== pyproject.toml (modern) ===")
    print(PYPROJECT_MODERN[:400] + "\n...\n")

    print("=== Package Layout ===")
    print(PACKAGE_LAYOUT)

    print("=== Build & Distribute Commands ===")
    commands = [
        ("Install build tool",  "pip install build twine"),
        ("Build distribution",  "python -m build"),
        ("Check distribution",  "twine check dist/*"),
        ("Upload to TestPyPI",  "twine upload --repository testpypi dist/*"),
        ("Upload to PyPI",      "twine upload dist/*"),
        ("Install editable",    "pip install -e .[dev]"),
        ("Run tests",           "pytest"),
        ("Lint",                "ruff check src/"),
        ("Type-check",          "mypy src/"),
    ]
    for desc, cmd in commands:
        print(f"  {desc:25s}: {cmd}")
