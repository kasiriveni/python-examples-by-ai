# Core Python Concepts

## Core Themes
- Arithmetic, comparison, logical, and membership operators.
- Bitwise operations and precedence-aware expressions.
- Operator overloading through special methods.

## Core Theme Examples
- Example 1: Arithmetic operators (+, -, *) with comparison operators (<, ==).
- Example 2: Bitwise AND (&) and XOR (^) with short-circuit evaluation.
- Example 3: __add__ and __eq__ dunder methods in Vector class.

## Files and Concepts
- bitwise_and_advanced_ops.py: bitwise AND, OR, XOR, shifts, operator module helpers
- operator_overloading.py: dunder methods for arithmetic, comparison, indexing, iteration
- operators_comprehensive.py: arithmetic, comparison, logical, bitwise, and membership operators
- operators_examples.py: walrus operator, assignment operators, short-circuit logic, bitwise examples

## Core Example
This example shows arithmetic, comparison, and a small overloaded operator.

```python
class Vector:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __add__(self, other):
		return Vector(self.x + other.x, self.y + other.y)

	def __repr__(self):
		return f"Vector({self.x}, {self.y})"

print(Vector(1, 2) + Vector(3, 4))
```
