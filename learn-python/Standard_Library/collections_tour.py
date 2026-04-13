"""
Standard Library: collections module — an in-depth tour.
"""
from collections import (
    Counter, defaultdict, OrderedDict, ChainMap,
    deque, namedtuple, UserDict, UserList, UserString
)
import heapq
from typing import Any

# ═══════════════════════════════════════════
# 1. Counter
# ═══════════════════════════════════════════
def demo_counter():
    print("=== Counter ===")
    text = "the quick brown fox jumps over the lazy dog"
    char_count = Counter(text.replace(" ", ""))
    print(f"  Top 5 chars: {char_count.most_common(5)}")

    word_count = Counter(text.split())
    print(f"  Word count: {dict(word_count)}")

    c1 = Counter(a=4, b=2, c=0, d=-2)
    c2 = Counter(a=1, b=2, c=3, d=4)
    print(f"  c1+c2: {c1 + c2}")
    print(f"  c1-c2: {c1 - c2}")
    print(f"  c1|c2 (union):     {c1 | c2}")
    print(f"  c1&c2 (intersect): {c1 & c2}")

    # elements() reconstructs the sequence
    print(f"  elements: {sorted(Counter('aabbc').elements())}")

# ═══════════════════════════════════════════
# 2. defaultdict
# ═══════════════════════════════════════════
def demo_defaultdict():
    print("\n=== defaultdict ===")

    # Grouping
    words = ["apple", "ant", "bear", "banana", "cherry", "cat"]
    by_letter: defaultdict[str, list[str]] = defaultdict(list)
    for w in words:
        by_letter[w[0]].append(w)
    for letter, group in sorted(by_letter.items()):
        print(f"  {letter}: {group}")

    # Nested defaultdict (2D grid)
    grid: defaultdict[int, defaultdict[int, int]] = defaultdict(lambda: defaultdict(int))
    for r in range(3):
        for c in range(3):
            grid[r][c] = r * 3 + c
    print(f"  grid[1][2] = {grid[1][2]}")

    # Default factory patterns
    dd_int   = defaultdict(int);    dd_int["x"] += 5
    dd_set   = defaultdict(set);    dd_set["a"].add(1); dd_set["a"].add(2)
    dd_str   = defaultdict(str);    dd_str["k"] += "hello"
    print(f"  int: {dict(dd_int)}, set: {dict(dd_set)}, str: {dict(dd_str)}")

# ═══════════════════════════════════════════
# 3. OrderedDict
# ═══════════════════════════════════════════
def demo_ordereddict():
    print("\n=== OrderedDict ===")
    od = OrderedDict([("one", 1), ("two", 2), ("three", 3)])

    # move_to_end
    od.move_to_end("one")
    print(f"  After move_to_end('one'): {list(od.items())}")
    od.move_to_end("three", last=False)
    print(f"  After move_to_end('three', last=False): {list(od.items())}")

    # LRU cache using OrderedDict
    class LRUCache:
        def __init__(self, capacity: int):
            self._cap = capacity
            self._cache: OrderedDict[Any, Any] = OrderedDict()

        def get(self, key):
            if key not in self._cache: return -1
            self._cache.move_to_end(key)
            return self._cache[key]

        def put(self, key, value):
            if key in self._cache:
                self._cache.move_to_end(key)
            self._cache[key] = value
            if len(self._cache) > self._cap:
                self._cache.popitem(last=False)  # evict LRU

        def __repr__(self): return repr(dict(self._cache))

    lru = LRUCache(3)
    lru.put(1, "a"); lru.put(2, "b"); lru.put(3, "c")
    print(f"  LRU: {lru}")
    lru.get(1)        # access 1 → moved to end
    lru.put(4, "d")   # evicts key 2 (least recently used)
    print(f"  After get(1) then put(4): {lru}")
    print(f"  get(2) = {lru.get(2)}")

# ═══════════════════════════════════════════
# 4. deque (efficient O(1) append/pop from both ends)
# ═══════════════════════════════════════════
def demo_deque():
    print("\n=== deque ===")
    dq: deque[int] = deque([1, 2, 3, 4, 5])
    dq.appendleft(0)
    dq.append(6)
    print(f"  After appendleft(0), append(6): {list(dq)}")
    dq.rotate(2)   # shift right by 2
    print(f"  After rotate(2): {list(dq)}")
    dq.rotate(-3)  # shift left by 3
    print(f"  After rotate(-3): {list(dq)}")

    # Fixed-size sliding window
    window: deque[int] = deque(maxlen=3)
    stream = [1, 2, 3, 4, 5, 6]
    for item in stream:
        window.append(item)
        print(f"  stream={item} window={list(window)} avg={sum(window)/len(window):.1f}")

# ═══════════════════════════════════════════
# 5. ChainMap
# ═══════════════════════════════════════════
def demo_chainmap():
    print("\n=== ChainMap (layered lookups) ===")
    # Simulates os.environ layering
    defaults  = {"color": "blue", "font": "Arial", "size": 12}
    user_prefs= {"color": "red",  "size": 14}
    session   = {"color": "green"}

    # ChainMap reads left to right (first found wins)
    config = ChainMap(session, user_prefs, defaults)
    print(f"  color: {config['color']}")   # green (session wins)
    print(f"  font:  {config['font']}")    # Arial (only in defaults)
    print(f"  size:  {config['size']}")    # 14    (user_prefs wins)

    # new_child adds a new layer (context scope)
    child = config.new_child({"debug": True})
    print(f"  child debug: {child.get('debug')}")
    print(f"  child color: {child['color']}")

# ═══════════════════════════════════════════
# 6. namedtuple
# ═══════════════════════════════════════════
def demo_namedtuple():
    print("\n=== namedtuple ===")
    Point = namedtuple("Point", ["x", "y"])
    Color = namedtuple("Color", "r g b a", defaults=[255])

    p = Point(3, 4)
    print(f"  Point: {p}")
    print(f"  x={p.x}, distance={p.x**2 + p.y**2:.1f}^0.5")

    c = Color(255, 128, 0)     # a defaults to 255
    print(f"  Color: {c}")

    # _replace creates a new instance with some fields changed
    p2 = p._replace(x=0)
    print(f"  p._replace(x=0): {p2}")

    # _asdict, _fields
    print(f"  as dict: {p._asdict()}")
    print(f"  fields:  {Point._fields}")

# ═══════════════════════════════════════════
# 7. UserDict, UserList, UserString (subclassable)
# ═══════════════════════════════════════════
class CaseInsensitiveDict(UserDict):
    """Keys normalized to lowercase."""
    def __setitem__(self, key, value): super().__setitem__(key.lower(), value)
    def __getitem__(self, key):        return super().__getitem__(key.lower())
    def __contains__(self, key):       return super().__contains__(key.lower())

class BoundedList(UserList):
    """List with max capacity."""
    def __init__(self, iterable=(), maxlen=5):
        self.maxlen = maxlen
        super().__init__(iterable)
    def append(self, item):
        if len(self) >= self.maxlen: raise OverflowError(f"max {self.maxlen} items")
        super().append(item)

if __name__ == "__main__":
    demo_counter()
    demo_defaultdict()
    demo_ordereddict()
    demo_deque()
    demo_chainmap()
    demo_namedtuple()

    print("\n=== UserDict / UserList ===")
    d = CaseInsensitiveDict({"Hello": "world"})
    d["Python"] = "rocks"
    print(f"  {'HELLO' in d}, {d['python']!r}")

    bl = BoundedList([1, 2, 3], maxlen=4)
    bl.append(4)
    try:
        bl.append(5)
    except OverflowError as e:
        print(f"  BoundedList: {e}")
