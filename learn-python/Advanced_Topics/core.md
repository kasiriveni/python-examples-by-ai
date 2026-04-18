# Core Python Concepts

## Core Themes
- Decorators, iterators, generators, and comprehensions.
- Context managers, descriptors, metaclasses, and memory tuning.
- Functional helpers, regular expressions, and advanced OOP patterns.

## Core Theme Examples
- Example 1: @wraps decorator applied to logging wrapper function.
- Example 2: Context manager class with __enter__ and __exit__ protocol.
- Example 3: lru_cache decorator for memoized function results.

## Files and Concepts
- abstract_base_classes.py: ABC enforcement, abstractmethod, virtual subclass registration
- Args_and_Kwargs.py: args, kwargs, unpacking, flexible call signatures
- Comprehensions.py: list, dict, and set comprehensions
- Context_Managers.py: enter and exit protocol, with statement, resource cleanup
- Decorators.py: function and class decorators, wrappers, wraps, stacking
- decorator_logging_example.py: logging decorators, call tracing, wrapper behavior
- descriptors.py: validated descriptors, lazy properties, attribute interception
- Generators.py: yield, lazy evaluation, generator functions
- Iterators.py: iter and next protocol, StopIteration, iterator state
- Lambdas.py: lambda expressions, inline callbacks, sorting and mapping
- Map_Filter_Reduce.py: map, filter, reduce, transformation pipelines
- memoization_example.py: lru_cache, result caching, cache-aware design
- metaclass_example.py: custom metaclasses, attribute enforcement, metaclass new
- OOP.py: classes, inheritance, dunder overrides, polymorphism
- Regular_Expressions.py: re search, pattern matching, compiled regex usage
- slots_and_memory.py: slots memory savings, tracemalloc profiling, restricted attributes

## Core Example
This example uses a decorator and a comprehension in one small workflow.

```python
from functools import wraps

def announce(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		print(f"running {func.__name__}")
		return func(*args, **kwargs)
	return wrapper

@announce
def squares(limit):
	return [number * number for number in range(limit)]

print(squares(4))
```
