"""
Control Flow: Advanced branching, guards, early returns, and pattern matching.
"""
from typing import Union
from dataclasses import dataclass

# ═══════════════════════════════════════════
# 1. Early return / guard clause pattern
# ═══════════════════════════════════════════
def process_order_nested(order: dict) -> str:
    """Anti-pattern: deeply nested conditions."""
    if order:
        if "user" in order:
            if order["user"].get("active"):
                if "items" in order and order["items"]:
                    return "OK"
                else:
                    return "No items"
            else:
                return "Inactive user"
        else:
            return "No user"
    else:
        return "Empty order"

def process_order(order: dict) -> str:
    """Guard clause style — flat, readable."""
    if not order:               return "Empty order"
    if "user" not in order:     return "No user"
    if not order["user"].get("active"): return "Inactive user"
    if not order.get("items"):  return "No items"
    return "OK"

# ═══════════════════════════════════════════
# 2. Structural pattern matching (Python 3.10+)
# ═══════════════════════════════════════════
@dataclass
class Point2D: x: float; y: float
@dataclass
class Circle:  center: Point2D; radius: float
@dataclass
class Rect:    top_left: Point2D; bottom_right: Point2D
@dataclass
class Line:    start: Point2D; end: Point2D

def describe_shape(shape) -> str:
    match shape:
        case Circle(center=Point2D(x=0, y=0), radius=r):
            return f"Unit-origin circle, r={r}"
        case Circle(radius=r) if r <= 0:
            return "Degenerate circle (r<=0)"
        case Circle(center=c, radius=r):
            return f"Circle at ({c.x},{c.y}), r={r}"
        case Rect(top_left=tl, bottom_right=br):
            w = br.x - tl.x; h = br.y - tl.y
            return f"Rect {w}×{h}, area={w*h}"
        case Line():
            return "A line segment"
        case _:
            return f"Unknown: {type(shape).__name__}"

def handle_command(command: dict) -> str:
    """REST-like command router via match."""
    match command:
        case {"action": "get",    "resource": str(r), "id": int(i)}:
            return f"GET {r}#{i}"
        case {"action": "create", "resource": str(r), "data": dict(d)}:
            return f"CREATE {r} with {len(d)} fields"
        case {"action": "delete", "resource": str(r)}:
            return f"DELETE {r}"
        case {"action": str(a)}:
            return f"Unknown action: {a!r}"
        case _:
            return "Invalid command"

# ═══════════════════════════════════════════
# 3. Conditional expressions and walrus
# ═══════════════════════════════════════════
def grade(score: int) -> str:
    return ("A" if score >= 90 else
            "B" if score >= 80 else
            "C" if score >= 70 else
            "D" if score >= 60 else "F")

def find_first_long(words: list[str], min_length: int = 5) -> str | None:
    return next((w for w in words if len(w) >= min_length), None)

def parse_numbers(text: str) -> list[int]:
    import re
    return [int(m.group()) for line in text.splitlines()
            if (m := re.search(r'\d+', line))]

# ═══════════════════════════════════════════
# 4. Short-circuit evaluation tricks
# ═══════════════════════════════════════════
def get_name(user: dict | None) -> str:
    return (user or {}).get("name") or "Anonymous"

def coalesce(*values):
    """Return first non-None, non-falsy value."""
    return next((v for v in values if v is not None and v != ""), None)

# ═══════════════════════════════════════════
# 5. Exception-based control flow
# ═══════════════════════════════════════════
class StopProcessing(Exception):
    def __init__(self, result): self.result = result

def pipeline_step(value: int) -> int:
    if value < 0:   raise StopProcessing(0)
    if value > 100: raise StopProcessing(100)
    return value * 2

def safe_pipeline(value: int) -> int:
    try:
        x = pipeline_step(value)
        x = pipeline_step(x - 10)
        return x
    except StopProcessing as e:
        return e.result

# ═══════════════════════════════════════════
# 6. Ternary chains and dispatch
# ═══════════════════════════════════════════
HANDLERS = {
    "add":  lambda a, b: a + b,
    "sub":  lambda a, b: a - b,
    "mul":  lambda a, b: a * b,
    "div":  lambda a, b: a / b if b != 0 else float("inf"),
}

def dispatch(op: str, a: float, b: float) -> float:
    handler = HANDLERS.get(op)
    if handler is None:
        raise ValueError(f"Unknown operation: {op!r}")
    return handler(a, b)

# ═══════════════════════════════════════════
# 7. Context-based branching
# ═══════════════════════════════════════════
import os

def get_config() -> dict:
    env = os.getenv("ENV", "development")
    base = {"debug": False, "log_level": "INFO", "workers": 4}
    match env:
        case "production":
            return {**base, "debug": False, "workers": 8}
        case "staging":
            return {**base, "debug": True, "log_level": "DEBUG", "workers": 2}
        case "test":
            return {**base, "debug": True, "log_level": "WARNING", "workers": 1}
        case _:
            return {**base, "debug": True, "log_level": "DEBUG", "workers": 1}

# ═══════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════
if __name__ == "__main__":
    print("=== Guard Clauses ===")
    cases = [
        {},
        {"user": {"active": True}},
        {"user": {"active": False}},
        {"user": {"active": True}, "items": []},
        {"user": {"active": True}, "items": ["pizza"]},
    ]
    for c in cases:
        print(f"  {str(c)[:40]!r} → {process_order(c)!r}")

    print("\n=== Structural Pattern Matching (shapes) ===")
    shapes = [
        Circle(Point2D(0, 0), 5),
        Circle(Point2D(3, 4), -1),
        Rect(Point2D(0, 0), Point2D(4, 3)),
        Line(Point2D(0, 0), Point2D(1, 1)),
        "not a shape",
    ]
    for s in shapes:
        print(f"  {describe_shape(s)}")

    print("\n=== Pattern Matching (commands) ===")
    cmds = [
        {"action": "get", "resource": "users", "id": 42},
        {"action": "create", "resource": "posts", "data": {"title": "Hello", "body": "..."}},
        {"action": "delete", "resource": "comments"},
        {"action": "patch"},
        {},
    ]
    for c in cmds:
        print(f"  {handle_command(c)}")

    print("\n=== Conditional expressions ===")
    for score in [95, 83, 72, 61, 40]:
        print(f"  {score} → {grade(score)}")

    print("\n=== Walrus + find ===")
    words = ["hi", "python", "is", "great"]
    result = find_first_long(words)
    print(f"  First long word: {result!r}")

    text = "line 1: 42\nno numbers here\nline 3: 99\nmore: 7"
    print(f"  Parsed numbers: {parse_numbers(text)}")

    print("\n=== Short-circuit ===")
    for user in [None, {}, {"name": ""}, {"name": "Alice"}]:
        print(f"  {str(user):30s} → {get_name(user)!r}")

    print("\n=== Coalesce ===")
    print(f"  {coalesce(None, '', 0, 'hello', 'world')!r}")

    print("\n=== Dispatch table ===")
    for op, a, b in [("add", 10, 5), ("mul", 3, 7), ("div", 10, 0)]:
        print(f"  {op}({a},{b}) = {dispatch(op, a, b)}")

    print("\n=== Safe pipeline ===")
    for val in [-5, 30, 200]:
        print(f"  pipeline({val}) = {safe_pipeline(val)}")
