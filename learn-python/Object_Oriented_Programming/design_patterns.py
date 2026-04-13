"""
Design patterns in OOP Python.
"""
from abc import ABC, abstractmethod

# === Singleton Pattern ===
class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

s1 = Singleton()
s2 = Singleton()
print(f"Singleton: s1 is s2 = {s1 is s2}")

# === Factory Pattern ===
class Animal(ABC):
    @abstractmethod
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"

class AnimalFactory:
    _animals = {"dog": Dog, "cat": Cat}

    @classmethod
    def create(cls, animal_type):
        animal_class = cls._animals.get(animal_type.lower())
        if not animal_class:
            raise ValueError(f"Unknown animal: {animal_type}")
        return animal_class()

dog = AnimalFactory.create("dog")
cat = AnimalFactory.create("cat")
print(f"\nFactory: {dog.speak()}, {cat.speak()}")

# === Observer Pattern ===
class EventEmitter:
    def __init__(self):
        self._listeners = {}

    def on(self, event, callback):
        self._listeners.setdefault(event, []).append(callback)

    def emit(self, event, *args, **kwargs):
        for callback in self._listeners.get(event, []):
            callback(*args, **kwargs)

emitter = EventEmitter()
emitter.on("data", lambda d: print(f"  Received: {d}"))
emitter.on("data", lambda d: print(f"  Logging: {d}"))
print("\nObserver:")
emitter.emit("data", "hello world")

# === Strategy Pattern ===
class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data):
        pass

class BubbleSort(SortStrategy):
    def sort(self, data):
        arr = data.copy()
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr

class BuiltinSort(SortStrategy):
    def sort(self, data):
        return sorted(data)

class Sorter:
    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy

    def sort(self, data):
        return self._strategy.sort(data)

data = [5, 2, 8, 1, 9]
print(f"\nStrategy (bubble): {Sorter(BubbleSort()).sort(data)}")
print(f"Strategy (builtin): {Sorter(BuiltinSort()).sort(data)}")

# === Decorator Pattern ===
class Coffee:
    def cost(self):
        return 5.0
    def description(self):
        return "Coffee"

class MilkDecorator:
    def __init__(self, coffee):
        self._coffee = coffee
    def cost(self):
        return self._coffee.cost() + 1.5
    def description(self):
        return self._coffee.description() + " + Milk"

class SugarDecorator:
    def __init__(self, coffee):
        self._coffee = coffee
    def cost(self):
        return self._coffee.cost() + 0.5
    def description(self):
        return self._coffee.description() + " + Sugar"

order = SugarDecorator(MilkDecorator(Coffee()))
print(f"\nDecorator: {order.description()} = ${order.cost():.2f}")
