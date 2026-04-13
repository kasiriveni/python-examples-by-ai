"""
Advanced Python: Metaclasses in depth.
Covers class creation, __new__, class decorators, and metaclass use cases.
"""
from functools import wraps

# ═══════════════════════════════════════════
# 1. type() as a metaclass
# ═══════════════════════════════════════════
print("=== type() creates classes dynamically ===")

# Normal class creation:
# class Dog: ...
# Is equivalent to:
Dog = type("Dog", (object,), {
    "sound": "woof",
    "speak": lambda self: f"I say {self.sound}",
})

d = Dog()
print(f"Dog().speak() = {d.speak()}")

# Dynamic inheritance
Animal = type("Animal", (object,), {"alive": True})
Cat = type("Cat", (Animal,), {"sound": "meow"})
print(f"Cat is Animal: {issubclass(Cat, Animal)}")

# ═══════════════════════════════════════════
# 2. Custom metaclass
# ═══════════════════════════════════════════
class SingletonMeta(type):
    """Metaclass that ensures only one instance per class."""
    _instances: dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Config(metaclass=SingletonMeta):
    def __init__(self, env="dev"):
        self.env = env
        self.settings: dict = {}

    def set(self, key, value):
        self.settings[key] = value

    def get(self, key, default=None):
        return self.settings.get(key, default)

print("\n=== Singleton Metaclass ===")
c1 = Config("production")
c1.set("debug", False)
c2 = Config("staging")  # Returns same instance
print(f"c1 is c2: {c1 is c2}")
print(f"c2.env:   {c2.env}")       # "production" (same object)
print(f"c2.debug: {c2.get('debug')}")

# ═══════════════════════════════════════════
# 3. Auto-register subclasses
# ═══════════════════════════════════════════
class PluginMeta(type):
    """Registry metaclass: automatically register all subclasses."""
    _registry: dict[str, type] = {}

    def __init_subclass__(cls, plugin_name: str = "", **kwargs):
        super().__init_subclass__(**kwargs)
        if plugin_name:
            PluginMeta._registry[plugin_name] = cls

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        plugin_name = namespace.get("plugin_name", "")
        if plugin_name and bases:
            PluginMeta._registry[plugin_name] = cls
        return cls

class BasePlugin(metaclass=PluginMeta):
    plugin_name = ""
    def run(self): raise NotImplementedError

class CSVPlugin(BasePlugin):
    plugin_name = "csv"
    def run(self): return "Processing CSV"

class JSONPlugin(BasePlugin):
    plugin_name = "json"
    def run(self): return "Processing JSON"

class XMLPlugin(BasePlugin):
    plugin_name = "xml"
    def run(self): return "Processing XML"

print("\n=== Auto-register Plugins ===")
print(f"Registered: {list(PluginMeta._registry.keys())}")
for name, cls in PluginMeta._registry.items():
    print(f"  {name}: {cls().run()}")

# ═══════════════════════════════════════════
# 4. Attribute validation metaclass
# ═══════════════════════════════════════════
class ValidatedMeta(type):
    """Enforce type annotations at class definition time."""

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        annotations = namespace.get("__annotations__", {})
        defaults = {k: v for k, v in namespace.items() if not k.startswith("_")}

        for attr, expected_type in annotations.items():
            if attr in defaults:
                val = defaults[attr]
                if not isinstance(val, expected_type):
                    raise TypeError(
                        f"{name}.{attr} must be {expected_type.__name__}, "
                        f"got {type(val).__name__}"
                    )
        return cls

class TypedConfig(metaclass=ValidatedMeta):
    host: str = "localhost"
    port: int = 8080
    debug: bool = False
    max_conn: int = 100

print("\n=== Validated Metaclass ===")
print(f"TypedConfig created: host={TypedConfig.host}, port={TypedConfig.port}")

try:
    class BadConfig(metaclass=ValidatedMeta):
        port: int = "not_an_int"
except TypeError as e:
    print(f"Caught type error: {e}")

# ═══════════════════════════════════════════
# 5. Abstract method enforcement
# ═══════════════════════════════════════════
class InterfaceMeta(type):
    """Raise error at instantiation if abstract methods remain."""

    def __call__(cls, *args, **kwargs):
        abstracts = {
            name for name, val in vars(cls).items()
            if getattr(val, "__isabstract__", False)
        }
        for base in cls.__mro__[1:]:
            for name, val in vars(base).items():
                if getattr(val, "__isabstract__", False) and name not in vars(cls):
                    abstracts.add(name)

        if abstracts:
            raise TypeError(f"Cannot instantiate {cls.__name__}: "
                            f"abstract methods {abstracts}")
        return super().__call__(*args, **kwargs)

def abstract(func):
    func.__isabstract__ = True
    return func

class Shape(metaclass=InterfaceMeta):
    @abstract
    def area(self) -> float: ...
    @abstract
    def perimeter(self) -> float: ...

class Circle(Shape):
    def __init__(self, r): self.r = r
    def area(self): return 3.14159 * self.r**2
    def perimeter(self): return 2 * 3.14159 * self.r

print("\n=== Interface Metaclass ===")
c = Circle(5)
print(f"Circle area={c.area():.2f}, perimeter={c.perimeter():.2f}")

try:
    Shape()  # Should fail: abstract methods not implemented
except TypeError as e:
    print(f"Cannot instantiate Shape: {e}")

# ═══════════════════════════════════════════
# 6. __init_subclass__ (Python 3.6+ alternative to metaclasses)
# ═══════════════════════════════════════════
class OrderedSerializer:
    """
    Uses __init_subclass__ to track field order.
    Simpler than a metaclass for many use cases.
    """
    _field_order: list[str] = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._field_order = [
            k for k in vars(cls)
            if not k.startswith("_") and not callable(getattr(cls, k))
        ]

    def serialize(self) -> dict:
        return {k: getattr(self, k) for k in self._field_order}

class Event(OrderedSerializer):
    name: str = ""
    timestamp: str = ""
    severity: str = "info"
    message: str = ""

print("\n=== __init_subclass__ ===")
e = Event()
e.name = "login"
e.timestamp = "2024-01-01T00:00:00"
e.message = "User logged in"
print(f"Field order: {Event._field_order}")
print(f"Serialized:  {e.serialize()}")
