# Core Python Concepts

## Core Themes
- Import mechanics and package structure.
- Dynamic importing, reload behavior, and export control.
- Main-entry patterns and module metadata.

## Core Theme Examples
- Example 1: Using sys.path to discover and import custom modules.
- Example 2: Using importlib.import_module for lazy loading.
- Example 3: Using if __name__ == "__main__" guard for entry point.

## Files and Concepts
- import_system_deep_dive.py: sys.path, sys.modules, importlib, lazy loading, relative imports, all exports
- modules_comprehensive.py: import styles, module attributes, path management, reloads, package layout
- modules_examples.py: name-main guard, main-function entry pattern
- package_readme_example.py: package layout reference and structural guidance

## Core Example
This example imports a module dynamically with importlib.

```python
from importlib import import_module

math_module = import_module("math")
values = [1, 4, 9]
roots = [math_module.sqrt(value) for value in values]

print(roots)
```
