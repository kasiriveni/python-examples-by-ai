# OOP advanced: dunder methods, MRO, multiple inheritance
class A:
    def ping(self):
        return 'A'

class B(A):
    def ping(self):
        return 'B'

class C(A):
    pass

class D(B, C):
    pass

d = D()
print(d.ping())  # method resolution order

# dunder repr
class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f'Point({self.x},{self.y})'

print(Point(1,2))

# Inheritance and super()
class Animal:
    def __init__(self, name):
        self.name = name
    def speak(self):
        return '...'
class Dog(Animal):
    def speak(self):
        return 'Woof!'
class Cat(Animal):
    def speak(self):
        return 'Meow!'
dog = Dog('Buddy')
cat = Cat('Whiskers')

print(dog.name, dog.speak())
print(cat.name, cat.speak())

# - Polymorphism
