"""
Enums in Python.
"""
from enum import Enum, IntEnum, Flag, auto, unique

# Basic Enum
class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

print(f"Color.RED = {Color.RED}")
print(f"Color.RED.name = {Color.RED.name}")
print(f"Color.RED.value = {Color.RED.value}")
print(f"Color(2) = {Color(2)}")
print(f"Color['BLUE'] = {Color['BLUE']}")

# Iterating
for color in Color:
    print(f"  {color.name}: {color.value}")

# auto() values
class Direction(Enum):
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()

print(f"\nDirections: {list(Direction)}")

# IntEnum (can be compared with ints)
class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

print(f"\nPriority.HIGH > 2: {Priority.HIGH > 2}")
print(f"Sorted: {sorted(Priority)}")

# Flag enum (bitwise operations)
class Permission(Flag):
    READ = auto()
    WRITE = auto()
    EXECUTE = auto()

admin = Permission.READ | Permission.WRITE | Permission.EXECUTE
print(f"\nAdmin perms: {admin}")
print(f"Has READ: {Permission.READ in admin}")

# Unique decorator (ensures no duplicate values)
@unique
class Status(Enum):
    ACTIVE = 1
    INACTIVE = 2
    PENDING = 3

# Enum with methods
class Planet(Enum):
    MERCURY = (3.303e+23, 2.4397e6)
    VENUS = (4.869e+24, 6.0518e6)
    EARTH = (5.976e+24, 6.37814e6)

    def __init__(self, mass, radius):
        self.mass = mass
        self.radius = radius

    @property
    def surface_gravity(self):
        G = 6.67300E-11
        return G * self.mass / (self.radius ** 2)

for planet in Planet:
    print(f"{planet.name}: gravity = {planet.surface_gravity:.2f} m/s²")
