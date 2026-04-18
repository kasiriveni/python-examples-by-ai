# Core Python Concepts

## Core Themes
- Core syntax, variables, strings, and built-in data structures.
- Functions, control flow, comprehensions, and file handling.
- Imports, formatting, and exception basics for foundation-level Python.

## Core Theme Examples
- Example 1: List and dict comprehensions with conditional filters.
- Example 2: F-string formatting and dynamic variable interpolation.
- Example 3: Try-except-finally blocks for robust error handling.

## Files and Concepts
- advanced_string_formatting.py: alignment, padding, width, and format specifications
- comprehensions.py: list, dict, and set comprehensions, conditional filtering
- control_flow.py: if and elif, for loops, while loops
- core_language.py: Decimal, Fraction, defaultdict, deque, ChainMap, Template strings
- data_structures.py: lists, tuples, dicts, sets, mutability
- exception_handling.py: try, except, finally, custom exceptions
- file_io.py: file reading, writing, context managers
- file_io_append.py: append mode, line-by-line reading
- functions_examples.py: args, kwargs, default parameters
- modules_import.py: import statements, from import usage
- nested_loops.py: nested loops, break, continue
- python_syntax.py: indentation rules, REPL-style syntax basics
- string_formatting.py: f-strings, format, percent formatting
- type_conversion.py: int, float, str casting, dynamic typing
- variables_and_data_types.py: int, float, str, bool, None values

## Core Example
This example combines variables, a function, and a comprehension.

```python
name = "Python"

def greet(target):
	return f"Hello, {target}!"

squares = [number * number for number in range(4)]
print(greet(name))
print(squares)
```
