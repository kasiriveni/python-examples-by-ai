"""
Advanced Python: Weakrefs, __slots__, and memory optimization.
"""
import sys
import weakref
import gc
from dataclasses import dataclass

# ═══════════════════════════════════════════
# 1. __slots__ — fixed attribute layout
# ═══════════════════════════════════════════
print("=== __slots__ ===")

class RegularPoint:
    def __init__(self, x, y, z):
        self.x = x; self.y = y; self.z = z

class SlottedPoint:
    __slots__ = ('x', 'y', 'z')
    def __init__(self, x, y, z):
        self.x = x; self.y = y; self.z = z

class InheritedSlots(SlottedPoint):
    __slots__ = ('color',)  # Add new slot; inherits x, y, z
    def __init__(self, x, y, z, color):
        super().__init__(x, y, z)
        self.color = color

r = RegularPoint(1, 2, 3)
s = SlottedPoint(1, 2, 3)

r_size = sys.getsizeof(r) + sys.getsizeof(r.__dict__)
s_size = sys.getsizeof(s)

print(f"Regular: {r_size} bytes (includes __dict__)")
print(f"Slotted: {s_size} bytes")
print(f"Savings: {r_size - s_size} bytes per object")

# Slotted objects can't have arbitrary attributes
try:
    s.w = 4
    print(f"Added w: {s.w}")
except AttributeError as e:
    print(f"AttributeError: {e}")

# Inherited slots work
cs = InheritedSlots(1, 2, 3, "red")
print(f"InheritedSlots: x={cs.x}, color={cs.color}")

# Benchmark: create 100k objects
import time
N = 100_000

start = time.perf_counter()
regular_pts = [RegularPoint(i, i*2, i*3) for i in range(N)]
t_regular = time.perf_counter() - start

start = time.perf_counter()
slotted_pts = [SlottedPoint(i, i*2, i*3) for i in range(N)]
t_slotted = time.perf_counter() - start

print(f"\nCreating {N:,} objects:")
print(f"  Regular: {t_regular:.3f}s")
print(f"  Slotted: {t_slotted:.3f}s")
total_r = sum(sys.getsizeof(p)+sys.getsizeof(p.__dict__) for p in regular_pts[:100]) * 1000
total_s = sum(sys.getsizeof(p) for p in slotted_pts[:100]) * 1000
print(f"  Regular RAM (est): {total_r/1024:.0f} KB")
print(f"  Slotted RAM (est): {total_s/1024:.0f} KB")

# ═══════════════════════════════════════════
# 2. Weak references
# ═══════════════════════════════════════════
print("\n=== Weak References ===")

class Resource:
    def __init__(self, name: str):
        self.name = name
        print(f"  [+] Resource '{name}' created")

    def __del__(self):
        print(f"  [-] Resource '{self.name}' destroyed")

    def use(self): return f"Using {self.name}"

# Strong reference — keeps object alive
strong = Resource("strong")

# Weak reference — does NOT prevent garbage collection
weak = weakref.ref(Resource("weak"))  # intermediate resource, will be GC'd
print(f"Weak ref alive: {weak() is not None}")

gc.collect()
print(f"After gc.collect, weak ref alive: {weak() is not None}")

# Access via weak ref
resource = Resource("example")
ref = weakref.ref(resource)
print(f"ref(): {ref()}")
print(f"ref().use(): {ref().use()}")

del resource  # strong ref deleted
gc.collect()
print(f"After del, ref(): {ref()}")

# ═══════════════════════════════════════════
# 3. WeakValueDictionary — cache without memory leak
# ═══════════════════════════════════════════
print("\n=== WeakValueDictionary (Cache) ===")

class ExpensiveObject:
    def __init__(self, key):
        self.key = key
        self.data = list(range(100))
    def __repr__(self): return f"ExpensiveObject({self.key})"

cache = weakref.WeakValueDictionary()

# Create and cache
for k in ["a", "b", "c"]:
    obj = ExpensiveObject(k)
    cache[k] = obj  # cacheed, obj is strong ref in local scope

print(f"Cache size: {len(cache)}")  # 3

# Remove strong references — cache entries disappear
del obj          # removes last strong ref (from loop final iteration)
gc.collect()
print(f"After del last obj, cache size: {len(cache)}")

# ═══════════════════════════════════════════
# 4. Interning and identity
# ═══════════════════════════════════════════
print("\n=== Object Interning ===")

# Small integers are interned
a, b = 100, 100
print(f"100 is 100: {a is b}")     # True (interned)
a, b = 1000, 1000
print(f"1000 is 1000: {a is b}")   # Often False (CPython specific)

# String interning
s1 = "hello"
s2 = "hello"
s3 = sys.intern("world")
s4 = sys.intern("world")
print(f"'hello' is 'hello': {s1 is s2}")    # True (compile-time intern)
print(f"interned 'world' is: {s3 is s4}")   # True

# ═══════════════════════════════════════════
# 5. Memory-efficient alternatives
# ═══════════════════════════════════════════
print("\n=== Memory-Efficient Patterns ===")

# Generator vs list
import types
gen = (x**2 for x in range(100_000))
lst = [x**2 for x in range(100_000)]
print(f"Generator size: {sys.getsizeof(gen)} bytes")
print(f"List size:      {sys.getsizeof(lst):,} bytes")

# array module — typed, compact arrays
import array
py_list  = list(range(10_000))
int_arr  = array.array('i', range(10_000))
long_arr = array.array('q', range(10_000))  # 8 bytes each

print(f"\nlist of 10k ints:    {sys.getsizeof(py_list):,} bytes")
print(f"array('i') 10k:      {sys.getsizeof(int_arr):,} bytes  (4 bytes each)")
print(f"array('q') 10k:      {sys.getsizeof(long_arr):,} bytes  (8 bytes each)")

# bytes vs list of ints
byte_list = list(range(256))
byte_buf  = bytes(range(256))
print(f"\nlist of 256 ints: {sys.getsizeof(byte_list):,} bytes")
print(f"bytes(256):       {sys.getsizeof(byte_buf):,} bytes")
