"""
Iterators and Generators: Infinite sequences and lazy pipelines.
"""
import itertools
import functools
from typing import Iterator, Generator, TypeVar

T = TypeVar("T")

# ═══════════════════════════════════════════
# 1. Infinite iterators
# ═══════════════════════════════════════════
def naturals(start: int = 1) -> Iterator[int]:
    """Infinite stream of integers."""
    n = start
    while True:
        yield n
        n += 1

def fibonacci() -> Iterator[int]:
    """Infinite Fibonacci sequence."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

def primes() -> Iterator[int]:
    """Infinite stream of prime numbers (simple sieve)."""
    yield 2
    composites: dict[int, list[int]] = {}
    cand = 3
    while True:
        if cand not in composites:
            yield cand
            composites[cand * cand] = [cand]
        else:
            for p in composites[cand]:
                composites.setdefault(cand + p, []).append(p)
            del composites[cand]
        cand += 2

def powers_of(base: int) -> Iterator[int]:
    """0, base, base², base³ …"""
    n = 0
    while True:
        yield base ** n
        n += 1

def cycle_with_index(iterable) -> Iterator[tuple[int, any]]:
    """Cycle through iterable, yielding (cycle_number, item)."""
    cycle = 0
    while True:
        for item in iterable:
            yield cycle, item
        cycle += 1

# Helper: take first n items
def take(n: int, gen: Iterator[T]) -> list[T]:
    return list(itertools.islice(gen, n))

# ═══════════════════════════════════════════
# 2. Generator-based pipelines
# ═══════════════════════════════════════════
def gen_map(func, gen: Iterator[T]) -> Iterator:
    for item in gen:
        yield func(item)

def gen_filter(pred, gen: Iterator[T]) -> Iterator[T]:
    for item in gen:
        if pred(item):
            yield item

def gen_limit(n: int, gen: Iterator[T]) -> Iterator[T]:
    for i, item in enumerate(gen):
        if i >= n:
            return
        yield item

def gen_skip(n: int, gen: Iterator[T]) -> Iterator[T]:
    for i, item in enumerate(gen):
        if i >= n:
            yield item

def sliding_window(n: int, gen: Iterator[T]) -> Iterator[tuple]:
    """Yield sliding windows of size n."""
    from collections import deque
    window = deque(maxlen=n)
    for item in gen:
        window.append(item)
        if len(window) == n:
            yield tuple(window)

def zip_streams(*streams: Iterator) -> Iterator[tuple]:
    """Lazy zip over multiple streams (stops at shortest)."""
    return zip(*streams)

def flatten_once(gen: Iterator) -> Iterator:
    """Flatten one level of nesting."""
    for item in gen:
        if hasattr(item, '__iter__') and not isinstance(item, (str, bytes)):
            yield from item
        else:
            yield item

class Pipeline:
    """Fluent API for generator pipelines."""

    def __init__(self, source: Iterator):
        self._gen = iter(source)

    def map(self, func):
        self._gen = gen_map(func, self._gen)
        return self

    def filter(self, pred):
        self._gen = gen_filter(pred, self._gen)
        return self

    def limit(self, n: int):
        self._gen = gen_limit(n, self._gen)
        return self

    def skip(self, n: int):
        self._gen = gen_skip(n, self._gen)
        return self

    def take(self, n: int) -> list:
        return list(itertools.islice(self._gen, n))

    def collect(self) -> list:
        return list(self._gen)

    def sum(self) -> int | float:
        return sum(self._gen)

    def first(self, default=None):
        return next(self._gen, default)

# ═══════════════════════════════════════════
# 3. Coroutines (data-driven generators)
# ═══════════════════════════════════════════
def accumulator() -> Generator[float, float, float]:
    """Coroutine that accumulates values sent to it."""
    total = 0.0
    while True:
        value = yield total
        if value is None:
            return total
        total += value

def running_average() -> Generator[float, float, None]:
    """Coroutine that yields running average of sent values."""
    total, count = 0.0, 0
    while True:
        value = yield total / count if count else 0.0
        total += value
        count += 1

def prime_filter_coro() -> Generator[int, int, None]:
    """Coroutine: receives integers, yields only primes."""
    def is_prime(n):
        if n < 2: return False
        if n == 2: return True
        if n % 2 == 0: return False
        return all(n % i != 0 for i in range(3, int(n**0.5)+1, 2))

    while True:
        n = yield
        if is_prime(n):
            print(f"  prime: {n}")

# ═══════════════════════════════════════════
# 4. Async generators (syntax demo — no event loop needed here)
# ═══════════════════════════════════════════
async def async_range(start: int, stop: int, step: int = 1):
    """Async generator version of range."""
    current = start
    while current < stop:
        yield current
        current += step

async def async_fibonacci(limit: int = 10):
    a, b = 0, 1
    count = 0
    while count < limit:
        yield a
        a, b = b, a + b
        count += 1

import asyncio

async def demo_async_generators():
    print("\n=== Async Generators ===")
    result = [x async for x in async_range(0, 10, 2)]
    print(f"  async range(0,10,2): {result}")

    fibs = [x async for x in async_fibonacci(8)]
    print(f"  async fibonacci(8): {fibs}")

    # Async pipelines
    async def async_filter(gen, pred):
        async for item in gen:
            if pred(item):
                yield item

    evens = [x async for x in async_filter(async_range(0, 20), lambda x: x % 2 == 0)]
    print(f"  async evens 0-20: {evens}")

# ═══════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════
if __name__ == "__main__":
    print("=== Infinite Sequences ===")
    print(f"Naturals:     {take(10, naturals())}")
    print(f"Fibonacci:    {take(12, fibonacci())}")
    print(f"Primes:       {take(20, primes())}")
    print(f"Powers of 2:  {take(10, powers_of(2))}")
    print(f"Powers of 3:  {take(8, powers_of(3))}")

    print("\n=== Cycle with Index ===")
    for cycle, item in itertools.islice(cycle_with_index("ABC"), 9):
        print(f"  cycle={cycle} item={item}")

    print("\n=== Sliding Window ===")
    data = [1, 2, 3, 4, 5, 6, 7]
    windows = list(sliding_window(3, iter(data)))
    print(f"  window(3): {windows}")

    print("\n=== Fluent Pipeline ===")
    result = (
        Pipeline(naturals())
        .filter(lambda x: x % 2 == 0)   # evens
        .map(lambda x: x ** 2)           # square
        .filter(lambda x: x % 3 != 0)   # not divisible by 3
        .take(10)
    )
    print(f"  Even squares not div by 3: {result}")

    # Sum of first 1000 prime numbers
    prime_sum = Pipeline(primes()).limit(1000).sum()
    print(f"  Sum of first 1000 primes: {prime_sum}")

    print("\n=== Coroutines ===")
    acc = accumulator()
    next(acc)  # prime
    for v in [1.5, 2.0, 3.5, 4.0]:
        total = acc.send(v)
    print(f"  Accumulator after [1.5,2.0,3.5,4.0]: {total}")

    avg_coro = running_average()
    next(avg_coro)
    readings = [78, 82, 65, 90, 70]
    for r in readings:
        cur_avg = avg_coro.send(r)
    print(f"  Running avg of {readings}: {cur_avg:.2f}")

    asyncio.run(demo_async_generators())
