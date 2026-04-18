# Core Python Concepts

## Core Themes
- Design patterns, Python idioms, and common gotchas.
- Algorithmic interview practice across strings, arrays, and graphs.
- Pattern-oriented and trick-oriented Python examples.

## Core Theme Examples
- Example 1: Singleton and factory method design patterns.
- Example 2: Sliding window and two-pointer array algorithms.
- Example 3: Dictionary merge operators and extended unpacking.

## Files and Concepts
- design_patterns.py: singleton, factory method, builder, prototype, adapter, decorator
- interview_problems.py: palindromes, sliding window, two pointers, prefix products, matrix rotation, BFS
- python_gotchas.py: mutable default arguments, late binding, identity versus equality, class-versus-instance attributes
- python_patterns.py: comprehensions, generator expressions, walrus operator, flattening, transposition, deduplication
- python_tricks.py: built-in helpers, dictionary merge, extended unpacking, string justification

## Core Example
This example uses a comprehension and a slice-based palindrome check.

```python
numbers = [1, 2, 3, 4]
squares = {number: number * number for number in numbers}

word = "level"
is_palindrome = word == word[::-1]

print(squares)
print(is_palindrome)
```
