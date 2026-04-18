# Core Python Concepts

## Core Themes
- Dependency management tools and package-install workflows.
- Comparing pip, uv, Conda, and Poetry-style capabilities.
- Package introspection, version constraints, and project reproducibility.

## Core Theme Examples
- Example 1: Using pip install -r requirements.txt for workflow.
- Example 2: Comparing uv sync vs poetry lock vs conda update.
- Example 3: Checking installed package versions with pip list --outdated.

## Files and Concepts
- Conda.py: Conda env creation, activation, installation, listing, removal
- package_managers_comparison.py: pip, uv, poetry comparison, installed-package introspection
- Pip.py: pip install, uninstall, version specs, package listing
- pip_and_uv.py: requirements formats, virtualenv flows, pip and uv command patterns
- Uv.py: uv installation, add and remove dependencies, listing

## Core Example
This example invokes pip through the active Python interpreter.

```python
import subprocess
import sys

command = [sys.executable, "-m", "pip", "--version"]
result = subprocess.run(command, capture_output=True, text=True, check=False)

print(result.stdout.strip())
```
