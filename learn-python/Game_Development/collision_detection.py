"""
Game Development: Collision Detection Algorithms.
Covers AABB, circle, SAT, and spatial hashing.
"""
import math
from dataclasses import dataclass

# ═══════════════════════════════════════════
# SHAPES
# ═══════════════════════════════════════════
@dataclass
class Rect:
    x: float; y: float; w: float; h: float

    @property
    def right(self): return self.x + self.w
    @property
    def bottom(self): return self.y + self.h
    @property
    def center(self): return (self.x + self.w/2, self.y + self.h/2)

@dataclass
class Circle:
    cx: float; cy: float; r: float

@dataclass
class Point:
    x: float; y: float

# ═══════════════════════════════════════════
# AABB (Axis-Aligned Bounding Box)
# ═══════════════════════════════════════════
def aabb_aabb(a: Rect, b: Rect) -> bool:
    """Returns True if two AABBs overlap."""
    return (a.x < b.right and a.right > b.x and
            a.y < b.bottom and a.bottom > b.y)

def aabb_overlap(a: Rect, b: Rect) -> tuple[float, float] | None:
    """Returns (overlap_x, overlap_y) penetration depth, or None."""
    if not aabb_aabb(a, b):
        return None
    ox = min(a.right, b.right) - max(a.x, b.x)
    oy = min(a.bottom, b.bottom) - max(a.y, b.y)
    return (ox, oy)

def point_in_rect(p: Point, r: Rect) -> bool:
    return r.x <= p.x <= r.right and r.y <= p.y <= r.bottom

# ═══════════════════════════════════════════
# Circle Collisions
# ═══════════════════════════════════════════
def circle_circle(a: Circle, b: Circle) -> bool:
    dist = math.sqrt((a.cx - b.cx)**2 + (a.cy - b.cy)**2)
    return dist < a.r + b.r

def circle_point(c: Circle, p: Point) -> bool:
    return math.sqrt((c.cx - p.x)**2 + (c.cy - p.y)**2) <= c.r

def circle_rect(c: Circle, r: Rect) -> bool:
    """Circle-AABB collision using closest point."""
    closest_x = max(r.x, min(c.cx, r.right))
    closest_y = max(r.y, min(c.cy, r.bottom))
    dist = math.sqrt((c.cx - closest_x)**2 + (c.cy - closest_y)**2)
    return dist <= c.r

# ═══════════════════════════════════════════
# Sweep (moving AABB)
# ═══════════════════════════════════════════
def swept_aabb(moving: Rect, vx: float, vy: float, static: Rect) -> float:
    """
    Returns time of collision [0, 1] for moving AABB against static AABB.
    1.0 means no collision during this frame.
    """
    # Entry/exit times on each axis
    if vx > 0:
        x_entry = (static.x - moving.right) / vx
        x_exit  = (static.right - moving.x) / vx
    elif vx < 0:
        x_entry = (static.right - moving.x) / vx
        x_exit  = (static.x - moving.right) / vx
    else:
        x_entry = float('-inf')
        x_exit  = float('inf')

    if vy > 0:
        y_entry = (static.y - moving.bottom) / vy
        y_exit  = (static.bottom - moving.y) / vy
    elif vy < 0:
        y_entry = (static.bottom - moving.y) / vy
        y_exit  = (static.y - moving.bottom) / vy
    else:
        y_entry = float('-inf')
        y_exit  = float('inf')

    entry = max(x_entry, y_entry)
    exit_ = min(x_exit, y_exit)

    if entry > exit_ or entry > 1.0 or exit_ < 0:
        return 1.0
    return max(0.0, entry)

# ═══════════════════════════════════════════
# Spatial Hashing
# ═══════════════════════════════════════════
class SpatialHash:
    """Partition space into cells for O(1) broad-phase collision."""

    def __init__(self, cell_size: float = 64.0):
        self.cell_size = cell_size
        self._grid: dict[tuple[int, int], list] = {}

    def _cells_for(self, r: Rect) -> list[tuple[int, int]]:
        x0 = int(r.x // self.cell_size)
        y0 = int(r.y // self.cell_size)
        x1 = int(r.right // self.cell_size)
        y1 = int(r.bottom // self.cell_size)
        return [(cx, cy) for cx in range(x0, x1+1) for cy in range(y0, y1+1)]

    def insert(self, obj, rect: Rect) -> None:
        for cell in self._cells_for(rect):
            self._grid.setdefault(cell, []).append(obj)

    def query(self, rect: Rect) -> set:
        candidates = set()
        for cell in self._cells_for(rect):
            for obj in self._grid.get(cell, []):
                candidates.add(obj)
        return candidates

    def clear(self) -> None:
        self._grid.clear()

# ═══════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════
if __name__ == "__main__":
    print("=== AABB Collision ===")
    a = Rect(0, 0, 50, 50)
    b = Rect(30, 30, 50, 50)      # overlaps
    c = Rect(100, 100, 50, 50)    # no overlap

    print(f"A {a} vs B {b}: {aabb_aabb(a, b)}")  # True
    print(f"A {a} vs C {c}: {aabb_aabb(a, c)}")  # False
    print(f"Overlap depth: {aabb_overlap(a, b)}")

    print("\n=== Point Tests ===")
    p_in  = Point(20, 20)
    p_out = Point(80, 80)
    print(f"Point {p_in} in A: {point_in_rect(p_in, a)}")
    print(f"Point {p_out} in A: {point_in_rect(p_out, a)}")

    print("\n=== Circle Collision ===")
    c1 = Circle(50, 50, 30)
    c2 = Circle(70, 70, 20)   # overlaps (dist=28.3, radii sum=50)
    c3 = Circle(200, 200, 10)

    print(f"Circle vs Circle (overlap): {circle_circle(c1, c2)}")
    print(f"Circle vs Circle (apart):  {circle_circle(c1, c3)}")
    print(f"Circle vs Rect: {circle_rect(c1, a)}")
    print(f"Circle contains point (20,20): {circle_point(c1, Point(20,20))}")

    print("\n=== Swept AABB ===")
    moving = Rect(0, 0, 20, 20)
    static = Rect(80, 0, 20, 20)
    t = swept_aabb(moving, 100, 0, static)
    print(f"Hit time: {t:.2f} (moving right at v=100)")

    no_hit = swept_aabb(moving, 30, 0, static)
    print(f"No hit time: {no_hit:.2f} (moving right at v=30, won't reach)")

    print("\n=== Spatial Hash ===")
    sh = SpatialHash(cell_size=64)
    objects = [("player", Rect(10, 10, 32, 32)),
               ("enemy1", Rect(50, 50, 32, 32)),
               ("enemy2", Rect(500, 500, 32, 32)),
               ("coin",   Rect(20, 20, 16, 16))]

    for name, rect in objects:
        sh.insert(name, rect)

    query_rect = Rect(0, 0, 64, 64)
    nearby = sh.query(query_rect)
    print(f"Objects near top-left 64x64: {nearby}")
