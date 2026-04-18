# Core Python Concepts

## Core Themes
- Python fundamentals and standard library usage.
- Basic control flow, loops, and simple object-oriented patterns.
- Serialization, networking, and external service examples.

## Core Theme Examples
- Example 1: Using json module to serialize Python objects.
- Example 2: Class with for loop and list processing.
- Example 3: HTTP request to fetch and parse JSON data.

## Files and Concepts
- 1.py: basic syntax, print statements, arithmetic, MD5 hashing
- 2.py: JSON serialization, primitive data types, Counter usage
- 3.py: HTTP requests, response handling, conditional logic
- 4.py: sys module usage, type casting, exception handling
- 5.py: class basics, encapsulation, instance methods
- 6.py: abstract base classes, inheritance, built-in collections, serialization
- 7.py: for loops, while loops, loop flow
- 8.py: Redis connection, authentication, connection pooling

## Core Example
This example combines lists, loops, classes, and JSON serialization in plain Python.

```python
import json

numbers = [1, 2, 3]

class User:
	def __init__(self, name):
		self.name = name

payload = {"user": User("Alice").name, "total": sum(numbers)}
print(json.dumps(payload))
```
