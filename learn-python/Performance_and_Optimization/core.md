# Core Python Concepts

## Core Themes
- Profiling, benchmarking, and measurement-first optimization.
- Memory usage, hot paths, and practical performance patterns.
- Balancing speed improvements with maintainability.

## Core Theme Examples
- Example 1: Using cProfile to measure function execution time.
- Example 2: Applying lru_cache to avoid redundant calculations.
- Example 3: Using list comprehensions vs loops for speed-and-clarity tradeoff.

## Files and Concepts
- memory_and_profiling.py: memory profiling, allocation awareness, profiling workflows
- performance_examples.py: small performance-focused coding examples and comparisons
- performance_patterns.py: common optimization patterns, caching, efficient looping strategies
- profiling_and_benchmarking.py: profilers, timing, repeatable benchmarks, bottleneck discovery
- profiling_example.py: simple profiling example, runtime measurement

## Core Example
This example times a function and caches repeated work.

```python
import time
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
	return n if n < 2 else fib(n - 1) + fib(n - 2)

start = time.perf_counter()
print(fib(20))
print(round(time.perf_counter() - start, 6))
```
