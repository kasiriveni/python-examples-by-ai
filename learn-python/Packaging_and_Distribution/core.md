# Core Python Concepts

## Core Themes
- Building and publishing Python packages.
- Modern pyproject-based metadata and build systems.
- Versioning, plugins, and package-level testing patterns.

## Core Theme Examples
- Example 1: Using build and twine to publish package to PyPI.
- Example 2: Declaring dependencies in pyproject.toml with PEP 621 format.
- Example 3: Parsing semantic version strings and implementing version bumps.

## Files and Concepts
- building_packages.py: src layout, pyproject metadata, build commands, twine publishing
- namespace_and_plugins.py: namespace packages, plugin protocols, registries, plugin discovery
- pyproject_toml_guide.py: PEP 517, PEP 518, PEP 621, dependency groups, tool configs
- semantic_versioning.py: semantic version parsing, version bumps, prereleases, changelog categories
- testing_packages.py: package tests, lightweight runners, exception and parameterized testing

## Core Example
This example parses a semantic version string with the standard library.

```python
import re

pattern = r"^(\d+)\.(\d+)\.(\d+)$"
match = re.match(pattern, "1.4.2")

if match:
	major, minor, patch = match.groups()
	print({"major": int(major), "minor": int(minor), "patch": int(patch)})
```
