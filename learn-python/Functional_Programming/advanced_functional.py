"""
Functional Programming: Higher-order functions, closures, currying, and functools.
"""
import functools
import operator
from typing import TypeVar, Callable, Iterable, Any

T = TypeVar("T")
U = TypeVar("U")

# ═══════════════════════════════════════════
# 1. Higher-order functions
# ═══════════════════════════════════════════
def apply_twice(f: Callable[[T], T], x: T) -> T:
    return f(f(x))

def compose(*fns: Callable) -> Callable:
    """Compose functions right-to-left: compose(f, g)(x) = f(g(x))."""
    def composed(x):
        for fn in reversed(fns):
            x = fn(x)
        return x
    return composed

def pipe(*fns: Callable) -> Callable:
    """Apply functions left-to-right: pipe(f, g)(x) = g(f(x))."""
    def piped(x):
        for fn in fns:
            x = fn(x)
        return x
    return piped

# ═══════════════════════════════════════════
# 2. Closures and factories
# ═══════════════════════════════════════════
def make_multiplier(factor: float) -> Callable[[float], float]:
    """Closure — captures `factor` in its scope."""
    def multiply(x: float) -> float:
        return x * factor
    multiply.__name__ = f"multiply_by_{factor}"
    return multiply

def make_validator(*rules: Callable[[Any], bool]) -> Callable[[Any], bool]:
    """Combine multiple validation predicates into one."""
    def validate(value) -> bool:
        return all(rule(value) for rule in rules)
    return validate

def counter(start: int = 0, step: int = 1) -> Callable[[], int]:
    """Stateful closure via mutable container."""
    state = [start]
    def increment() -> int:
        val = state[0]; state[0] += step; return val
    return increment

# ═══════════════════════════════════════════
# 3. Currying and partial application
# ═══════════════════════════════════════════
def curry(fn: Callable) -> Callable:
    """Auto-currying based on function arity."""
    import inspect
    n = len(inspect.signature(fn).parameters)
    def curried(*args):
        if len(args) >= n:
            return fn(*args[:n])
        return lambda *more: curried(*(args + more))
    return curried

@curry
def add3(a: int, b: int, c: int) -> int:
    return a + b + c

# functools.partial
double   = functools.partial(operator.mul, 2)
add5     = functools.partial(operator.add, 5)
left_pad = functools.partial(str.rjust, width=10, fillchar="0")

# ═══════════════════════════════════════════
# 4. functools higher-order tools
# ═══════════════════════════════════════════
@functools.lru_cache(maxsize=128)
def fib(n: int) -> int:
    return n if n < 2 else fib(n-1) + fib(n-2)

@functools.cache   # unbounded (Python 3.9+)
def collatz_len(n: int) -> int:
    if n == 1: return 1
    return 1 + collatz_len(n // 2 if n % 2 == 0 else 3 * n + 1)

def demo_reduce():
    print("\n=== reduce ===")
    nums = [1, 2, 3, 4, 5]
    product = functools.reduce(operator.mul, nums)
    max_val = functools.reduce(lambda a, b: a if a > b else b, nums)
    flatten = functools.reduce(lambda acc, x: acc + x, [[1,2],[3,4],[5,6]], [])
    print(f"  product: {product}, max: {max_val}, flatten: {flatten}")

# ═══════════════════════════════════════════
# 5. map, filter, zip pipelines
# ═══════════════════════════════════════════
def demo_builtins():
    print("\n=== map / filter / zip ===")
    nums = range(1, 11)

    # map
    squares = list(map(lambda x: x**2, nums))
    print(f"  squares: {squares}")

    # filter
    primes = list(filter(
        lambda n: n > 1 and all(n % d != 0 for d in range(2, int(n**0.5)+1)),
        range(2, 30)
    ))
    print(f"  primes<30: {primes}")

    # zip
    keys   = ["a", "b", "c"]
    values = [1, 2, 3]
    print(f"  dict(zip): {dict(zip(keys, values))}")

    # Chained pipeline using generators
    pipeline = filter(
        lambda x: x % 3 == 0,
        map(lambda x: x**2, range(1, 20))
    )
    print(f"  squares divisible by 3: {list(pipeline)}")

# ═══════════════════════════════════════════
# 6. @functools.wraps, caching, total_ordering
# ═══════════════════════════════════════════
def trace(fn: Callable) -> Callable:
    @functools.wraps(fn)            # preserves __name__, __doc__
    def wrapper(*args, **kwargs):
        print(f"  CALL {fn.__name__}({args}, {kwargs})")
        result = fn(*args, **kwargs)
        print(f"  RETURN {result!r}")
        return result
    return wrapper

@functools.total_ordering
class Version:
    def __init__(self, major, minor, patch):
        self.v = (major, minor, patch)
    def __eq__(self, other): return self.v == other.v
    def __lt__(self, other): return self.v < other.v
    def __repr__(self):      return "v" + ".".join(map(str, self.v))

# ═══════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════
if __name__ == "__main__":
    print("=== Higher-order functions ===")
    print(f"  apply_twice(x+3, 7) = {apply_twice(lambda x: x+3, 7)}")

    normalize = pipe(str.strip, str.lower, lambda s: s.replace(" ", "_"))
    print(f"  pipe: {normalize('  Hello World  ')!r}")

    shout = compose(str.upper, str.strip)
    print(f"  compose: {shout('  hello  ')!r}")

    print("\n=== Closures ===")
    triple = make_multiplier(3)
    print(f"  triple(7) = {triple(7)}")
    cnt = counter(0, 2)
    print(f"  counter: {[cnt() for _ in range(5)]}")

    is_valid_age = make_validator(
        lambda x: isinstance(x, int),
        lambda x: 0 <= x <= 150
    )
    for v in [25, -1, 200, "old"]:
        print(f"  is_valid_age({v!r}) = {is_valid_age(v)}")

    print("\n=== Currying ===")
    print(f"  add3(1)(2)(3) = {add3(1)(2)(3)}")
    print(f"  add3(1, 2)(3) = {add3(1, 2)(3)}")
    print(f"  add3(1, 2, 3) = {add3(1, 2, 3)}")

    print("\n=== Partial application ===")
    print(f"  double(9) = {double(9)}")
    print(f"  add5(10)  = {add5(10)}")
    print(f"  left_pad('42') = {left_pad('42')!r}")

    print("\n=== lru_cache / cache ===")
    import sys
    fib(30)
    print(f"  fib(30) = {fib(30)}, cache_info = {fib.cache_info()}")
    longest = max(range(1, 100), key=collatz_len)
    print(f"  Longest Collatz sequence under 100: starts at {longest} ({collatz_len(longest)} steps)")

    demo_reduce()
    demo_builtins()

    print("\n=== @functools.wraps ===")
    @trace
    def multiply(a, b): return a * b
    multiply(3, 4)
    print(f"  name preserved: {multiply.__name__!r}")

    print("\n=== total_ordering ===")
    versions = [Version(1,10,0), Version(2,0,0), Version(1,9,5)]
    print(f"  sorted: {sorted(versions)}")
    v1, v2 = Version(1,0,0), Version(2,0,0)
    print(f"  {v1} <= {v2}: {v1 <= v2}")
    print(f"  {v2} >= {v1}: {v2 >= v1}")
