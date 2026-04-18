# Core Python Concepts

## Core Themes
- Pythonic class design and inheritance patterns.
- Decorators, context managers, iterators, and magic methods.
- Type hints, dataclasses, and standard-library helpers for clean code.

## Core Theme Examples
- Example 1: Dataclass field definitions with automatic initialization.
- Example 2: Property decorators and computed attributes.
- Example 3: Custom context managers with __enter__ and __exit__.

## Files and Concepts
- abc_example.py: abstract base classes, abstract methods, interface design
- classes_inheritance_mro.py: inheritance, multiple inheritance, method-resolution order
- context_managers.py: enter and exit methods, with statement
- context_managers_examples.py: custom context managers, resource cleanup
- dataclasses_namedtuple.py: dataclass, NamedTuple, structured records
- decorators.py: wrapper functions, decorator syntax
- decorators_examples.py: property, staticmethod, classmethod decorators
- dunder_methods.py: repr, str, call, and other magic methods
- functools_examples.py: partial, lru_cache, reduce
- iterators_and_generators.py: iter and next methods, yield, iterator design
- iterators_generators.py: custom iterators, generator functions
- itertools_collections_examples.py: Counter, deque, permutations, combinations
- pythonic_oop.py: enumerate, EAFP style, Protocol usage
- type_hints.py: basic annotations, List, Optional
- type_hints_examples.py: Union, Literal, TypeVar, Optional

## Core Example
This example uses a dataclass and a cached function for clean Pythonic code.

```python
from dataclasses import dataclass
from functools import lru_cache

@dataclass
class User:
	name: str

@lru_cache(maxsize=None)
def fib(n):
	return n if n < 2 else fib(n - 1) + fib(n - 2)

print(User("Alice"), fib(10))
```
