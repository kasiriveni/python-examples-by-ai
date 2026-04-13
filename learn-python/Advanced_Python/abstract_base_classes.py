"""
Advanced Python: Abstract Base Classes (ABCs) and class hierarchies.
"""
from abc import ABC, abstractmethod, abstractproperty
from typing import Protocol, runtime_checkable
import math

# ═══════════════════════════════════════════
# 1. Basic ABC usage
# ═══════════════════════════════════════════
class Shape(ABC):
    """Abstract base for all 2D shapes."""

    @abstractmethod
    def area(self) -> float:
        """Return the area."""
        ...

    @abstractmethod
    def perimeter(self) -> float:
        """Return the perimeter."""
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the shape name."""
        ...

    def describe(self) -> str:
        return (f"{self.name}: area={self.area():.4f}, "
                f"perimeter={self.perimeter():.4f}")

class Circle(Shape):
    def __init__(self, r: float): self.r = r
    def area(self):      return math.pi * self.r**2
    def perimeter(self): return 2 * math.pi * self.r
    @property
    def name(self): return "Circle"

class Rectangle(Shape):
    def __init__(self, w, h): self.w = w; self.h = h
    def area(self):      return self.w * self.h
    def perimeter(self): return 2 * (self.w + self.h)
    @property
    def name(self): return "Rectangle"

class Triangle(Shape):
    def __init__(self, a, b, c):
        self.a = a; self.b = b; self.c = c
    def area(self):
        s = (self.a + self.b + self.c) / 2
        return math.sqrt(s * (s-self.a) * (s-self.b) * (s-self.c))
    def perimeter(self): return self.a + self.b + self.c
    @property
    def name(self): return "Triangle"

# ═══════════════════════════════════════════
# 2. ABCs from collections.abc
# ═══════════════════════════════════════════
from collections.abc import MutableSequence, MutableMapping, Iterable

class Stack(MutableSequence):
    """Stack built on MutableSequence abstract base."""

    def __init__(self):
        self._data: list = []

    # Required by MutableSequence
    def __getitem__(self, index):  return self._data[index]
    def __setitem__(self, index, value): self._data[index] = value
    def __delitem__(self, index):  del self._data[index]
    def __len__(self):             return len(self._data)

    def insert(self, index, value): self._data.insert(index, value)

    # Stack-specific methods
    def push(self, item):          self._data.append(item)
    def pop(self, index=-1):       return self._data.pop(index)
    def peek(self):                return self._data[-1] if self._data else None
    def __repr__(self):            return f"Stack({self._data})"

class BiMap(MutableMapping):
    """Bidirectional mapping (both key→value and value→key)."""

    def __init__(self):
        self._fwd: dict = {}
        self._rev: dict = {}

    def __setitem__(self, key, value):
        if value in self._rev:
            old_key = self._rev[value]
            if old_key != key:
                del self._fwd[old_key]
        if key in self._fwd:
            old_val = self._fwd[key]
            if old_val != value:
                del self._rev[old_val]
        self._fwd[key] = value
        self._rev[value] = key

    def __getitem__(self, key):  return self._fwd[key]
    def __delitem__(self, key):
        val = self._fwd.pop(key)
        del self._rev[val]
    def __iter__(self):          return iter(self._fwd)
    def __len__(self):           return len(self._fwd)

    def inverse(self, value):   return self._rev[value]
    def __repr__(self):         return f"BiMap({self._fwd})"

# ═══════════════════════════════════════════
# 3. Virtual subclasses (register)
# ═══════════════════════════════════════════
class Printable(ABC):
    """ABC for printable objects. Supports virtual subclasses."""

    @abstractmethod
    def to_string(self) -> str: ...

    def print_self(self): print(f"  → {self.to_string()}")

class LegacyLogger:
    """Pre-existing class — we can't modify it."""
    def to_string(self): return "LegacyLogger output"

# Register LegacyLogger as a virtual subclass of Printable
Printable.register(LegacyLogger)

# ═══════════════════════════════════════════
# 4. Mixin pattern with ABCs
# ═══════════════════════════════════════════
class JSONSerializableMixin(ABC):
    """Mixin that adds JSON serialization if to_dict is provided."""

    @abstractmethod
    def to_dict(self) -> dict: ...

    def to_json(self) -> str:
        import json
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str):
        import json
        return cls(**json.loads(json_str))

class LoggableMixin:
    """Mixin adding logging to any class."""
    def log(self, message: str, level: str = "INFO") -> None:
        print(f"  [{level}] {type(self).__name__}: {message}")

class DataModel(JSONSerializableMixin, LoggableMixin):
    def __init__(self, name: str, value: float):
        self.name = name
        self.value = value

    def to_dict(self) -> dict:
        return {"name": self.name, "value": self.value}

    @classmethod
    def from_json(cls, json_str: str):
        import json
        return cls(**json.loads(json_str))

# ═══════════════════════════════════════════
# 5. ABC hooks and __subclasshook__
# ═══════════════════════════════════════════
class Drawable(ABC):
    """ABC with customized subclass detection via __subclasshook__."""

    @classmethod
    def __subclasshook__(cls, subclass):
        # Any class with a .draw() method qualifies
        if cls is Drawable:
            return hasattr(subclass, 'draw') and callable(subclass.draw)
        return NotImplemented

class Sprite:
    def draw(self): return "Sprite drawn"

class Button:
    def render(self): return "Button rendered"  # no draw()

if __name__ == "__main__":
    print("=== Shapes ===")
    for shape in [Circle(5), Rectangle(4, 6), Triangle(3, 4, 5)]:
        print(f"  {shape.describe()}")

    # Can't instantiate ABC directly
    try:
        s = Shape()
    except TypeError as e:
        print(f"  Cannot instantiate ABC: {e}")

    print("\n=== MutableSequence Stack ===")
    s = Stack()
    for v in [10, 20, 30, 40]:
        s.push(v)
    print(f"  {s}")
    print(f"  Peek: {s.peek()}")
    s.pop()
    print(f"  After pop: {s}")
    print(f"  Is Iterable: {isinstance(s, Iterable)}")

    print("\n=== BiMap ===")
    bm = BiMap()
    bm["alice"] = "alice@example.com"
    bm["bob"]   = "bob@example.com"
    print(f"  alice → {bm['alice']}")
    print(f"  alice@example.com → {bm.inverse('alice@example.com')}")
    # Remapping
    bm["alice"] = "newalice@example.com"
    print(f"  After remap: {bm}")

    print("\n=== Virtual Subclass ===")
    ll = LegacyLogger()
    print(f"  isinstance(LegacyLogger(), Printable): {isinstance(ll, Printable)}")
    ll.to_string()

    print("\n=== Mixin ===")
    dm = DataModel("temperature", 36.6)
    json_str = dm.to_json()
    print(f"  JSON: {json_str}")
    dm2 = DataModel.from_json(json_str)
    print(f"  Parsed back: {dm2.to_dict()}")
    dm.log("Serialized successfully")

    print("\n=== __subclasshook__ ===")
    print(f"  Sprite is Drawable:  {issubclass(Sprite, Drawable)}")
    print(f"  Button is Drawable:  {issubclass(Button, Drawable)}")
    sp = Sprite()
    print(f"  isinstance check:    {isinstance(sp, Drawable)}")
