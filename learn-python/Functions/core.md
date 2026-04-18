# Core Python Concepts

## Core Themes
- Function definitions and calling conventions.
- Closures, scope, recursion, and higher-order functions.
- Lambda expressions and decorator-related patterns.

## Core Theme Examples
- Example 1: Function with default parameters and args convention.
- Example 2: Nested function accessing outer scope with closure.
- Example 3: Lambda expression passed to sorted() or map().

## Files and Concepts
- advanced_functions.py: closures, parameterized decorators, recursion, type annotations
- calling_conventions.py: positional-only args, keyword-only args, variadic args, closures, decorated functions
- closures_and_scope.py: LEGB scope, closures, nonlocal, memoization
- function_basics.py: basic functions, default parameters, args, kwargs, docstrings
- higher_order_functions.py: first-class functions, passing and returning functions, map, filter, reduce
- lambda_functions.py: lambda syntax, sorting with lambda, map and filter with lambda
- recursion.py: factorial, Fibonacci, Tower of Hanoi, binary search recursion

## Core Example
This example demonstrates closures and a small lambda helper.

```python
def multiplier(factor):
	def apply(value):
		return value * factor
	return apply

times_three = multiplier(3)
square = lambda value: value * value

print(times_three(4), square(5))
```
