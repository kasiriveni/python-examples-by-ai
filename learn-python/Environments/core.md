# Core Python Concepts

## Core Themes
- Python environment isolation and version management.
- Tooling around venv, Pipenv, Poetry, and pyenv.
- Environment variables and configuration loading.

## Core Theme Examples
- Example 1: Creating venv and checking sys.prefix != sys.base_prefix.
- Example 2: Using poetry install to resolve and manage project dependencies.
- Example 3: Loading APP_ENV from .env file with fallback defaults.

## Files and Concepts
- environment_management.py: environment variables, dotenv parsing, config classes, platform and path info
- Pipenv.py: Pipenv install flows, activation, project initialization
- Poetry.py: Poetry init, dependency management, env activation, script execution
- Pyenv.py: Python version installation, global and local version switching
- Venv.py: virtual-environment creation, activation, deactivation across platforms

## Core Example
This example reads environment variables with sensible defaults.

```python
import os
import sys

app_env = os.getenv("APP_ENV", "development")
debug = os.getenv("DEBUG", "false").lower() == "true"
inside_venv = sys.prefix != sys.base_prefix

print(app_env, debug, inside_venv)
```
