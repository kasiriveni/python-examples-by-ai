"""
Abstract Base Classes (ABC) in Python.
"""
from abc import ABC, abstractmethod
from collections.abc import Sequence, Mapping, Iterable
import math

# === Defining abstract base class ===
class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        """Calculate the area of the shape."""
        pass

    @abstractmethod
    def perimeter(self) -> float:
        """Calculate the perimeter of the shape."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the shape."""
        pass

    # Concrete method (shared implementation)
    def describe(self) -> str:
        return f"{self.name}: area={self.area():.2f}, perimeter={self.perimeter():.2f}"

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    @property
    def name(self):
        return "Circle"

    def area(self):
        return math.pi * self.radius ** 2

    def perimeter(self):
        return 2 * math.pi * self.radius

class Triangle(Shape):
    def __init__(self, a, b, c):
        self.a, self.b, self.c = a, b, c

    @property
    def name(self):
        return "Triangle"

    def area(self):
        s = (self.a + self.b + self.c) / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

    def perimeter(self):
        return self.a + self.b + self.c

# === Custom collection using ABCs ===
class SortedList(Sequence):
    def __init__(self, items=None):
        self._data = sorted(items) if items else []

    def __getitem__(self, index):
        return self._data[index]

    def __len__(self):
        return len(self._data)

    def add(self, item):
        import bisect
        bisect.insort(self._data, item)

    def __repr__(self):
        return f"SortedList({self._data})"

# === Registering virtual subclasses ===
class Printable(ABC):
    @abstractmethod
    def to_string(self) -> str:
        pass

@Printable.register
class Document:
    def to_string(self):
        return "Document content"

if __name__ == "__main__":
    # Cannot instantiate abstract class
    try:
        s = Shape()
    except TypeError as e:
        print(f"Cannot instantiate ABC: {e}")

    # Concrete implementations
    shapes = [Circle(5), Triangle(3, 4, 5)]
    for shape in shapes:
        print(shape.describe())

    # Custom collection
    print(f"\n--- SortedList ---")
    sl = SortedList([5, 2, 8, 1, 4])
    print(f"SortedList: {sl}")
    sl.add(3)
    print(f"After add(3): {sl}")
    print(f"sl[2] = {sl[2]}")
    print(f"len = {len(sl)}")
    print(f"Is Sequence: {isinstance(sl, Sequence)}")

    # Virtual subclass
    doc = Document()
    print(f"\nIs Printable: {isinstance(doc, Printable)}")

    # Check built-in ABC
    print(f"\nlist is Sequence: {isinstance([], Sequence)}")
    print(f"dict is Mapping: {isinstance({}, Mapping)}")
    print(f"str is Iterable: {isinstance('', Iterable)}")
