# Data Types Deep Dive: type hints, dataclass, Enum, mutable vs immutable
from dataclasses import dataclass
from enum import Enum

# Type hints
def greet(name: str) -> str:
    return f"Hello, {name}"

# Dataclass
@dataclass
class Point:
    x: float
    y: float

# Enum
class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

p = Point(1.0, 2.0)
print(greet("Alice"), p, Color.RED)

# Mutable vs Immutable
lst = [1, 2, 3]  # mutable
t = (1, 2, 3)    # immutable
print("Before", lst)
lst.append(4)
print("After", lst)
