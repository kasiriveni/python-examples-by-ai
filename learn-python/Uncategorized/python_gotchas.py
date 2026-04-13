"""
Uncategorized: Common Python gotchas, anti-patterns, and how to fix them.
"""

# ═══════════════════════════════════════════
# 1. Mutable default arguments
# ═══════════════════════════════════════════
print("=== Gotcha: Mutable Default Arguments ===")

# ❌ BUG
def append_bad(item, lst=[]):
    lst.append(item)
    return lst

# All calls share the SAME list!
print(f"append_bad(1): {append_bad(1)}")
print(f"append_bad(2): {append_bad(2)}")   # Surprise: [1, 2]

# ✅ FIX: use None sentinel
def append_good(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst

print(f"append_good(1): {append_good(1)}")
print(f"append_good(2): {append_good(2)}")  # Correct: [2]

# ═══════════════════════════════════════════
# 2. Late binding closures
# ═══════════════════════════════════════════
print("\n=== Gotcha: Late Binding Closures ===")

# ❌ BUG: all functions print 4
funcs_bad = [(lambda: i) for i in range(5)]
print(f"Bad (all 4): {[f() for f in funcs_bad]}")

# ✅ FIX: default argument captures value early
funcs_good = [(lambda i=i: i) for i in range(5)]
print(f"Good (0-4):  {[f() for f in funcs_good]}")

# ═══════════════════════════════════════════
# 3. Integer identity vs equality
# ═══════════════════════════════════════════
print("\n=== Gotcha: is vs == ===")

a = 256; b = 256
print(f"256 is 256: {a is b}")   # True (cached small integer)

a = 257; b = 257
print(f"257 is 257: {a is b}")   # May be True (CPython caches at module compile time)

a = int(input.__doc__[:1]) if False else 257
b = int(input.__doc__[:1]) if False else 257
print("Lesson: Always use == for value comparison, is only for None/True/False")

# ═══════════════════════════════════════════
# 4. Class-level vs instance-level attributes
# ═══════════════════════════════════════════
print("\n=== Gotcha: Class vs Instance Attributes ===")

class Counter:
    count = 0  # class-level attribute — SHARED

    def increment_bad(self): self.count += 1   # Shadows class attr
    def increment_fix(self): Counter.count += 1  # Modifies class attr

    # ✅ Best practice: always use instance attrs in __init__
class CounterGood:
    def __init__(self):
        self.count = 0     # instance-level
    def increment(self): self.count += 1

c1 = Counter(); c2 = Counter()
c1.count = 99   # shadows, doesn't affect c2
print(f"Class count after c1.count=99: {Counter.count}")  # still 0

g1, g2 = CounterGood(), CounterGood()
g1.increment()
print(f"g1.count={g1.count}, g2.count={g2.count}")  # 1, 0 ✓

# ═══════════════════════════════════════════
# 5. Iterating while modifying
# ═══════════════════════════════════════════
print("\n=== Gotcha: Modifying During Iteration ===")

# ❌ BUG
lst = [1, 2, 3, 4, 5, 6]
try:
    for item in lst:
        if item % 2 == 0:
            lst.remove(item)   # skips elements!
    print(f"Bad removal (skipped): {lst}")
except Exception as e:
    print(f"Error: {e}")

# ✅ FIX: iterate over a copy, or use list comprehension
lst = [1, 2, 3, 4, 5, 6]
for item in lst[:]:          # iterate over copy
    if item % 2 == 0:
        lst.remove(item)
print(f"Good removal:  {lst}")

lst = [1, 2, 3, 4, 5, 6]
lst = [x for x in lst if x % 2 != 0]  # comprehension
print(f"Comprehension: {lst}")

# ═══════════════════════════════════════════
# 6. Chained comparisons with 'not in' / 'is not'
# ═══════════════════════════════════════════
print("\n=== Gotcha: not x is None vs x is not None ===")

x = [1, 2, 3]
print(f"not x is None:  {not x is None}")   # ❌ reads as: not (x is None) = True
print(f"x is not None:  {x is not None}")   # ✅ clear

x = None
print(f"not x is None (None): {not x is None}")  # True but misleading
print(f"x is not None (None): {x is not None}")  # False ✓

# ═══════════════════════════════════════════
# 7. Copy vs deepcopy
# ═══════════════════════════════════════════
print("\n=== Gotcha: Shallow vs Deep Copy ===")
import copy

original = {"a": [1, 2, 3], "b": [4, 5, 6]}
shallow  = copy.copy(original)
deep     = copy.deepcopy(original)

original["a"].append(99)
print(f"After original['a'].append(99):")
print(f"  original: {original['a']}")
print(f"  shallow:  {shallow['a']}   ← also changed!")
print(f"  deep:     {deep['a']}     ← unchanged ✓")

# ═══════════════════════════════════════════
# 8. Exception handling anti-patterns
# ═══════════════════════════════════════════
print("\n=== Exception Gotchas ===")

# ❌ Bare except swallows KeyboardInterrupt too!
try:
    x = 1/0
except:  # noqa  bad practice
    pass

# ✅ Always name the exception
try:
    x = 1/0
except ZeroDivisionError as e:
    print(f"  Caught ZeroDivisionError: {e}")

# ❌ Exception variable leaks in Python — surprise!
try:
    raise ValueError("oops")
except ValueError as err:
    pass
try:
    print(f"  err: {err}")  # NameError in Python 3!
except NameError:
    print("  'err' doesn't exist after except block (by design)")

# ═══════════════════════════════════════════
# 9. Truthiness gotchas
# ═══════════════════════════════════════════
print("\n=== Falsy Values Gotchas ===")
falsy = [0, 0.0, 0j, "", b"", [], {}, set(), None, False]
for v in falsy:
    print(f"  bool({str(v):8s}) = {bool(v)}")

# ❌ Gotcha: 0 is falsy but may be valid data
def process(value=None):
    if not value:          # ❌ treats 0 as no-value
        value = "default"
    return value

def process_fixed(value=None):
    if value is None:      # ✅ only skips truly absent values
        value = "default"
    return value

print(f"\n  process(0):       {process(0)}")        # 'default' (wrong!)
print(f"  process_fixed(0): {process_fixed(0)}")   # 0 (correct)
