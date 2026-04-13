"""
Performance and Optimization: Memory and CPU profiling techniques.
"""
import sys
import time
import functools
from collections import defaultdict

# === 1. Memory measurement ===
print("=== Memory Usage ===")

def get_size(obj, seen=None):
    """Recursively calculate size of objects."""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum(get_size(k, seen) + get_size(v, seen) for k, v in obj.items())
    elif isinstance(obj, (list, tuple, set, frozenset)):
        size += sum(get_size(i, seen) for i in obj)
    return size

# Compare data structures
data_list = list(range(1000))
data_tuple = tuple(range(1000))
data_set = set(range(1000))
data_dict = {i: i for i in range(1000)}

for name, data in [("list", data_list), ("tuple", data_tuple),
                    ("set", data_set), ("dict", data_dict)]:
    print(f"  {name:6s}: {get_size(data):,} bytes")

# === 2. Timing decorator ===
print("\n=== Timing ===")

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"  {func.__name__}: {elapsed:.6f}s")
        return result
    return wrapper

@timer
def list_comprehension(n):
    return [i**2 for i in range(n)]

@timer
def generator_sum(n):
    return sum(i**2 for i in range(n))

@timer
def map_approach(n):
    return list(map(lambda x: x**2, range(n)))

n = 100_000
list_comprehension(n)
generator_sum(n)
map_approach(n)

# === 3. Caching ===
print("\n=== Caching ===")

@timer
def fib_naive(n):
    if n < 2:
        return n
    return fib_naive.__wrapped__(n-1) + fib_naive.__wrapped__(n-2) if hasattr(fib_naive, '__wrapped__') else n

@functools.lru_cache(maxsize=None)
def fib_cached(n):
    if n < 2:
        return n
    return fib_cached(n-1) + fib_cached(n-2)

start = time.perf_counter()
result = fib_cached(100)
elapsed = time.perf_counter() - start
print(f"  fib_cached(100) = {result} ({elapsed:.6f}s)")
print(f"  Cache info: {fib_cached.cache_info()}")

# === 4. String concatenation ===
print("\n=== String Concat ===")

@timer
def concat_plus(n):
    s = ""
    for i in range(n):
        s += str(i)
    return len(s)

@timer
def concat_join(n):
    return len("".join(str(i) for i in range(n)))

@timer
def concat_list(n):
    parts = []
    for i in range(n):
        parts.append(str(i))
    return len("".join(parts))

n = 50_000
concat_plus(n)
concat_join(n)
concat_list(n)

# === 5. Dict vs defaultdict vs Counter ===
print("\n=== Counting Performance ===")

words = "the quick brown fox jumps over the lazy dog the fox".split() * 10000

@timer
def count_dict(words):
    counts = {}
    for w in words:
        counts[w] = counts.get(w, 0) + 1
    return counts

@timer
def count_defaultdict(words):
    counts = defaultdict(int)
    for w in words:
        counts[w] += 1
    return dict(counts)

@timer
def count_counter(words):
    from collections import Counter
    return dict(Counter(words))

count_dict(words)
count_defaultdict(words)
count_counter(words)

# === 6. Generator vs list memory ===
print("\n=== Generator vs List Memory ===")

list_size = sys.getsizeof([i for i in range(100_000)])
gen_size = sys.getsizeof(i for i in range(100_000))
print(f"  List: {list_size:,} bytes")
print(f"  Generator: {gen_size:,} bytes")
print(f"  Ratio: {list_size/gen_size:.0f}x")

# === 7. __slots__ comparison ===
print("\n=== __slots__ Memory ===")

class RegularClass:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class SlottedClass:
    __slots__ = ('x', 'y', 'z')
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

r = RegularClass(1, 2, 3)
s = SlottedClass(1, 2, 3)
r_size = sys.getsizeof(r) + sys.getsizeof(r.__dict__)
s_size = sys.getsizeof(s)
print(f"  Regular: {r_size} bytes")
print(f"  Slotted: {s_size} bytes")
print(f"  Savings: {r_size - s_size} bytes")
