# Core Python Concepts

## Core Themes
- Pure functions and immutable-style transformations.
- Higher-order functions, composition, and currying.
- Map, filter, reduce, and partial application patterns.

## Core Theme Examples
- Example 1: Pure function transforming immutable list without state changes.
- Example 2: Function composition or map combined with lambda predicates.
- Example 3: filter(), reduce(), and partial() chained on sequence of values.

## Files and Concepts
- advanced_functional.py: higher-order functions, closures, function composition, currying, pipe patterns
- functional_examples.py: map, filter, reduce, partial application, pure-function examples
- functional_patterns.py: pure functions, composition, higher-order operations, partial functions
- functional_programming_comprehensive.py: accumulate, reduce, partial, curry decorators, comprehensive functional patterns

## Core Example
This example filters, maps, and reduces values with small pure functions.

```python
from functools import reduce

numbers = [1, 2, 3, 4, 5]
evens = filter(lambda value: value % 2 == 0, numbers)
doubled = map(lambda value: value * 2, evens)
total = reduce(lambda left, right: left + right, doubled, 0)

print(total)
```
