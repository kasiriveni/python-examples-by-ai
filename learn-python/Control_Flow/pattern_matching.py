"""
Pattern matching (match/case) - Python 3.10+
"""

# Structural pattern matching
def describe_point(point):
    match point:
        case (0, 0):
            return "Origin"
        case (x, 0):
            return f"On x-axis at {x}"
        case (0, y):
            return f"On y-axis at {y}"
        case (x, y):
            return f"Point({x}, {y})"

points = [(0, 0), (5, 0), (0, 3), (2, 7)]
for p in points:
    print(f"  {p} -> {describe_point(p)}")

# Matching with classes
class Command:
    pass

class Quit(Command):
    pass

class Move(Command):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Say(Command):
    def __init__(self, message):
        self.message = message

def handle_command(cmd):
    match cmd:
        case Quit():
            return "Quitting..."
        case Move(x=x, y=y):
            return f"Moving to ({x}, {y})"
        case Say(message=msg):
            return f"Saying: {msg}"
        case _:
            return "Unknown command"

commands = [Move(10, 20), Say("hello"), Quit()]
for cmd in commands:
    print(f"  {handle_command(cmd)}")

# Matching sequences
def analyze_sequence(seq):
    match seq:
        case []:
            return "empty"
        case [x]:
            return f"single element: {x}"
        case [x, y]:
            return f"pair: {x}, {y}"
        case [x, *rest]:
            return f"starts with {x}, {len(rest)} more"

sequences = [[], [1], [1, 2], [1, 2, 3, 4, 5]]
for s in sequences:
    print(f"  {s} -> {analyze_sequence(s)}")

# Matching dictionaries
def process_event(event):
    match event:
        case {"type": "click", "x": x, "y": y}:
            return f"Click at ({x}, {y})"
        case {"type": "keypress", "key": k}:
            return f"Key pressed: {k}"
        case {"type": "scroll", "direction": d}:
            return f"Scrolling {d}"
        case _:
            return "Unknown event"

events = [
    {"type": "click", "x": 100, "y": 200},
    {"type": "keypress", "key": "Enter"},
    {"type": "scroll", "direction": "up"},
]
for e in events:
    print(f"  {process_event(e)}")

# OR patterns
def categorize(value):
    match value:
        case 0 | 1:
            return "binary"
        case n if n < 0:
            return "negative"
        case n if n < 100:
            return "small"
        case _:
            return "large"

for v in [0, 1, -5, 42, 999]:
    print(f"  {v} -> {categorize(v)}")
