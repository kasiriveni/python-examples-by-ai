"""
Performance profiling and optimization in Python.
"""
import time
import timeit
import cProfile
import io
import pstats
from functools import lru_cache

# === timeit for micro-benchmarks ===
print("=== timeit ===")

# Compare list creation methods
list_comp_time = timeit.timeit('[x**2 for x in range(100)]', number=10000)
map_time = timeit.timeit('list(map(lambda x: x**2, range(100)))', number=10000)
loop_time = timeit.timeit('''
result = []
for x in range(100):
    result.append(x**2)
''', number=10000)

print(f"List comprehension: {list_comp_time:.4f}s")
print(f"map+lambda: {map_time:.4f}s")
print(f"For loop: {loop_time:.4f}s")

# === Context manager timer ===
print("\n=== Custom Timer ===")

class Timer:
    def __init__(self, label=""):
        self.label = label

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, *args):
        self.elapsed = time.perf_counter() - self.start
        print(f"  {self.label}: {self.elapsed:.6f}s")

with Timer("Sum 1M"):
    total = sum(range(1_000_000))

with Timer("List comp 1M"):
    squares = [x**2 for x in range(1_000_000)]

# === cProfile ===
print("\n=== cProfile ===")

def fibonacci_slow(n):
    if n <= 1:
        return n
    return fibonacci_slow(n-1) + fibonacci_slow(n-2)

@lru_cache(maxsize=None)
def fibonacci_fast(n):
    if n <= 1:
        return n
    return fibonacci_fast(n-1) + fibonacci_fast(n-2)

# Profile slow version
profiler = cProfile.Profile()
profiler.enable()
fibonacci_slow(20)
profiler.disable()

stream = io.StringIO()
stats = pstats.Stats(profiler, stream=stream)
stats.sort_stats('cumulative')
stats.print_stats(5)
print(stream.getvalue())

# Compare performance
with Timer("fib_slow(30)"):
    fibonacci_slow(30)

with Timer("fib_fast(30)"):
    fibonacci_fast(30)

# === Memory optimization ===
print("\n=== Memory Tips ===")
import sys

# Slots vs regular class
class RegularPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class SlottedPoint:
    __slots__ = ('x', 'y')
    def __init__(self, x, y):
        self.x = x
        self.y = y

rp = RegularPoint(1, 2)
sp = SlottedPoint(1, 2)
print(f"Regular point size: {sys.getsizeof(rp)} + {sys.getsizeof(rp.__dict__)} bytes")
print(f"Slotted point size: {sys.getsizeof(sp)} bytes")

# Generator vs list
list_mem = sys.getsizeof([x**2 for x in range(10000)])
gen_mem = sys.getsizeof(x**2 for x in range(10000))
print(f"\nList (10K items): {list_mem} bytes")
print(f"Generator (10K items): {gen_mem} bytes")
