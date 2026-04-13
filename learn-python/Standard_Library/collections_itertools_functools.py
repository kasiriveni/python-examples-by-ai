"""
Standard Library: Collections, itertools, and functools deep dive.
"""
from collections import Counter, defaultdict, deque, namedtuple, OrderedDict, ChainMap
from itertools import (chain, combinations, permutations, product, groupby,
                       islice, count, cycle, repeat, starmap, accumulate,
                       takewhile, dropwhile, zip_longest)
from functools import reduce, partial, lru_cache, total_ordering, wraps
from operator import add, mul, itemgetter, attrgetter

# ═══════════════════════════════════════════
# COLLECTIONS
# ═══════════════════════════════════════════
print("=== collections ===\n")

# Counter
words = "to be or not to be that is the question".split()
counter = Counter(words)
print(f"Counter: {counter.most_common(3)}")
print(f"Total: {counter.total()}")

# Counter arithmetic
c1 = Counter(a=3, b=1, c=2)
c2 = Counter(a=1, b=2, d=1)
print(f"c1 + c2 = {c1 + c2}")
print(f"c1 - c2 = {c1 - c2}")

# defaultdict
tree = lambda: defaultdict(tree)
filesystem = tree()
filesystem["home"]["user"]["documents"]["file.txt"] = "content"
print(f"\ndefaultdict tree created")

# deque
dq = deque(maxlen=5)
for i in range(8):
    dq.append(i)
print(f"Deque (maxlen=5): {dq}")
dq.rotate(2)
print(f"After rotate(2): {dq}")

# namedtuple
Point = namedtuple('Point', ['x', 'y', 'z'], defaults=[0])
p = Point(1, 2)
print(f"\nNamedTuple: {p}, z={p.z}")
print(f"As dict: {p._asdict()}")

# ═══════════════════════════════════════════
# ITERTOOLS
# ═══════════════════════════════════════════
print("\n=== itertools ===\n")

# Infinite iterators
print("count:   ", list(islice(count(10, 2), 5)))
print("cycle:   ", list(islice(cycle("ABC"), 8)))
print("repeat:  ", list(repeat("x", 4)))

# Combinatoric
print(f"\ncombinations('ABC', 2): {list(combinations('ABC', 2))}")
print(f"permutations('AB', 2):  {list(permutations('AB', 2))}")
print(f"product('AB', '12'):    {list(product('AB', '12'))}")

# Filtering
data = [1, 4, 2, 7, 3, 8, 5]
print(f"\ntakewhile(<5): {list(takewhile(lambda x: x < 5, data))}")
print(f"dropwhile(<5): {list(dropwhile(lambda x: x < 5, data))}")

# Chaining
lists = [[1, 2], [3, 4], [5, 6]]
print(f"chain:         {list(chain.from_iterable(lists))}")

# Groupby
data = [("fruit", "apple"), ("veggie", "carrot"), ("fruit", "banana"), ("veggie", "pea")]
data.sort(key=itemgetter(0))
for key, group in groupby(data, key=itemgetter(0)):
    print(f"  {key}: {[item[1] for item in group]}")

# Accumulate
nums = [1, 2, 3, 4, 5]
print(f"\naccumulate(sum): {list(accumulate(nums))}")
print(f"accumulate(mul): {list(accumulate(nums, mul))}")
print(f"accumulate(max): {list(accumulate([3, 1, 4, 1, 5, 9], max))}")

# ═══════════════════════════════════════════
# FUNCTOOLS
# ═══════════════════════════════════════════
print("\n=== functools ===\n")

# partial
base2_int = partial(int, base=2)
print(f"partial int(base=2)('1010') = {base2_int('1010')}")

# reduce
factorial = reduce(mul, range(1, 6))
print(f"reduce factorial(5) = {factorial}")

# lru_cache
@lru_cache(maxsize=256)
def expensive(n):
    return sum(i*i for i in range(n))

expensive(1000)
expensive(1000)  # cached
print(f"lru_cache info: {expensive.cache_info()}")

# total_ordering
@total_ordering
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade
    def __eq__(self, other):
        return self.grade == other.grade
    def __lt__(self, other):
        return self.grade < other.grade
    def __repr__(self):
        return f"{self.name}({self.grade})"

students = [Student("Alice", 90), Student("Bob", 85), Student("Charlie", 95)]
print(f"\nSorted students: {sorted(students)}")
print(f"Max: {max(students)}")