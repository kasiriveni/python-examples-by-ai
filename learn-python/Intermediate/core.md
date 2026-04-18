# Core Python Concepts

## Core Themes
- Object-oriented programming and class design.
- Comprehensions, error handling, and module organization.
- Working with APIs and reusable code structure.

## Core Theme Examples
- Example 1: Class definition with __init__ and instance methods.
- Example 2: List comprehension with exception-handling wrapper.
- Example 3: Function that calls external API and processes response.

## Files and Concepts
- classes_intermediate.py: composition, mixins, dataclasses, object initialization
- comprehensions_and_data.py: list, dict, and set comprehensions, filtering
- error_handling.py: try, except, finally, error-handling patterns
- modules_and_packages.py: imports, module usage, package structure
- oop.py: classes, inheritance, method overriding, polymorphism
- working_with_apis.py: HTTP requests, API calls, JSON response handling

## Core Example
This example shows a small class, a comprehension, and safe error handling.

```python
class Counter:
	def __init__(self, values):
		self.values = values

	def squares(self):
		return [value * value for value in self.values]

try:
	print(Counter([1, 2, 3]).squares())
except Exception as error:
	print(f"Failed: {error}")
```
