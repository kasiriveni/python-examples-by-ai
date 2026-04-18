# Core Python Concepts

## Core Themes
- Class design and object construction.
- Inheritance, polymorphism, and encapsulation.
- Magic methods, mixins, and common design patterns.

## Core Theme Examples
- Example 1: Class definition with __init__ and instance method.
- Example 2: Base class with inherited subclass overriding speak() method.
- Example 3: Singleton pattern or magic methods like __add__ and __repr__.

## Files and Concepts
- advanced_oop.py: metaclasses, slots, memory layout, class creation control
- classes_and_objects.py: classes, instances, properties, classmethods, staticmethods, dunder methods
- design_patterns.py: singleton, factory, observer, abstract-factory patterns
- encapsulation_and_properties.py: property decorator, getters and setters, name mangling, access control
- inheritance_and_polymorphism.py: abstract base classes, inheritance, polymorphic dispatch
- magic_methods.py: arithmetic dunder methods, comparisons, hashing, context-manager methods
- oop_advanced.py: method-resolution order, super calls, inheritance chains
- oop_deep_dive.py: multiple inheritance, mixins, composition, dataclass patterns

## Core Example
This example shows inheritance, polymorphism, and a readable object representation.

```python
class Animal:
	def speak(self):
		return "sound"

class Dog(Animal):
	def speak(self):
		return "bark"

pet = Dog()
print(type(pet).__name__, pet.speak())
```
