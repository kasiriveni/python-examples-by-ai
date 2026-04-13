"""
Virtual Environments and Packaging: Setup and management.
"""
import os
import sys
import site

# === Virtual Environment Information ===
print("=== Current Environment ===")
print(f"Python: {sys.version}")
print(f"Executable: {sys.executable}")
print(f"Prefix: {sys.prefix}")
print(f"Base prefix: {sys.base_prefix}")
print(f"In venv: {sys.prefix != sys.base_prefix}")
print(f"Path: {sys.path[:3]}")

# === Virtual Environment Creation (code reference) ===
VENV_COMMANDS = """
=== Virtual Environment Commands ===

# Create virtual environment
python -m venv myproject_env

# Activate (Windows)
myproject_env\\Scripts\\activate

# Activate (Unix/Mac)
source myproject_env/bin/activate

# Deactivate
deactivate

# Create with specific Python
python3.12 -m venv myproject_env

# Create with system packages access
python -m venv --system-site-packages myproject_env
"""

# === Requirements management ===
REQUIREMENTS_EXAMPLE = """
# requirements.txt
fastapi>=0.110.0,<1.0.0
uvicorn[standard]>=0.29.0
sqlalchemy>=2.0.0
pydantic>=2.0.0
python-dotenv>=1.0.0
"""

REQUIREMENTS_DEV = """
# requirements-dev.txt
-r requirements.txt
pytest>=8.0.0
pytest-cov>=5.0.0
ruff>=0.4.0
mypy>=1.9.0
pre-commit>=3.7.0
"""

# === pyproject.toml modern packaging ===
PYPROJECT_EXAMPLE = """
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "my-package"
version = "0.1.0"
description = "My Python package"
readme = "README.md"
requires-python = ">=3.10"
license = "MIT"
authors = [
    { name = "Developer", email = "dev@example.com" },
]
dependencies = [
    "requests>=2.31",
    "click>=8.0",
]

[project.optional-dependencies]
dev = ["pytest", "ruff"]

[project.scripts]
my-cli = "my_package.cli:main"
"""

# === Package structure ===
PACKAGE_STRUCTURE = """
my-package/
├── pyproject.toml
├── README.md
├── LICENSE
├── src/
│   └── my_package/
│       ├── __init__.py
│       ├── core.py
│       ├── cli.py
│       └── utils.py
├── tests/
│   ├── __init__.py
│   ├── test_core.py
│   └── test_utils.py
└── docs/
    └── index.md
"""

# === Pip commands reference ===
PIP_COMMANDS = """
=== Pip Commands ===

pip install package              # Install package
pip install package==1.2.3       # Specific version
pip install package>=1.0,<2.0    # Version range
pip install -r requirements.txt  # From file
pip install -e .                 # Editable install (development)
pip install -e ".[dev]"          # Editable with extras

pip freeze > requirements.txt    # Export installed packages
pip list                         # List installed packages
pip show package                 # Package info
pip uninstall package            # Remove package
pip install --upgrade package    # Upgrade package

# Modern alternatives:
pip install uv                   # Fast installer
uv pip install -r requirements.txt
"""

if __name__ == "__main__":
    print(VENV_COMMANDS)
    print(REQUIREMENTS_EXAMPLE)
    print(PYPROJECT_EXAMPLE)
    print("=== Package Structure ===")
    print(PACKAGE_STRUCTURE)
    print(PIP_COMMANDS)
