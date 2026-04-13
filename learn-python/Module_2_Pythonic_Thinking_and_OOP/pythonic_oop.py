"""
Module 2: Pythonic Thinking and OOP - writing idiomatic Python.
"""
from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable
from abc import abstractmethod

# === Pythonic patterns ===
print("=== Pythonic vs Non-Pythonic ===")

# Non-pythonic: manual index
names = ["Alice", "Bob", "Charlie"]
# for i in range(len(names)):  # BAD
#     print(f"{i}: {names[i]}")

# Pythonic: enumerate
for i, name in enumerate(names, 1):
    print(f"  {i}. {name}")

# Non-pythonic: checking for None
# if x != None:  # BAD
# Pythonic:
x = "hello"
if x is not None:
    print(f"  x = {x}")

# EAFP vs LBYL
data = {"key": "value"}

# LBYL (Look Before You Leap)
if "key" in data:
    val = data["key"]

# EAFP (Easier to Ask Forgiveness) - Pythonic
try:
    val = data["key"]
except KeyError:
    val = "default"

# === Protocols (Structural Typing) ===
print("\n=== Protocols ===")

@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> str: ...

class Circle:
    def __init__(self, radius):
        self.radius = radius
    def draw(self) -> str:
        return f"Drawing circle r={self.radius}"

class Square:
    def __init__(self, side):
        self.side = side
    def draw(self) -> str:
        return f"Drawing square s={self.side}"

shapes = [Circle(5), Square(3)]
for shape in shapes:
    print(f"  {shape.draw()} (is Drawable: {isinstance(shape, Drawable)})")

# === Data classes ===
print("\n=== Dataclasses ===")

@dataclass(frozen=True)
class Point:
    x: float
    y: float

    def distance_to(self, other: 'Point') -> float:
        return ((self.x - other.x)**2 + (self.y - other.y)**2) ** 0.5

@dataclass
class Player:
    name: str
    health: int = 100
    inventory: list = field(default_factory=list)
    _score: int = field(default=0, repr=False)

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)

    def add_item(self, item):
        self.inventory.append(item)

    @property
    def is_alive(self):
        return self.health > 0

p1, p2 = Point(0, 0), Point(3, 4)
print(f"  Distance: {p1.distance_to(p2)}")

player = Player("Hero")
player.take_damage(30)
player.add_item("sword")
print(f"  {player}")

# === Descriptive magic methods ===
print("\n=== Magic Methods ===")

class Money:
    def __init__(self, amount, currency="USD"):
        self.amount = amount
        self.currency = currency

    def __add__(self, other):
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other):
        if self.currency != other.currency:
            raise ValueError("Cannot subtract different currencies")
        return Money(self.amount - other.amount, self.currency)

    def __mul__(self, factor):
        return Money(self.amount * factor, self.currency)

    def __lt__(self, other):
        return self.amount < other.amount

    def __eq__(self, other):
        return self.amount == other.amount and self.currency == other.currency

    def __repr__(self):
        return f"Money({self.amount}, '{self.currency}')"

    def __str__(self):
        return f"${self.amount:,.2f} {self.currency}"

a = Money(100)
b = Money(50)
print(f"  {a} + {b} = {a + b}")
print(f"  {a} * 3 = {a * 3}")
print(f"  {a} > {b}: {a > b}")

# === Context managers (class-based) ===
print("\n=== Context Manager ===")

class Timer:
    import time

    def __enter__(self):
        self.start = self.time.perf_counter()
        return self

    def __exit__(self, *args):
        self.elapsed = self.time.perf_counter() - self.start
        print(f"  Elapsed: {self.elapsed:.4f}s")

with Timer():
    total = sum(range(1_000_000))
