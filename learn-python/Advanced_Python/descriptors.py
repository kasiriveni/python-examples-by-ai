"""
Advanced Python: Descriptors in depth.
Descriptors control attribute access; used to build properties, validators, ORMs.
"""
from typing import Any, TypeVar, Generic, overload

# ═══════════════════════════════════════════
# 1. Descriptor protocol basics
# ═══════════════════════════════════════════
print("=== Data vs Non-Data Descriptors ===")

class DataDescriptor:
    """Has both __get__ and __set__ — takes priority over instance __dict__."""

    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self  # accessed from class
        return getattr(obj, self.private_name, None)

    def __set__(self, obj, value):
        setattr(obj, self.private_name, value)

    def __delete__(self, obj):
        try:
            delattr(obj, self.private_name)
        except AttributeError:
            pass

class NonDataDescriptor:
    """Has only __get__ — instance __dict__ takes priority."""

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        print(f"  NonDataDescriptor.__get__ called for {self.name}")
        return 42  # instance can override this

class Demo:
    x = DataDescriptor()
    y = NonDataDescriptor()

d = Demo()
d.x = 10
print(f"d.x = {d.x}")  # uses DataDescriptor.__get__
d.y = 99               # goes into instance dict, bypasses non-data descriptor
print(f"d.y = {d.y}")  # returns 99 (instance dict wins)

# ═══════════════════════════════════════════
# 2. Typed / validated descriptors
# ═══════════════════════════════════════════
print("\n=== Typed Descriptor ===")

T = TypeVar("T")

class Typed(Generic[T]):
    def __set_name__(self, owner, name):
        self.name = name
        self._attr = f"_typed_{name}"

    def __init__(self, type_: type[T], default=None):
        self.type_ = type_
        self.default = default

    def __get__(self, obj, objtype=None):
        if obj is None: return self
        return getattr(obj, self._attr, self.default)

    def __set__(self, obj, value):
        if not isinstance(value, self.type_):
            raise TypeError(f"{self.name}: expected {self.type_.__name__}, got {type(value).__name__}")
        setattr(obj, self._attr, value)

class Bounded:
    """Numeric descriptor with min/max validation."""
    def __set_name__(self, owner, name):
        self.name = name
        self._attr = f"_bounded_{name}"

    def __init__(self, lo=None, hi=None, default=0):
        self.lo, self.hi, self.default = lo, hi, default

    def __get__(self, obj, _=None):
        if obj is None: return self
        return getattr(obj, self._attr, self.default)

    def __set__(self, obj, value):
        if self.lo is not None and value < self.lo:
            raise ValueError(f"{self.name}: {value} < minimum {self.lo}")
        if self.hi is not None and value > self.hi:
            raise ValueError(f"{self.name}: {value} > maximum {self.hi}")
        setattr(obj, self._attr, value)

class Player:
    name    = Typed(str, default="Unknown")
    age     = Typed(int, default=0)
    health  = Bounded(lo=0, hi=100, default=100)
    speed   = Bounded(lo=0.0, hi=10.0, default=5.0)

p = Player()
p.name = "Alice"
p.age  = 25
p.health = 75
print(f"Player: name={p.name}, age={p.age}, health={p.health}")

try:
    p.health = 150
except ValueError as e:
    print(f"Caught: {e}")

try:
    p.name = 123
except TypeError as e:
    print(f"Caught: {e}")

# ═══════════════════════════════════════════
# 3. Cached property (like functools.cached_property)
# ═══════════════════════════════════════════
print("\n=== Cached Property Descriptor ===")

class cached_property:
    """Computes once, caches on instance."""

    def __init__(self, func):
        self.func = func
        self.__doc__ = func.__doc__
        self.attrname = None

    def __set_name__(self, owner, name):
        self.attrname = name

    def __get__(self, obj, cls=None):
        if obj is None:
            return self
        name = self.attrname or self.func.__name__
        if name not in obj.__dict__:
            obj.__dict__[name] = self.func(obj)
        return obj.__dict__[name]

class Circle:
    def __init__(self, r): self.r = r

    @cached_property
    def area(self):
        print("  (computing area...)")
        return 3.14159 * self.r**2

    @cached_property
    def circumference(self):
        print("  (computing circumference...)")
        return 2 * 3.14159 * self.r

c = Circle(5)
print(f"area: {c.area:.2f}")       # computed
print(f"area: {c.area:.2f}")       # cached
print(f"circumference: {c.circumference:.2f}")

# ═══════════════════════════════════════════
# 4. ORM-like field descriptors
# ═══════════════════════════════════════════
print("\n=== ORM-style Field Descriptors ===")

class Field:
    def __init__(self, type_, required=True, default=None):
        self.type_ = type_
        self.required = required
        self.default = default
        self.name = ""

    def __set_name__(self, owner, name):
        self.name = name
        if not hasattr(owner, "_fields"):
            owner._fields = {}
        owner._fields[name] = self

    def __get__(self, obj, cls=None):
        if obj is None: return self
        return obj.__dict__.get(self.name, self.default)

    def __set__(self, obj, value):
        if value is None and self.required:
            raise ValueError(f"'{self.name}' is required")
        if value is not None and not isinstance(value, self.type_):
            try:
                value = self.type_(value)
            except (ValueError, TypeError):
                raise TypeError(f"'{self.name}' must be {self.type_.__name__}")
        obj.__dict__[self.name] = value

class ModelBase:
    def __init__(self, **kwargs):
        for name, field in self.__class__.__dict__.items():
            if isinstance(field, Field):
                setattr(self, name, kwargs.get(name, field.default))

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items()
                if not k.startswith("_")}

    def __repr__(self):
        fields = ", ".join(f"{k}={v!r}" for k, v in self.to_dict().items())
        return f"{type(self).__name__}({fields})"

class User(ModelBase):
    name  = Field(str)
    email = Field(str)
    age   = Field(int, required=False, default=0)
    score = Field(float, required=False, default=0.0)

u = User(name="Alice", email="alice@test.com", age="30")  # age coerced
print(f"User: {u}")
print(f"Fields defined: {list(User._fields.keys())}")

try:
    User(name="Bob")  # missing required email
except ValueError as e:
    print(f"Caught: {e}")
