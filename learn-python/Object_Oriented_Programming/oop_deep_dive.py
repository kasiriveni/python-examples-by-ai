"""
OOP: Inheritance, MRO, mixins, composition, dunder methods, and data classes.
"""
from __future__ import annotations
import math
import copy
from functools import total_ordering
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Iterator

# ═══════════════════════════════════════════
# 1. Single and multi-level inheritance
# ═══════════════════════════════════════════
class Animal:
    def __init__(self, name: str, weight_kg: float):
        self.name = name
        self.weight_kg = weight_kg

    def speak(self) -> str:
        return "..."

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.name!r})"

class Mammal(Animal):
    def __init__(self, name: str, weight_kg: float, fur_color: str):
        super().__init__(name, weight_kg)
        self.fur_color = fur_color

    def nurse_young(self) -> str:
        return f"{self.name} nurses its young"

class Dog(Mammal):
    def speak(self) -> str: return f"{self.name} says: Woof!"
    def fetch(self) -> str: return f"{self.name} fetches the ball"

class Cat(Mammal):
    def speak(self) -> str: return f"{self.name} says: Meow!"
    def purr(self) -> str: return "Purrr..."

# ═══════════════════════════════════════════
# 2. Multiple inheritance & MRO
# ═══════════════════════════════════════════
class Flyable:
    def fly(self) -> str: return f"{self.name} is flying"   # type: ignore
    def move(self) -> str: return "flying"

class Swimmable:
    def swim(self) -> str: return f"{self.name} is swimming"  # type: ignore
    def move(self) -> str: return "swimming"

class Duck(Mammal, Flyable, Swimmable):
    def speak(self) -> str: return f"{self.name} says: Quack!"
    # MRO: Duck → Mammal → Animal → Flyable → Swimmable
    # move() resolves to Flyable.move because it comes first in MRO

# ═══════════════════════════════════════════
# 3. Mixins (thin behaviour units)
# ═══════════════════════════════════════════
class SerializableMixin:
    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

    @classmethod
    def from_dict(cls, data: dict):
        obj = cls.__new__(cls)
        obj.__dict__.update(data)
        return obj

class LoggableMixin:
    _event_log: list[str]   # expected attribute

    def log_event(self, event: str) -> None:
        if not hasattr(self, "_event_log"):
            self._event_log = []
        self._event_log.append(event)

    def get_log(self) -> list[str]:
        return list(getattr(self, "_event_log", []))

class ComparableMixin:
    """Requires _key() method from subclass; provides full comparison operators."""
    def _key(self): raise NotImplementedError
    def __eq__(self, other): return self._key() == other._key()
    def __lt__(self, other): return self._key() <  other._key()
    def __le__(self, other): return self._key() <= other._key()
    def __gt__(self, other): return self._key() >  other._key()
    def __ge__(self, other): return self._key() >= other._key()
    def __hash__(self): return hash(self._key())

class Employee(SerializableMixin, LoggableMixin, ComparableMixin):
    def __init__(self, name: str, salary: float):
        self.name = name; self.salary = salary
    def _key(self): return (self.salary, self.name)
    def give_raise(self, amount: float):
        self.salary += amount
        self.log_event(f"raise +{amount}")
    def __repr__(self): return f"Employee({self.name!r}, ${self.salary:,.0f})"

# ═══════════════════════════════════════════
# 4. Abstract base classes
# ═══════════════════════════════════════════
class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...
    @abstractmethod
    def perimeter(self) -> float: ...

    def describe(self) -> str:
        return (f"{type(self).__name__}: "
                f"area={self.area():.2f}, perimeter={self.perimeter():.2f}")

@dataclass
class Circle(Shape):
    radius: float
    def area(self) -> float: return math.pi * self.radius ** 2
    def perimeter(self) -> float: return 2 * math.pi * self.radius

@dataclass
class Rectangle(Shape):
    width: float; height: float
    def area(self) -> float: return self.width * self.height
    def perimeter(self) -> float: return 2 * (self.width + self.height)

@dataclass
class Triangle(Shape):
    a: float; b: float; c: float
    def perimeter(self) -> float: return self.a + self.b + self.c
    def area(self) -> float:
        s = self.perimeter() / 2
        return math.sqrt(s * (s-self.a) * (s-self.b) * (s-self.c))

# ═══════════════════════════════════════════
# 5. Dunder methods
# ═══════════════════════════════════════════
@total_ordering
class Money:
    def __init__(self, amount: float, currency: str = "USD"):
        self._amount = round(amount, 2)
        self.currency = currency

    def _check_currency(self, other: "Money"):
        if self.currency != other.currency:
            raise ValueError(f"Cannot mix {self.currency} and {other.currency}")

    def __add__(self, other: "Money") -> "Money":
        self._check_currency(other)
        return Money(self._amount + other._amount, self.currency)

    def __sub__(self, other: "Money") -> "Money":
        self._check_currency(other)
        return Money(self._amount - other._amount, self.currency)

    def __mul__(self, factor: float) -> "Money":
        return Money(self._amount * factor, self.currency)

    def __truediv__(self, divisor: float) -> "Money":
        return Money(self._amount / divisor, self.currency)

    def __neg__(self) -> "Money":
        return Money(-self._amount, self.currency)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money): return NotImplemented
        return self._amount == other._amount and self.currency == other.currency

    def __lt__(self, other: "Money") -> bool:
        self._check_currency(other)
        return self._amount < other._amount

    def __repr__(self) -> str:
        return f"Money({self._amount:.2f}, {self.currency!r})"

    def __str__(self) -> str:
        symbols = {"USD": "$", "EUR": "€", "GBP": "£"}
        sym = symbols.get(self.currency, self.currency + " ")
        return f"{sym}{self._amount:,.2f}"

    def __bool__(self) -> bool: return self._amount != 0.0

    def __abs__(self) -> "Money": return Money(abs(self._amount), self.currency)

# ═══════════════════════════════════════════
# 6. Composition (has-a relationship)
# ═══════════════════════════════════════════
@dataclass
class Address:
    street: str; city: str; country: str
    def __str__(self): return f"{self.street}, {self.city}, {self.country}"

@dataclass
class ContactInfo:
    email: str; phone: str = ""
    def __str__(self): return self.email

class Person:
    def __init__(self, first: str, last: str, address: Address, contact: ContactInfo):
        self.first = first; self.last = last
        self.address = address          # composition
        self.contact = contact          # composition

    @property
    def full_name(self) -> str: return f"{self.first} {self.last}"

    def __repr__(self):
        return f"Person({self.full_name!r}, {self.address.city!r})"

# ═══════════════════════════════════════════
# 7. __slots__ for memory efficiency
# ═══════════════════════════════════════════
class Point2D:
    __slots__ = ("x", "y")
    def __init__(self, x: float, y: float):
        self.x = x; self.y = y
    def distance_to(self, other: "Point2D") -> float:
        return math.hypot(self.x - other.x, self.y - other.y)
    def __repr__(self): return f"Point2D({self.x}, {self.y})"
    def __iter__(self): yield self.x; yield self.y

# ═══════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════
if __name__ == "__main__":
    print("=== Inheritance ===")
    pets: list[Animal] = [
        Dog("Rex", 30, "golden"),
        Cat("Whiskers", 4, "orange"),
        Duck("Donald", 2, "white"),
    ]
    for pet in pets:
        print(f"  {pet}: {pet.speak()}")
    duck = pets[2]
    assert isinstance(duck, Duck)
    print(f"  Duck.move() = {duck.move()!r}  (MRO: Flyable wins)")
    print(f"  Duck MRO: {[cls.__name__ for cls in Duck.__mro__]}")

    print("\n=== Mixins ===")
    alice = Employee("Alice", 80_000)
    bob   = Employee("Bob",   95_000)
    alice.give_raise(5_000)
    print(f"  {alice}, log: {alice.get_log()}")
    print(f"  alice < bob: {alice < bob}")
    print(f"  alice dict: {alice.to_dict()}")
    alice2 = Employee.from_dict(alice.to_dict())
    print(f"  reconstructed: {alice2}")

    print("\n=== Shapes ===")
    shapes: list[Shape] = [Circle(5), Rectangle(4, 6), Triangle(3, 4, 5)]
    for s in shapes:
        print(f"  {s.describe()}")

    print("\n=== Money dunder methods ===")
    price  = Money(19.99)
    tax    = Money(1.60)
    total  = price + tax
    half   = total / 2
    print(f"  {price} + {tax} = {total}")
    print(f"  Half = {half}")
    print(f"  Sorted: {sorted([Money(10), Money(5), Money(15)])}")
    print(f"  bool(Money(0)) = {bool(Money(0))}")

    print("\n=== Composition ===")
    addr = Address("123 Main St", "Springfield", "US")
    contact = ContactInfo("alice@example.com", "+1-555-0100")
    person = Person("Alice", "Smith", addr, contact)
    print(f"  {person!r}")
    print(f"  Address: {person.address}")

    print("\n=== __slots__ ===")
    p1, p2 = Point2D(0, 0), Point2D(3, 4)
    print(f"  Distance: {p1.distance_to(p2)}")
    print(f"  Unpack: {list(p2)}")
    try:
        p1.z = 5    # type: ignore
    except AttributeError as e:
        print(f"  __slots__ prevents: {e}")
