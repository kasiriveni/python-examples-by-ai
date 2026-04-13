"""
Packaging and Distribution: Building and publishing Python packages.
"""
import os

# === Package structure example ===
PACKAGE_LAYOUT = """
mypackage/
├── pyproject.toml          # Build configuration
├── README.md               # Project description
├── LICENSE                  # License file
├── CHANGELOG.md            # Version history
├── src/
│   └── mypackage/
│       ├── __init__.py     # Package marker + version
│       ├── core.py         # Main functionality
│       ├── utils.py        # Helper functions
│       └── cli.py          # CLI entry point
├── tests/
│   ├── conftest.py         # Shared fixtures
│   ├── test_core.py
│   └── test_utils.py
└── docs/
    ├── index.md
    └── api.md
"""

# === pyproject.toml (modern standard) ===
PYPROJECT_TOML = '''
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "mypackage"
version = "1.0.0"
description = "A sample Python package"
readme = "README.md"
license = "MIT"
requires-python = ">=3.10"
authors = [
    { name = "Your Name", email = "you@example.com" },
]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]
keywords = ["example", "package"]
dependencies = [
    "requests>=2.28",
    "click>=8.0",
]

[project.optional-dependencies]
dev = ["pytest>=8.0", "ruff", "mypy"]
docs = ["mkdocs", "mkdocstrings"]

[project.scripts]
mypackage = "mypackage.cli:main"

[project.urls]
Homepage = "https://github.com/user/mypackage"
Documentation = "https://mypackage.readthedocs.io"
Repository = "https://github.com/user/mypackage"
'''

# === __init__.py example ===
INIT_PY = '''
"""MyPackage - A sample Python package."""

__version__ = "1.0.0"

from .core import MyClass, process_data
from .utils import helper_function

__all__ = ["MyClass", "process_data", "helper_function"]
'''

# === Build and publish commands ===
BUILD_COMMANDS = """
=== Building and Publishing ===

# Install build tools
pip install build twine

# Build the package
python -m build
# Creates: dist/mypackage-1.0.0.tar.gz
#          dist/mypackage-1.0.0-py3-none-any.whl

# Check the package
twine check dist/*

# Upload to TestPyPI (testing)
twine upload --repository testpypi dist/*

# Upload to PyPI (production)
twine upload dist/*

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ mypackage

# Using trusted publishing (GitHub Actions)
# See: https://docs.pypi.org/trusted-publishers/
"""

# === Versioning strategies ===
class SemanticVersion:
    """Semantic versioning helper (MAJOR.MINOR.PATCH)."""

    def __init__(self, version_string):
        parts = version_string.split('.')
        self.major = int(parts[0])
        self.minor = int(parts[1])
        self.patch = int(parts[2]) if len(parts) > 2 else 0

    def bump_major(self):
        return SemanticVersion(f"{self.major + 1}.0.0")

    def bump_minor(self):
        return SemanticVersion(f"{self.major}.{self.minor + 1}.0")

    def bump_patch(self):
        return SemanticVersion(f"{self.major}.{self.minor}.{self.patch + 1}")

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"

    def __repr__(self):
        return f"SemanticVersion('{self}')"

if __name__ == "__main__":
    print("=== Package Layout ===")
    print(PACKAGE_LAYOUT)

    print("=== pyproject.toml ===")
    print(PYPROJECT_TOML)

    print(BUILD_COMMANDS)

    # Version bumping
    print("=== Version Bumping ===")
    v = SemanticVersion("1.2.3")
    print(f"Current: {v}")
    print(f"Patch:   {v.bump_patch()}")
    print(f"Minor:   {v.bump_minor()}")
    print(f"Major:   {v.bump_major()}")
