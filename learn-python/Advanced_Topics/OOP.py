# OOP: Classes, Objects, Inheritance, Dunder/Magic Methods

# Class and Object
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} makes a sound."

# Inheritance
class Dog(Animal):
    def speak(self):
        return f"{self.name} barks."

# Dunder/Magic Methods
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

# Usage
animal = Animal("Generic Animal")
dog = Dog("Buddy")
print(animal.speak())
print(dog.speak())

v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(v1 + v2)
