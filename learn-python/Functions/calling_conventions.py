"""
Functions: Argument patterns, closures, decorators, and advanced calling conventions.
"""
import functools
import inspect
import time
from typing import Any, Callable, TypeVar

T = TypeVar("T")

# ═══════════════════════════════════════════
# 1. Argument patterns
# ═══════════════════════════════════════════
def positional_only(x: int, y: int, /, z: int = 0) -> int:
    """x, y are positional-only (Python 3.8+ /)."""
    return x + y + z

def keyword_only(*, name: str, age: int, city: str = "NYC") -> str:
    """All args after * must be keyword."""
    return f"{name}, {age}, {city}"

def variadic(*args: int, sep: str = ", ", **kwargs: str) -> str:
    return sep.join(str(a) for a in args) + " " + str(kwargs)

# ═══════════════════════════════════════════
# 2. Closures
# ═══════════════════════════════════════════
def make_adder(n: int) -> Callable[[int], int]:
    def add(x: int) -> int: return x + n
    add.__name__ = f"add_{n}"
    return add

def make_counter(start: int = 0):
    count = [start]
    def increment(by: int = 1) -> int:
        count[0] += by; return count[0]
    def reset(): count[0] = start
    def value(): return count[0]
    increment.reset = reset
    increment.value = value
    return increment

def cycle_factory(items: list) -> Callable[[], Any]:
    idx = [0]
    def next_item():
        item = items[idx[0] % len(items)]; idx[0] += 1; return item
    return next_item

# ═══════════════════════════════════════════
# 3. Parametrized decorators
# ═══════════════════════════════════════════
def retry(max_attempts: int = 3, exceptions: tuple = (Exception,), delay: float = 0.0):
    def decorator(fn: Callable):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except exceptions as e:
                    last_exc = e
                    print(f"  [retry] {fn.__name__} attempt {attempt}/{max_attempts}: {e}")
                    if delay and attempt < max_attempts:
                        time.sleep(delay)
            raise last_exc
        return wrapper
    return decorator

def validate_types(**types):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            sig = inspect.signature(fn)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()
            for param_name, expected_type in types.items():
                if param_name in bound.arguments:
                    val = bound.arguments[param_name]
                    if not isinstance(val, expected_type):
                        raise TypeError(
                            f"{fn.__name__}() param {param_name!r}: "
                            f"expected {expected_type.__name__}, got {type(val).__name__}"
                        )
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def memoize(maxsize: int | None = 128):
    """@memoize() or @memoize(maxsize=None) for unlimited."""
    def decorator(fn):
        return functools.lru_cache(maxsize=maxsize)(fn)
    return decorator

# ═══════════════════════════════════════════
# 4. inspect usage
# ═══════════════════════════════════════════
def introspect(fn: Callable) -> dict:
    sig   = inspect.signature(fn)
    hints = fn.__annotations__
    return {
        "name":   fn.__name__,
        "params": {
            name: {
                "kind":    param.kind.name,
                "default": None if param.default is inspect.Parameter.empty else param.default,
                "annotation": str(hints.get(name, "?")),
            }
            for name, param in sig.parameters.items()
        },
        "return": str(hints.get("return", "?")),
        "is_coroutine": inspect.iscoroutinefunction(fn),
    }

# ═══════════════════════════════════════════
# 5. Callable class (Timer)
# ═══════════════════════════════════════════
class Timer:
    def __init__(self, name: str = ""):
        self.name = name; self.elapsed: float = 0.0

    def __enter__(self):
        self._start = time.perf_counter(); return self

    def __exit__(self, *_):
        self.elapsed = time.perf_counter() - self._start
        if self.name:
            print(f"  [{self.name}] {self.elapsed*1000:.2f}ms")

    def __call__(self, fn: Callable) -> Callable:
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            with Timer(fn.__name__):
                return fn(*args, **kwargs)
        return wrapper

# ═══════════════════════════════════════════
# 6. functools.singledispatch
# ═══════════════════════════════════════════
@functools.singledispatch
def serialize(obj) -> str:
    return repr(obj)

@serialize.register(int)
@serialize.register(float)
def _(obj) -> str: return str(obj)

@serialize.register(list)
def _(obj: list) -> str: return "[" + ", ".join(serialize(x) for x in obj) + "]"

@serialize.register(dict)
def _(obj: dict) -> str:
    return "{" + ", ".join(f"{serialize(k)}: {serialize(v)}" for k, v in obj.items()) + "}"

# ═══════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════
if __name__ == "__main__":
    print("=== Argument patterns ===")
    print(f"  positional_only(1,2,3): {positional_only(1,2,3)}")
    print(f"  keyword_only(name='X',age=30): {keyword_only(name='X', age=30)}")
    print(f"  variadic(1,2,3,sep='-',x='a'): {variadic(1,2,3,sep='-',x='a')}")
    try:
        positional_only(x=1, y=2)
    except TypeError as e:
        print(f"  positional-only error: {e}")

    print("\n=== Closures ===")
    add10 = make_adder(10)
    print(f"  add10(5) = {add10(5)}")
    cnt = make_counter(0)
    print(f"  counter: {[cnt() for _ in range(5)]}")
    cnt.reset()
    print(f"  after reset: {cnt.value()}")
    next_color = cycle_factory(["red", "green", "blue"])
    print(f"  cycle: {[next_color() for _ in range(5)]}")

    print("\n=== @retry ===")
    attempt_count = [0]
    @retry(max_attempts=3, exceptions=(ValueError,))
    def flaky():
        attempt_count[0] += 1
        if attempt_count[0] < 3: raise ValueError("Not yet!")
        return "Success"
    print(f"  Result: {flaky()!r}")

    print("\n=== @validate_types ===")
    @validate_types(name=str, age=int)
    def greet(name: str, age: int) -> str:
        return f"Hello {name}, age {age}"
    print(f"  {greet('Alice', 30)}")
    try:
        greet("Bob", "thirty")
    except TypeError as e:
        print(f"  Type error: {e}")

    print("\n=== @memoize ===")
    @memoize(maxsize=64)
    def fib(n: int) -> int:
        return n if n < 2 else fib(n-1) + fib(n-2)
    print(f"  fib(30) = {fib(30)}, cache_info: {fib.cache_info()}")

    print("\n=== Introspection ===")
    info = introspect(greet)
    print(f"  Name: {info['name']}, is_coroutine: {info['is_coroutine']}")
    for pname, pinfo in info["params"].items():
        print(f"  Param {pname}: {pinfo['kind']}, annotation={pinfo['annotation']}")

    print("\n=== singledispatch ===")
    for val in [42, 3.14, [1, 2, 3], {"a": 1, "b": [2, 3]}, "hello"]:
        print(f"  serialize({val!r}) → {serialize(val)}")

    print("\n=== Timer ===")
    with Timer("list-comp") as t:
        data = [x**2 for x in range(100_000)]
    print(f"  list-comp elapsed: {t.elapsed*1000:.2f}ms (length={len(data)})")
