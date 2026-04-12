from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def __repr__(self):
        return f'Rectangle({self.width}, {self.height})'

    def total_sides(self):
        return 4

    # private method
    def __private_method(self):
        return "This is a private method"


r = Rectangle(5, 10)
print("Area:", r.area())
print("Total sides:", r.total_sides())
print(r)

# ❌ Not recommended (will fail)
# print(r.__private_method())


print("\n--- Serialization Examples ---\n")


print(r.__repr__())
