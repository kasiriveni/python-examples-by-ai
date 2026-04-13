"""
Slots and memory optimization in Python.
"""
import sys

# === Regular class ===
class RegularPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# === Slotted class ===
class SlottedPoint:
    __slots__ = ('x', 'y')

    def __init__(self, x, y):
        self.x = x
        self.y = y

# === Memory comparison ===
print("=== Memory Comparison ===")
rp = RegularPoint(1, 2)
sp = SlottedPoint(1, 2)

rp_size = sys.getsizeof(rp) + sys.getsizeof(rp.__dict__)
sp_size = sys.getsizeof(sp)
print(f"Regular: {rp_size} bytes (obj + __dict__)")
print(f"Slotted: {sp_size} bytes")
print(f"Savings: {rp_size - sp_size} bytes ({(1 - sp_size/rp_size)*100:.0f}%)")

# Large-scale comparison
n = 100_000
import tracemalloc
tracemalloc.start()

regular_list = [RegularPoint(i, i) for i in range(n)]
snapshot1 = tracemalloc.take_snapshot()

del regular_list
tracemalloc.stop()

tracemalloc.start()
slotted_list = [SlottedPoint(i, i) for i in range(n)]
snapshot2 = tracemalloc.take_snapshot()
del slotted_list
tracemalloc.stop()

# === Slots limitations ===
print("\n=== Slots Limitations ===")

# Cannot add dynamic attributes
try:
    sp.z = 3
except AttributeError as e:
    print(f"Cannot add attribute: {e}")

# No __dict__ available
print(f"Has __dict__: {hasattr(sp, '__dict__')}")

# Slots with inheritance
class SlottedPoint3D(SlottedPoint):
    __slots__ = ('z',)

    def __init__(self, x, y, z):
        super().__init__(x, y)
        self.z = z

p3d = SlottedPoint3D(1, 2, 3)
print(f"\n3D Point: ({p3d.x}, {p3d.y}, {p3d.z})")
print(f"Slots: {SlottedPoint3D.__slots__}")

# === Slots with default values ===
class Config:
    __slots__ = ('host', 'port', 'debug')

    def __init__(self, host='localhost', port=8080, debug=False):
        self.host = host
        self.port = port
        self.debug = debug

    def __repr__(self):
        return f"Config({self.host}:{self.port}, debug={self.debug})"

config = Config(port=3000)
print(f"\nConfig: {config}")

# === Weakref with slots (need __weakref__) ===
import weakref

class WeakRefSlotted:
    __slots__ = ('value', '__weakref__')

    def __init__(self, value):
        self.value = value

obj = WeakRefSlotted(42)
ref = weakref.ref(obj)
print(f"\nWeakref value: {ref().value}")
