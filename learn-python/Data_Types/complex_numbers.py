"""
Complex numbers in Python.
"""

# Creating complex numbers
z1 = 3 + 4j
z2 = complex(1, -2)
z3 = complex("5+3j")
print(f"z1 = {z1}, z2 = {z2}, z3 = {z3}")

# Accessing parts
print(f"z1.real = {z1.real}")
print(f"z1.imag = {z1.imag}")
print(f"z1.conjugate() = {z1.conjugate()}")

# Arithmetic
print(f"z1 + z2 = {z1 + z2}")
print(f"z1 - z2 = {z1 - z2}")
print(f"z1 * z2 = {z1 * z2}")
print(f"z1 / z2 = {z1 / z2}")
print(f"z1 ** 2 = {z1 ** 2}")

# Magnitude and phase
import cmath
print(f"|z1| = {abs(z1)}")
print(f"Phase of z1 = {cmath.phase(z1)}")
print(f"Polar form: {cmath.polar(z1)}")
print(f"From polar: {cmath.rect(5.0, 0.9272952180016122)}")

# Complex math functions
print(f"sqrt(-1) = {cmath.sqrt(-1)}")
print(f"e^(pi*i) = {cmath.exp(cmath.pi * 1j)}")
print(f"log(z1) = {cmath.log(z1)}")
