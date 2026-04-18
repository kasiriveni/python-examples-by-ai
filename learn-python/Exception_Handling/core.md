# Core Python Concepts

## Core Themes
- Exception-handling fundamentals and control flow.
- Custom exception hierarchies and chained exceptions.
- Batch errors and domain-specific error patterns.

## Core Theme Examples
- Example 1: Try-except catching ValueError from conversion.
- Example 2: Custom exception class with inheritance.
- Example 3: Multiple except handlers for different error types.

## Files and Concepts
- class.py: class structure, public and private methods, visibility patterns
- custom_exceptions.py: custom exceptions, exception hierarchies, validation and retry errors
- custom_exceptions_advanced.py: hierarchical exceptions, exception chaining, context preservation
- exception_basics.py: try and except, multiple handlers, else and finally, reraising
- exception_groups.py: ExceptionGroup, except star syntax, aggregated errors
- exception_patterns.py: HTTP-style exceptions, database errors, auth errors, rate-limit mapping

## Core Example
This example catches a built-in error and raises a custom exception when needed.

```python
class InvalidAgeError(Exception):
	pass

def parse_age(text):
	age = int(text)
	if age < 0:
		raise InvalidAgeError("age cannot be negative")
	return age

try:
	print(parse_age("12"))
except (ValueError, InvalidAgeError) as error:
	print(error)
```
