# Example: Classes, Inheritance, and MRO
# Demonstrates class inheritance and Method Resolution Order (MRO)

class A:
    def greet(self):
        print("Hello from A")

class B(A):
    def greet(self):
        print("Hello from B")

class C(A):
    def greet(self):
        print("Hello from C")

class D(B, C):
    pass

# MRO demonstration
obj = D()
obj.greet()
print(D.mro())
