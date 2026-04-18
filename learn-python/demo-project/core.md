# Core Python Concepts

## Core Themes
- Small project scaffold and execution entry point.
- Placeholder space for runnable demonstrations.
- Useful for practicing packaging and dependency setup.

## Core Theme Examples
- Example 1: Create a minimal Python module structure.
- Example 2: Add runnable script entry points.
- Example 3: Set up package dependencies and environment configuration.

## Files and Concepts
- demo.py: empty starter script for demo-project structure

## Core Example
This example creates a tiny project folder with an entry-point file.

```python
from pathlib import Path

root = Path("demo_app")
root.mkdir(exist_ok=True)
(root / "main.py").write_text('print("hello")\n', encoding="utf-8")

print(sorted(path.name for path in root.iterdir()))
```
