# Core Python Concepts

## Core Themes
- Readable code structure and maintainable design.
- SOLID principles, testing, logging, and documentation habits.
- Error handling and project organization patterns.

## Core Theme Examples
- Example 1: Using dataclass instead of dict for clean config management.
- Example 2: Applying single-responsibility principle with strategy pattern.
- Example 3: Custom exception hierarchy with context managers for cleanup.

## Files and Concepts
- clean_code.py: naming, single-responsibility functions, guard clauses, dataclasses, comprehension idioms
- code_organization.py: project structure, config dataclasses, dependency injection, repository and service layers
- docstring_example.py: docstring formatting, function documentation, type hints
- error_handling_patterns.py: specific exceptions, custom hierarchies, retry patterns, cleanup
- logging_example.py: logging setup, log levels, exception logging
- solid_principles.py: single responsibility, open-closed, Liskov substitution, polymorphic strategy design
- unit_test_example.py: unittest test cases, assertions, test organization

## Core Example
This example uses a dataclass and dependency injection for clean structure.

```python
from dataclasses import dataclass

@dataclass
class Config:
	retries: int = 3

class Service:
	def __init__(self, config):
		self.config = config

	def describe(self):
		return f"retries={self.config.retries}"

print(Service(Config()).describe())
```
