# Core Python Concepts

## Core Themes
- Package organization and reusable-code boundaries.
- Public-versus-private module layout thinking.
- This folder currently serves as a package placeholder.

## Core Theme Examples
- Example 1: Defining __init__.py to expose public API.
- Example 2: Separating public methods from _private helper methods.
- Example 3: Organizing modules as reusable package boundaries.

## Files and Concepts
- No Python files in this folder.

## Core Example
This example shows a small public class with a private helper method.

```python
class PublicAPI:
	def process(self, items):
		return [self._double(item) for item in items]

	def _double(self, item):
		return item * 2

print(PublicAPI().process([1, 2, 3]))
```
