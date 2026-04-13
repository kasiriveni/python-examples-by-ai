"""
Operators: Bitwise ops, operator module, augmented assignment, and custom overloading.
"""
from __future__ import annotations
import operator
import functools

# ═══════════════════════════════════════════
# 1. Custom Vector with full operator support
# ═══════════════════════════════════════════
class Vector:
    def __init__(self, x: float, y: float):
        self.x = x; self.y = y

    def __add__(self, other): return Vector(self.x + other.x, self.y + other.y)
    def __sub__(self, other): return Vector(self.x - other.x, self.y - other.y)
    def __mul__(self, s):     return Vector(self.x * s, self.y * s)
    def __rmul__(self, s):    return self.__mul__(s)
    def __truediv__(self, s): return Vector(self.x / s, self.y / s)
    def __neg__(self):        return Vector(-self.x, -self.y)
    def __abs__(self):        return (self.x**2 + self.y**2) ** 0.5
    def __matmul__(self, o):  return self.x*o.x + self.y*o.y   # dot product
    def __iter__(self):       yield self.x; yield self.y
    def __len__(self):        return 2
    def __bool__(self):       return self.x != 0 or self.y != 0
    def __eq__(self, other):
        if not isinstance(other, Vector): return NotImplemented
        return (self.x, self.y) == (other.x, other.y)
    def __repr__(self):       return f"Vector({self.x}, {self.y})"
    def __lt__(self, other):  return abs(self) < abs(other)

    def normalized(self):
        m = abs(self)
        if m == 0: raise ZeroDivisionError
        return self / m

# ═══════════════════════════════════════════
# 2. Bitwise tricks
# ═══════════════════════════════════════════
def bitwise_demo():
    print("=== Bitwise operators ===")
    a, b = 0b1010_1100, 0b1111_0000
    for label, result in [
        ("a & b  (AND)", a & b),
        ("a | b  (OR)",  a | b),
        ("a ^ b  (XOR)", a ^ b),
        ("~a     (NOT)", ~a),
        ("a << 2 (×4)",  a << 2),
        ("a >> 2 (÷4)",  a >> 2),
    ]:
        print(f"  {label:16s} = {result:>12} ({result & 0xFFFF:016b})")

    print("\n=== Bit tricks ===")
    for n in range(1, 17):
        is_pow2 = (n & (n - 1)) == 0
        print(f"  {n:2d} {'yes' if is_pow2 else 'no ':3s}", end="  ")
        if n % 4 == 0: print()
    print()

    # Swap without temp using XOR
    x, y = 123, 456
    x ^= y; y ^= x; x ^= y
    print(f"  XOR swap: x={x}, y={y}")

    # Bit flags (permissions)
    READ, WRITE, EXEC = 1, 2, 4
    perm = 0
    perm |= READ | WRITE    # set
    perm &= ~WRITE          # clear WRITE
    perm ^= EXEC            # toggle EXEC
    print(f"  Permissions: r={'on' if perm&READ else 'off'} "
          f"w={'on' if perm&WRITE else 'off'} "
          f"x={'on' if perm&EXEC else 'off'}")

# ═══════════════════════════════════════════
# 3. operator module
# ═══════════════════════════════════════════
def operator_module_demo():
    print("\n=== operator module ===")
    pairs = [(10, 3), (7, 4), (100, 99)]
    for a, b in pairs:
        row = [f"{name}={fn(a,b)}"
               for name, fn in [
                   ("add",  operator.add),
                   ("sub",  operator.sub),
                   ("mul",  operator.mul),
                   ("mod",  operator.mod),
                   ("pow",  operator.pow),
               ]]
        print(f"  ({a},{b}): {', '.join(row)}")

    # itemgetter / attrgetter
    records = [{"name":"Charlie","score":88},
               {"name":"Alice","score":95},
               {"name":"Bob","score":72}]
    for key in ["name","score"]:
        sorted_r = sorted(records, key=operator.itemgetter(key))
        print(f"  by {key}: {[r['name'] for r in sorted_r]}")

    # reduce + operator
    nums = list(range(1, 6))
    product = functools.reduce(operator.mul, nums, 1)
    print(f"  product {nums} = {product}")

# ═══════════════════════════════════════════
# 4. Augmented assignment behaviour
# ═══════════════════════════════════════════
def augmented_assignment_demo():
    print("\n=== Augmented assignment ===")
    x = 10
    x += 5;  print(f"  += : {x}")
    x -= 3;  print(f"  -= : {x}")
    x *= 2;  print(f"  *= : {x}")
    x //= 3; print(f"  //=: {x}")
    x **= 2; print(f"  **=: {x}")
    x %= 7;  print(f"  %%= : {x}")

    # List += mutates in place
    a = [1, 2, 3]; b = a
    a += [4, 5]
    print(f"  list +=: same object = {a is b}  (both: {a})")

    # Tuple += creates new object
    t = (1, 2, 3); u = t
    t += (4, 5)
    print(f"  tuple +=: same object = {t is u}  (t: {t})")

# ═══════════════════════════════════════════
# 5. Walrus operator (assignment expression)
# ═══════════════════════════════════════════
def walrus_demo():
    print("\n=== Walrus operator := ===")
    import re
    patterns = [r"\d+", r"[a-z]+"]
    text = "abc 123 def"
    for pat in patterns:
        if m := re.search(pat, text):
            print(f"  pattern={pat!r} → match={m.group()!r}")

    # while with walrus
    data = iter([1, 3, 5, 2, 7, 4])
    while (n := next(data, None)) is not None:
        if n > 4: print(f"  First > 4: {n}"); break

    # list comprehension filter and transform in one pass
    lines = ["  hello  ", "", "  world  ", "   "]
    cleaned = [s for line in lines if (s := line.strip())]
    print(f"  cleaned: {cleaned}")

# ═══════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════
if __name__ == "__main__":
    print("=== Vector arithmetic ===")
    v1 = Vector(3, 4)
    v2 = Vector(1, 2)
    print(f"  v1={v1}, |v1|={abs(v1)}")
    print(f"  v1+v2={v1+v2}  v1-v2={v1-v2}")
    print(f"  v1*2={v1*2}  3*v1={3*v1}")
    print(f"  v1@v2={v1@v2} (dot)  v1.normalized()={v1.normalized()}")
    print(f"  sorted: {sorted([Vector(5,0), Vector(1,0), Vector(3,4)])}")

    bitwise_demo()
    operator_module_demo()
    augmented_assignment_demo()
    walrus_demo()
