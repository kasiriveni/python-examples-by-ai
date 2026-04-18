# Core Python Concepts

## Core Themes
- Abstract interfaces, protocols, and structural typing.
- Descriptors, metaclasses, and advanced attribute mechanics.
- Generics, async patterns, and memory-aware programming.

## Core Theme Examples
- Example 1: Abstract base class with @abstractmethod decorator enforcement.
- Example 2: Descriptor protocol with validated property setter.
- Example 3: Async function with await and TypeVar generic constraint.

## Files and Concepts
- abstract_base_classes.py: ABC definitions, abstract methods and properties, collections.abc
- async_patterns.py: async and await, gather, task creation, cancellation patterns
- comprehensions.py: list, dict, and set comprehensions, generator expressions
- descriptors.py: descriptor protocol, data versus non-data descriptors, controlled attributes
- metaclasses.py: type-based class creation, custom metaclasses, singleton metaclass
- protocols.py: Protocol types, structural subtyping, runtime-checkable protocols
- type_system.py: TypeVar, Generic classes, constrained generics, overloads
- weakrefs_and_memory.py: slots optimization, weak references, garbage collection, memory profiling

## Core Example
This example uses an abstract base class to define a clear interface.

```python
from abc import ABC, abstractmethod

class Shape(ABC):
	@abstractmethod
	def area(self):
		raise NotImplementedError

class Square(Shape):
	def __init__(self, side):
		self.side = side

	def area(self):
		return self.side * self.side

print(Square(4).area())
```
