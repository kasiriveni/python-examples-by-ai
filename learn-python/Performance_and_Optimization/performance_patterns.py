"""
Performance and Optimization: Profiling, algorithmic complexity, memory, and caching.
"""
from __future__ import annotations
import time
import sys
import gc
import array
import functools
import itertools
import bisect
from collections import defaultdict
from typing import Callable, TypeVar

T = TypeVar("T")

# ═══════════════════════════════════════════
# 1. Timing utilities
# ═══════════════════════════════════════════
class Timer:
    def __init__(self, name: str = ""):
        self.name = name
        self.elapsed: float = 0.0

    def __enter__(self):
        self._start = time.perf_counter()
        return self

    def __exit__(self, *_):
        self.elapsed = time.perf_counter() - self._start
        if self.name:
            print(f"  [{self.name}] {self.elapsed*1000:.3f}ms")

def timeit(fn: Callable, *args, n: int = 1, **kwargs) -> float:
    """Run fn(*args, **kwargs) n times, return mean runtime in ms."""
    start = time.perf_counter()
    for _ in range(n):
        fn(*args, **kwargs)
    return (time.perf_counter() - start) * 1000 / n

# ═══════════════════════════════════════════
# 2. O(n²) vs O(n log n) vs O(n) patterns
# ═══════════════════════════════════════════
def has_duplicates_o_n2(lst: list) -> bool:           # O(n²) — nested loop
    for i in range(len(lst)):
        for j in range(i+1, len(lst)):
            if lst[i] == lst[j]: return True
    return False

def has_duplicates_o_n(lst: list) -> bool:             # O(n) — hash set
    return len(set(lst)) != len(lst)

def two_sum_o_n2(nums: list[int], target: int) -> tuple[int,int] | None:
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            if nums[i] + nums[j] == target: return (i, j)
    return None

def two_sum_o_n(nums: list[int], target: int) -> tuple[int,int] | None:
    seen: dict[int, int] = {}
    for i, n in enumerate(nums):
        complement = target - n
        if complement in seen: return (seen[complement], i)
        seen[n] = i
    return None

def binary_search(lst: list, target) -> int:
    """O(log n) binary search; returns index or -1."""
    lo, hi = 0, len(lst) - 1
    while lo <= hi:
        mid = (lo + hi) >> 1
        if lst[mid] == target: return mid
        elif lst[mid] < target: lo = mid + 1
        else: hi = mid - 1
    return -1

# ═══════════════════════════════════════════
# 3. Memory-efficient alternatives
# ═══════════════════════════════════════════
def compare_memory():
    """Compare memory sizes of list, tuple, generator, array."""
    n = 10_000
    a_list  = list(range(n))
    a_tuple = tuple(range(n))
    a_arr   = array.array("i", range(n))  # C int array
    a_gen   = (x for x in range(n))       # generator object

    print("=== Memory sizes ===")
    print(f"  list({n}):    {sys.getsizeof(a_list):>8} bytes")
    print(f"  tuple({n}):   {sys.getsizeof(a_tuple):>8} bytes")
    print(f"  array({n}):   {sys.getsizeof(a_arr):>8} bytes")
    print(f"  generator:  {sys.getsizeof(a_gen):>8} bytes (lazy)")

def use_generators_not_lists(n: int) -> int:
    """Generator pipeline uses O(1) memory regardless of n."""
    return sum(x*x for x in range(n) if x % 2 == 0)

# ═══════════════════════════════════════════
# 4. Memoization and caching
# ═══════════════════════════════════════════
@functools.lru_cache(maxsize=None)
def fib_memo(n: int) -> int:
    if n < 2: return n
    return fib_memo(n-1) + fib_memo(n-2)

def fib_iter(n: int) -> int:
    """O(n) time, O(1) space — iterative beats recursive even with memoization."""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

def memoize(fn: Callable) -> Callable:
    cache: dict = {}
    @functools.wraps(fn)
    def wrapper(*args):
        if args not in cache:
            cache[args] = fn(*args)
        return cache[args]
    wrapper.cache = cache      # type: ignore
    return wrapper

@memoize
def expensive_power(base: int, exp: int) -> int:
    return base ** exp

# ═══════════════════════════════════════════
# 5. Efficient string building
# ═══════════════════════════════════════════
def concat_bad(words: list[str]) -> str:
    result = ""
    for w in words:   # O(n²) — creates new string each iteration
        result += w + " "
    return result.rstrip()

def concat_good(words: list[str]) -> str:
    return " ".join(words)  # O(n) — single concatenation

def build_csv_row_bad(fields: list[str]) -> str:
    s = ""
    for i, f in enumerate(fields):
        s += f if i == 0 else "," + f
    return s

def build_csv_row_good(fields: list[str]) -> str:
    return ",".join(fields)

# ═══════════════════════════════════════════
# 6. Sorting optimizations
# ═══════════════════════════════════════════
def sort_by_multiple_keys(people: list[dict]) -> list[dict]:
    """Sort by (department, -salary, name) — Schwartzian transform."""
    return sorted(people,
                  key=lambda p: (p["dept"], -p["salary"], p["name"]))

def group_consecutive(lst: list[int]) -> list[list[int]]:
    """Group consecutive integers without sorting: O(n)."""
    if not lst: return []
    groups: list[list[int]] = []
    group = [lst[0]]
    for n in lst[1:]:
        if n == group[-1] + 1:
            group.append(n)
        else:
            groups.append(group)
            group = [n]
    groups.append(group)
    return groups

def sliding_window_max(nums: list[int], k: int) -> list[int]:
    """O(n) sliding window maximum using a deque."""
    from collections import deque
    dq: deque[int] = deque()
    result = []
    for i, num in enumerate(nums):
        while dq and nums[dq[-1]] <= num:
            dq.pop()
        dq.append(i)
        if dq[0] == i - k:
            dq.popleft()
        if i >= k - 1:
            result.append(nums[dq[0]])
    return result

# ═══════════════════════════════════════════
# 7. Benchmarking helpers
# ═══════════════════════════════════════════
def benchmark(implementations: dict[str, Callable], *args,
              n_runs: int = 1000, **kwargs) -> dict[str, float]:
    """Benchmark multiple implementations of the same function."""
    results: dict[str, float] = {}
    for label, fn in implementations.items():
        ms = timeit(fn, *args, n=n_runs, **kwargs)
        results[label] = ms
    return results

# ═══════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════
if __name__ == "__main__":
    print("=== Timer ===")
    with Timer("list comprehension"):
        data = [x**2 for x in range(100_000)]

    print("\n=== O(n) vs O(n²) duplicate check ===")
    sample = list(range(5_000))
    ms_n2 = timeit(has_duplicates_o_n2, sample, n=10)
    ms_n  = timeit(has_duplicates_o_n,  sample, n=10)
    print(f"  O(n²): {ms_n2:.2f}ms  |  O(n): {ms_n:.4f}ms  "
          f"| speedup: {ms_n2/ms_n:.0f}x")

    print("\n=== Two-sum comparison ===")
    big_list = list(range(10_000)); target = 9999
    ms_n2 = timeit(two_sum_o_n2, big_list, target, n=5)
    ms_n  = timeit(two_sum_o_n,  big_list, target, n=100)
    print(f"  O(n²): {ms_n2:.2f}ms  |  O(n): {ms_n:.4f}ms")

    print("\n=== Binary search ===")
    sorted_data = list(range(1_000_000))
    with Timer("bisect.bisect_left"):
        idx = bisect.bisect_left(sorted_data, 999_900)
    print(f"  bisect found at index {idx}")

    compare_memory()

    print("\n=== Fibonacci ===")
    n = 35
    t_memo = timeit(fib_memo,  n, n=100)
    t_iter = timeit(fib_iter,  n, n=100)
    print(f"  fib_memo({n}): {t_memo:.4f}ms")
    print(f"  fib_iter({n}): {t_iter:.4f}ms  (same result: {fib_iter(n) == fib_memo(n)})")
    fib_memo.cache_clear()

    print("\n=== String concatenation ===")
    words = ["word"] * 1000
    t_bad  = timeit(concat_bad,  words, n=500)
    t_good = timeit(concat_good, words, n=500)
    print(f"  concat_bad:  {t_bad:.4f}ms")
    print(f"  concat_good: {t_good:.4f}ms  | speedup: {t_bad/t_good:.1f}x")

    print("\n=== Sliding window max ===")
    nums = [1, 3, -1, -3, 5, 3, 6, 7]
    print(f"  nums={nums}")
    for k in [3, 4]:
        print(f"  window={k}: {sliding_window_max(nums, k)}")

    print("\n=== Group consecutive ===")
    ints = [1,2,3,7,8,9,15,16]
    print(f"  {ints} → {group_consecutive(ints)}")
