"""
Integers in Python - comprehensive examples.
"""

# Integer literals
decimal = 42
binary = 0b101010       # 42
octal = 0o52            # 42
hexadecimal = 0x2A      # 42

print(f"Decimal: {decimal}")
print(f"Binary 0b101010 = {binary}")
print(f"Octal 0o52 = {octal}")
print(f"Hex 0x2A = {hexadecimal}")

# Large integers (Python has arbitrary precision)
big_number = 10 ** 100
print(f"10^100 = {big_number}")
print(f"Type: {type(big_number)}")

# Underscore separators for readability
population = 7_900_000_000
print(f"World population: {population:,}")

# Integer methods
n = -42
print(f"{n}.bit_length() = {n.bit_length()}")
print(f"(255).to_bytes(2, 'big') = {(255).to_bytes(2, 'big')}")
print(f"int.from_bytes(b'\\x00\\xff', 'big') = {int.from_bytes(b'\\x00\\xff', 'big')}")

# Base conversions
print(f"bin(255) = {bin(255)}")
print(f"oct(255) = {oct(255)}")
print(f"hex(255) = {hex(255)}")
print(f"int('ff', 16) = {int('ff', 16)}")
print(f"int('11111111', 2) = {int('11111111', 2)}")
