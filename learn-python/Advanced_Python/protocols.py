"""
Advanced Python: Protocols and structural subtyping (PEP 544).
"""
from typing import Protocol, runtime_checkable, TypeVar, SupportsFloat, SupportsInt
from abc import abstractmethod

# ═══════════════════════════════════════════
# 1. Defining Protocols
# ═══════════════════════════════════════════
@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> str: ...

@runtime_checkable
class Serializable(Protocol):
    def to_dict(self) -> dict: ...
    def to_json(self) -> str: ...

@runtime_checkable
class Comparable(Protocol):
    def __lt__(self, other) -> bool: ...
    def __eq__(self, other) -> bool: ...

# ─────────────────────────────────────────
# Classes that IMPLICITLY implement protocols
# ─────────────────────────────────────────
import json

class Circle:
    def __init__(self, r): self.r = r
    def draw(self) -> str: return f"○ circle(r={self.r})"
    def to_dict(self) -> dict: return {"type": "circle", "r": self.r}
    def to_json(self) -> str: return json.dumps(self.to_dict())
    def __lt__(self, other): return self.r < other.r
    def __eq__(self, other): return self.r == other.r

class Rectangle:
    def __init__(self, w, h): self.w = w; self.h = h
    def draw(self) -> str: return f"▭ rect({self.w}x{self.h})"
    def to_dict(self) -> dict: return {"type": "rect", "w": self.w, "h": self.h}
    def to_json(self) -> str: return json.dumps(self.to_dict())
    def __lt__(self, other): return self.w*self.h < other.w*other.h
    def __eq__(self, other): return self.w*self.h == other.w*other.h

# Third-party class — no modification needed
class ExternalShape:
    """Imagine this comes from a library we can't change."""
    def draw(self) -> str: return "★ external shape"

def render_all(shapes: list[Drawable]) -> None:
    for shape in shapes:
        print(f"  {shape.draw()}")

def serialize_all(items: list[Serializable]) -> list[str]:
    return [item.to_json() for item in items]

print("=== Protocol: Drawable ===")
shapes = [Circle(5), Rectangle(3, 4), ExternalShape()]
render_all(shapes)                     # works — structural typing

print(f"\nCircle is Drawable:      {isinstance(Circle(1), Drawable)}")
print(f"ExternalShape is Drawable: {isinstance(ExternalShape(), Drawable)}")

print("\n=== Protocol: Serializable ===")
serializables = [Circle(3), Rectangle(2, 5)]
jsons = serialize_all(serializables)
for j in jsons:
    print(f"  {j}")

# ═══════════════════════════════════════════
# 2. Protocol with generic typing
# ═══════════════════════════════════════════
T = TypeVar("T")

class SupportsLenAndIter(Protocol[T]):
    def __len__(self) -> int: ...
    def __iter__(self): ...

def first_n(container: SupportsLenAndIter, n: int) -> list:
    return list(item for _, item in zip(range(n), container))

print("\n=== Generic Protocol ===")
print(first_n([1, 2, 3, 4, 5], 3))        # list
print(first_n(range(10), 5))              # range
print(first_n("hello world", 5))          # str

# ═══════════════════════════════════════════
# 3. Callback protocols
# ═══════════════════════════════════════════
class Transformer(Protocol):
    def __call__(self, value: int) -> int: ...

class Predicate(Protocol):
    def __call__(self, value: int) -> bool: ...

def apply_transform(data: list[int], transform: Transformer) -> list[int]:
    return [transform(x) for x in data]

def filter_items(data: list[int], pred: Predicate) -> list[int]:
    return [x for x in data if pred(x)]

print("\n=== Callback Protocols ===")
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
squared = apply_transform(data, lambda x: x ** 2)
print(f"Squared: {squared}")

evens = filter_items(data, lambda x: x % 2 == 0)
print(f"Evens: {evens}")

# ═══════════════════════════════════════════
# 4. Protocol inheritance
# ═══════════════════════════════════════════
@runtime_checkable
class Closeable(Protocol):
    def close(self) -> None: ...

@runtime_checkable
class Resource(Closeable, Protocol):
    def read(self) -> bytes: ...
    def write(self, data: bytes) -> int: ...

class FakeFile:
    def __init__(self, path):
        self.path = path
        self._data = b""
        self._closed = False

    def read(self) -> bytes: return self._data
    def write(self, data: bytes) -> int:
        self._data += data
        return len(data)
    def close(self) -> None: self._closed = True
    def __enter__(self): return self
    def __exit__(self, *_): self.close()

print("\n=== Protocol Inheritance ===")
f = FakeFile("/tmp/test.bin")
print(f"Is Closeable: {isinstance(f, Closeable)}")
print(f"Is Resource:  {isinstance(f, Resource)}")

f.write(b"Hello!")
print(f"Read back: {f.read()}")
f.close()
print(f"Closed: {f._closed}")

# ═══════════════════════════════════════════
# 5. Built-in protocol compatibility
# ═══════════════════════════════════════════
print("\n=== Built-in Protocols ===")

class Temperature:
    def __init__(self, celsius: float):
        self.celsius = celsius
    def __float__(self): return float(self.celsius)
    def __int__(self): return int(self.celsius)
    def __str__(self): return f"{self.celsius}°C"
    def __repr__(self): return f"Temperature({self.celsius})"

t = Temperature(36.6)
print(f"float(t): {float(t)}")
print(f"int(t):   {int(t)}")
print(f"str(t):   {t}")
print(f"isinstance(t, SupportsFloat): {isinstance(t, SupportsFloat)}")
print(f"isinstance(t, SupportsInt):   {isinstance(t, SupportsInt)}")

# Sort using Comparable protocol
shapes2 = [Circle(3), Circle(7), Circle(1), Circle(5)]
sorted_shapes = sorted(shapes2)
print(f"\nSorted circles: {[s.r for s in sorted_shapes]}")
