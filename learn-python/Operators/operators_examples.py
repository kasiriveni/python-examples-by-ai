# Operators examples: arithmetic, comparison, bitwise, walrus
# Walrus operator
if (n := 5) > 0:
    print(f"n is {n}")

# Bitwise
a = 6  # 110
b = 3  # 011
print("a & b =", a & b)
print("a | b =", a | b)
print("a ^ b =", a ^ b)

# Comparison
x = 10
y = 20
print("x == y:", x == y)
print("x != y:", x != y)
print("x > y:", x > y)
print("x < y:", x < y)
print("x >= y:", x >= y)
print("x <= y:", x <= y)


# Arithmetic
num1 = 15
num2 = 4
print("num1 + num2 =", num1 + num2)
print("num1 - num2 =", num1 - num2)
print("num1 * num2 =", num1 * num2)
print("num1 / num2 =", num1 / num2)
print("num1 // num2 =", num1 // num2)  # Floor division
print("num1 % num2 =", num1 % num2)    # Modulus
print("num1 ** num2 =", num1 ** num2)  # Exponentiation


# Assignment
a = 5
print("Initial value of a:", a)
a += 3
print("After a += 3:", a)
a *= 2
print("After a *= 2:", a)
a -= 4
print("After a -= 4:", a)
a /= 2
print("After a /= 2:", a)

# Logical
p = True
q = False
print("p and q:", p and q)
print("p or q:", p or q)
print("not p:", not p)


# Identity
list1 = [1, 2, 3]
list2 = list1
list3 = [1, 2, 3]
print("list1 is list2:", list1 is list2)
print("list1 is list3:", list1 is list3)



