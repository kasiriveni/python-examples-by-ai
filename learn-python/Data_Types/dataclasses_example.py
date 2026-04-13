"""
Dataclasses in Python (3.7+).
"""
from dataclasses import dataclass, field, asdict, astuple, replace
from typing import ClassVar

@dataclass
class Point:
    x: float
    y: float

    def distance_to(self, other: 'Point') -> float:
        return ((self.x - other.x)**2 + (self.y - other.y)**2) ** 0.5

p1 = Point(3, 4)
p2 = Point(0, 0)
print(f"p1 = {p1}")
print(f"Distance: {p1.distance_to(p2):.2f}")

# Default values and field()
@dataclass
class Student:
    name: str
    age: int
    grades: list = field(default_factory=list)
    school: str = "MIT"
    _id: int = field(init=False, repr=False)
    student_count: ClassVar[int] = 0

    def __post_init__(self):
        Student.student_count += 1
        self._id = Student.student_count

s1 = Student("Alice", 20, [90, 85, 92])
s2 = Student("Bob", 22)
print(f"s1 = {s1}")
print(f"s2 = {s2}")
print(f"Count: {Student.student_count}")

# Conversion utilities
print(f"As dict: {asdict(s1)}")
print(f"As tuple: {astuple(p1)}")

# Replace (returns new instance)
p3 = replace(p1, x=10)
print(f"Replaced: {p3}")

# Frozen dataclass (immutable)
@dataclass(frozen=True)
class Color:
    r: int
    g: int
    b: int

red = Color(255, 0, 0)
print(f"Red: {red}")
print(f"Hash: {hash(red)}")

# Ordered dataclass
@dataclass(order=True)
class Version:
    major: int
    minor: int
    patch: int

versions = [Version(2, 0, 1), Version(1, 5, 0), Version(2, 0, 0)]
print(f"Sorted: {sorted(versions)}")

# Slots for memory efficiency (Python 3.10+)
@dataclass(slots=True)
class Lightweight:
    x: int
    y: int

lw = Lightweight(1, 2)
print(f"Lightweight: {lw}")
