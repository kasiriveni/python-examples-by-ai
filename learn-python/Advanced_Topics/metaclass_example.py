"""
Example of using metaclasses to enforce class attributes.
"""
class AttributeEnforcer(type):
    def __new__(cls, name, bases, dct):
        if 'required_attribute' not in dct:
            raise TypeError(f"Class {name} must define 'required_attribute'")
        return super().__new__(cls, name, bases, dct)

class MyClass(metaclass=AttributeEnforcer):
    required_attribute = 42

if __name__ == "__main__":
    obj = MyClass()
    print(f"Required attribute: {obj.required_attribute}")
