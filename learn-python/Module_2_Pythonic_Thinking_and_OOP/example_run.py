"""Example runner for Module 2: Pythonic Thinking and OOP"""

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return f"Person(name={self.name!r}, age={self.age})"


def main():
    print("Module 2 - OOP example")
    p = Person("Ada", 36)
    print(p)
    print("Greeting:", f'Hello, {p.name}!')


if __name__ == "__main__":
    main()
