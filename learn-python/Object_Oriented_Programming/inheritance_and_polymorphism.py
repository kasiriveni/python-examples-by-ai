"""
Inheritance and polymorphism in Python.
"""
from abc import ABC, abstractmethod

# Abstract base class
class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def perimeter(self):
        pass

    def describe(self):
        return f"{self.__class__.__name__}: area={self.area():.2f}, perimeter={self.perimeter():.2f}"

# Single inheritance
class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        import math
        return math.pi * self.radius ** 2

    def perimeter(self):
        import math
        return 2 * math.pi * self.radius

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

# Multi-level inheritance
class Square(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)

# Multiple inheritance
class Drawable:
    def draw(self):
        return f"Drawing {self.__class__.__name__}"

class Resizable:
    def resize(self, factor):
        return f"Resizing {self.__class__.__name__} by {factor}x"

class UICircle(Circle, Drawable, Resizable):
    pass

# Polymorphism
def print_shape_info(shape: Shape):
    print(f"  {shape.describe()}")

if __name__ == "__main__":
    shapes = [Circle(5), Rectangle(4, 6), Square(3)]

    print("Shapes:")
    for shape in shapes:
        print_shape_info(shape)

    # isinstance and issubclass
    c = Circle(10)
    print(f"\nCircle is Shape: {isinstance(c, Shape)}")
    print(f"Square is Rectangle: {issubclass(Square, Rectangle)}")

    # Multiple inheritance
    ui_circle = UICircle(7)
    print(f"\n{ui_circle.draw()}")
    print(f"{ui_circle.resize(2)}")
    print(f"Area: {ui_circle.area():.2f}")

    # MRO (Method Resolution Order)
    print(f"\nMRO: {[c.__name__ for c in UICircle.__mro__]}")
