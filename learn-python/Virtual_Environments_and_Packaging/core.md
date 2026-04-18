# Core Python Concepts

## Core Themes
- Environment creation, activation, and dependency pinning.
- How pip resolves packages and manages installs.
- Import-system mechanics and packaging metadata.

## Core Theme Examples
- Example 1: Creating venv and pinning dependencies with requirements.txt.
- Example 2: Understanding pip dependency resolver with lockfiles.
- Example 3: Using sys.path and sys.modules for custom import hooks.

## Files and Concepts
- dependency_management.py: requirements, pyproject dependency specs, lockfile concepts, resolver logic
- import_system.py: sys.path, sys.modules, importlib, custom import hooks, lazy loading
- main.py: YAML configuration loading and startup-oriented config access
- pip_internals.py: programmatic pip invocation, freeze, check, outdated, lock-generation concepts
- venv_and_packaging.py: venv metadata, activation, requirements management, pyproject structure

## Core Example
This example inspects the current interpreter and a requirements file path.

```python
from pathlib import Path
import sys

requirements = Path("requirements.txt")
inside_venv = sys.prefix != sys.base_prefix

print(sys.executable)
print(requirements.name)
print(inside_venv)
```
