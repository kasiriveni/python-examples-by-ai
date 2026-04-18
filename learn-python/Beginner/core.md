# Core Python Concepts

## Core Themes
- Variables, data types, and collection basics.
- Conditionals, loops, and function fundamentals.
- Simple file handling and introductory recursion.

## Core Theme Examples
- Example 1: List and dictionary creation with type assignment.
- Example 2: For loop inside function with conditional check.
- Example 3: Reading text file into list with context manager.

## Files and Concepts
- collections_basics.py: lists, tuples, unpacking, collection operations
- control_flow.py: if and else, break, continue, ternary expressions, match case
- file_handling.py: file reading, file writing, context managers
- functions.py: functions, lambda expressions, default parameters, scope, nested functions, recursion
- variables_and_basics.py: variable assignment, string methods, formatting, basic types
- variables_and_data_types.py: string, integer, float, boolean declarations

## Core Example
This example uses a list, a loop, and a small helper function.

```python
items = ["apple", "banana", "avocado"]

def starts_with_a(word):
	return word.startswith("a")

for item in items:
	if starts_with_a(item):
		print(item)
```
