"""
Advanced Python: Python's type system — generics, TypeVar, overload, TypedDict.
"""
from typing import (
    TypeVar, Generic, overload, TypedDict, Union, Literal,
    NamedTuple, Final, ClassVar, Annotated, get_type_hints,
    get_args, get_origin
)
from dataclasses import dataclass
import inspect

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")
Num = TypeVar("Num", int, float, complex)

# ═══════════════════════════════════════════
# 1. Generic classes
# ═══════════════════════════════════════════
class Stack(Generic[T]):
    """Type-safe generic stack."""
    def __init__(self): self._data: list[T] = []
    def push(self, item: T) -> None:  self._data.append(item)
    def pop(self)  -> T:              return self._data.pop()
    def peek(self) -> T | None:       return self._data[-1] if self._data else None
    def __len__(self):                return len(self._data)
    def __repr__(self):               return f"Stack[{T}]({self._data})"

class Pair(Generic[K, V]):
    def __init__(self, key: K, value: V):
        self.key = key; self.value = value
    def swap(self) -> "Pair[V, K]":
        return Pair(self.value, self.key)
    def __repr__(self): return f"Pair({self.key!r}: {self.value!r})"

# ═══════════════════════════════════════════
# 2. TypeVar constraints and bounds
# ═══════════════════════════════════════════
Comparable = TypeVar("Comparable", bound="Comparable")

def max_of(*values: Num) -> Num:
    """Works with int, float, and complex constraints."""
    if not values:
        raise ValueError("At least one value required")
    return max(values)  # type: ignore

def binary_search(arr: list[T], target: T, key=None) -> int:
    """Return index of target or -1. arr must be sorted."""
    lo, hi = 0, len(arr) - 1
    key = key or (lambda x: x)
    t = key(target)
    while lo <= hi:
        mid = (lo + hi) // 2
        m = key(arr[mid])
        if m == t: return mid
        if m < t:  lo = mid + 1
        else:      hi = mid - 1
    return -1

# ═══════════════════════════════════════════
# 3. @overload — different signatures
# ═══════════════════════════════════════════
@overload
def process(value: int) -> str: ...
@overload
def process(value: str) -> int: ...
@overload
def process(value: list[int]) -> float: ...

def process(value):
    """Single implementation, multiple overloaded signatures."""
    if isinstance(value, int):
        return str(value * 2)
    elif isinstance(value, str):
        return len(value)
    elif isinstance(value, list):
        return sum(value) / len(value) if value else 0.0
    raise TypeError(f"Unsupported type: {type(value)}")

# ═══════════════════════════════════════════
# 4. TypedDict — typed dictionaries
# ═══════════════════════════════════════════
class UserBase(TypedDict):
    id:    int
    name:  str
    email: str

class User(UserBase, total=False):
    """total=False means optional keys."""
    age:    int
    bio:    str
    avatar: str

class APIResponse(TypedDict):
    status:  Literal["ok", "error"]
    data:    list[User]
    total:   int
    page:    int
    message: str

# ═══════════════════════════════════════════
# 5. NamedTuple with types
# ═══════════════════════════════════════════
class Point(NamedTuple):
    x: float
    y: float
    z: float = 0.0

    def distance_to(self, other: "Point") -> float:
        return ((self.x-other.x)**2 + (self.y-other.y)**2 + (self.z-other.z)**2) ** 0.5

class Config(NamedTuple):
    host: str
    port: int
    debug: bool = False
    max_connections: int = 100

# ═══════════════════════════════════════════
# 6. Annotated — metadata for validators
# ═══════════════════════════════════════════
from dataclasses import dataclass as dc

@dataclass
class Gt:
    """Annotated metadata: greater than."""
    min_val: float

@dataclass
class Le:
    """Annotated metadata: less than or equal."""
    max_val: float

@dataclass
class Regex:
    pattern: str

# Use Annotated types as documentation/validator hints
PositiveFloat = Annotated[float, Gt(0)]
Percentage    = Annotated[float, Gt(0), Le(100)]
Email         = Annotated[str, Regex(r"^[^@]+@[^@]+\.[^@]+$")]

def validate_annotated(value, annotation):
    """Inspect Annotated metadata and validate."""
    origin = get_origin(annotation)
    if origin is not Annotated:
        return True
    base, *metadata = get_args(annotation)
    for constraint in metadata:
        if isinstance(constraint, Gt) and not (value > constraint.min_val):
            raise ValueError(f"{value} must be > {constraint.min_val}")
        if isinstance(constraint, Le) and not (value <= constraint.max_val):
            raise ValueError(f"{value} must be <= {constraint.max_val}")
    return True

# ═══════════════════════════════════════════
# 7. Literal and Final
# ═══════════════════════════════════════════
HTTPMethod = Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]
LogLevel   = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

MAX_RETRIES: Final = 3
API_VERSION: Final[str] = "v2"

@dataclass
class HTTPRequest:
    method: HTTPMethod
    url: str
    headers: dict[str, str]

# ═══════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════
if __name__ == "__main__":
    print("=== Generic Stack ===")
    s: Stack[int] = Stack()
    for v in [1, 2, 3, 4, 5]:
        s.push(v)
    print(f"Stack: len={len(s)}, peek={s.peek()}, pop={s.pop()}, len={len(s)}")

    sp: Stack[str] = Stack()
    for w in ["hello", "world"]:
        sp.push(w)
    print(f"String stack peek: {sp.peek()!r}")

    print("\n=== Generic Pair ===")
    p = Pair("key", 42)
    print(f"Pair: {p}")
    print(f"Swapped: {p.swap()}")

    print("\n=== Binary Search ===")
    arr = [1, 3, 5, 7, 9, 11, 13, 15]
    for target in [7, 15, 4]:
        idx = binary_search(arr, target)
        print(f"  search({target}): idx={idx}")

    print("\n=== @overload ===")
    print(f"  process(42):       {process(42)!r}")
    print(f"  process('hello'):  {process('hello')!r}")
    print(f"  process([1,2,3]): {process([1, 2, 3])!r}")

    print("\n=== TypedDict ===")
    user: User = {"id": 1, "name": "Alice", "email": "alice@example.com", "age": 30}
    print(f"  User: {user}")

    resp: APIResponse = {
        "status": "ok", "data": [user], "total": 1, "page": 1, "message": "ok"
    }
    print(f"  API response: status={resp['status']}, total={resp['total']}")

    print("\n=== NamedTuple ===")
    p1, p2 = Point(0, 0), Point(3, 4)
    print(f"  Distance {p1} → {p2}: {p1.distance_to(p2)}")
    cfg = Config("localhost", 8080, debug=True)
    print(f"  Config: {cfg}")

    print("\n=== Annotated Validation ===")
    for val, annotation in [(5.0, PositiveFloat), (0.0, PositiveFloat), (50.0, Percentage), (150.0, Percentage)]:
        try:
            validate_annotated(val, annotation)
            print(f"  {val} → valid")
        except ValueError as e:
            print(f"  {val} → invalid: {e}")

    print("\n=== Final ===")
    print(f"  MAX_RETRIES: {MAX_RETRIES}")
    print(f"  API_VERSION: {API_VERSION}")
