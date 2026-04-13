"""
Iterators and Generators: itertools — an interactive tour.
"""
import itertools
import operator
from collections import deque

# ═══════════════════════════════════════════
# 1. Infinite iterators
# ═══════════════════════════════════════════
def demo_infinite():
    print("=== Infinite Iterators ===")

    # count — equivalent to range but infinite
    counter = itertools.count(start=10, step=5)
    print(f"  count(10, 5) x5: {list(itertools.islice(counter, 5))}")

    # cycle — repeat a sequence forever
    cycled = itertools.cycle("ABCD")
    print(f"  cycle('ABCD') x7: {list(itertools.islice(cycled, 7))}")

    # repeat — repeat one element
    print(f"  repeat(7, 4): {list(itertools.repeat(7, 4))}")
    # repeat without limit + zip trick
    doubled = list(map(operator.mul, range(5), itertools.repeat(2)))
    print(f"  x2 via repeat: {doubled}")

# ═══════════════════════════════════════════
# 2. Combinatoric iterators
# ═══════════════════════════════════════════
def demo_combinatoric():
    print("\n=== Combinatoric Iterators ===")

    digits = [1, 2, 3]
    print(f"  permutations([1,2,3], 2): {list(itertools.permutations(digits, 2))}")
    print(f"  combinations([1,2,3], 2): {list(itertools.combinations(digits, 2))}")
    print(f"  comb_w_replace([1,2,3],2): {list(itertools.combinations_with_replacement(digits, 2))}")
    print(f"  product([1,2],[A,B]):       {list(itertools.product([1, 2], 'AB'))}")
    print(f"  product(range(2), repeat=3): {list(itertools.product(range(2), repeat=3))}")

    # Practical: generate all 2-char passwords from digits+alpha
    pool = "abc123"
    pw_count = sum(1 for _ in itertools.product(pool, repeat=2))
    print(f"  2-char passwords from '{pool}': {pw_count}")

# ═══════════════════════════════════════════
# 3. Finite chaining
# ═══════════════════════════════════════════
def demo_chaining():
    print("\n=== Chaining Iterators ===")

    a, b, c = [1, 2], [3, 4], [5, 6]
    print(f"  chain: {list(itertools.chain(a, b, c))}")
    nested = [[1, 2], [3, 4], [5, 6]]
    print(f"  chain.from_iterable: {list(itertools.chain.from_iterable(nested))}")

    # islice
    gen = (x**2 for x in itertools.count())
    print(f"  first 6 squares: {list(itertools.islice(gen, 6))}")
    gen2 = itertools.count()
    print(f"  islice(5,10,2): {list(itertools.islice(gen2, 5, 10, 2))}")

    # zip_longest
    short = [1, 2, 3]; long = [10, 20, 30, 40, 50]
    print(f"  zip_longest: {list(itertools.zip_longest(short, long, fillvalue=0))}")

# ═══════════════════════════════════════════
# 4. Filtering and selection
# ═══════════════════════════════════════════
def demo_filtering():
    print("\n=== Filtering / Selection ===")

    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    evens = list(itertools.compress(data, [i % 2 == 0 for i in data]))
    print(f"  compress (evens): {evens}")

    # dropwhile / takewhile
    nums = [1, 3, 5, 2, 4, 6, 7]
    print(f"  takewhile(<5): {list(itertools.takewhile(lambda x: x < 5, nums))}")
    print(f"  dropwhile(<5): {list(itertools.dropwhile(lambda x: x < 5, nums))}")

    # filterfalse
    print(f"  filterfalse(even): {list(itertools.filterfalse(lambda x: x%2==0, range(10)))}")

# ═══════════════════════════════════════════
# 5. Grouping
# ═══════════════════════════════════════════
def demo_groupby():
    print("\n=== groupby ===")

    words = ["apple", "ant", "bear", "banana", "cherry", "cat"]
    words.sort(key=lambda w: w[0])   # MUST sort before groupby
    for letter, group in itertools.groupby(words, key=lambda w: w[0]):
        print(f"  '{letter}': {list(group)}")

    # Real-world: group transactions by category
    transactions = [
        {"cat": "food",  "amount": 12.0},
        {"cat": "food",  "amount": 8.5},
        {"cat": "travel","amount": 200.0},
        {"cat": "travel","amount": 45.0},
        {"cat": "food",  "amount": 5.0},
    ]
    # Group by category (pre-sort required)
    transactions.sort(key=lambda t: t["cat"])
    print("\n  Spending by category:")
    for cat, items in itertools.groupby(transactions, key=lambda t: t["cat"]):
        total = sum(i["amount"] for i in items)
        print(f"    {cat}: ${total:.2f}")

# ═══════════════════════════════════════════
# 6. Accumulate
# ═══════════════════════════════════════════
def demo_accumulate():
    print("\n=== accumulate ===")

    numbers = [1, 2, 3, 4, 5]
    print(f"  running sum:     {list(itertools.accumulate(numbers))}")
    print(f"  running product: {list(itertools.accumulate(numbers, operator.mul))}")
    print(f"  running max:     {list(itertools.accumulate(numbers, max))}")

    # Running min with initial
    prices = [5, 3, 8, 1, 9, 2]
    print(f"  prices:          {prices}")
    print(f"  running min:     {list(itertools.accumulate(prices, min))}")
    # Compute max drawdown: price - running max
    running_max = list(itertools.accumulate(prices, max))
    drawdowns = [p - rm for p, rm in zip(prices, running_max)]
    print(f"  drawdowns:       {drawdowns}")
    print(f"  max drawdown:    {min(drawdowns)}")

# ═══════════════════════════════════════════
# 7. Practical recipes
# ═══════════════════════════════════════════
def sliding_window(iterable, n):
    """[1,2,3,4,5], 3 → (1,2,3),(2,3,4),(3,4,5)"""
    it = iter(iterable)
    window = deque(itertools.islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for item in it:
        window.append(item)
        yield tuple(window)

def batched(iterable, n):
    """Yield successive n-sized chunks."""
    it = iter(iterable)
    while True:
        batch = list(itertools.islice(it, n))
        if not batch:
            break
        yield batch

def unique_everseen(iterable, key=None):
    """Maintain order, remove duplicates."""
    seen = set()
    for el in iterable:
        k = key(el) if key else el
        if k not in seen:
            seen.add(k)
            yield el

if __name__ == "__main__":
    demo_infinite()
    demo_combinatoric()
    demo_chaining()
    demo_filtering()
    demo_groupby()
    demo_accumulate()

    print("\n=== Recipes ===")
    data = [1, 2, 3, 4, 5, 6, 7]
    print(f"  sliding_window(3): {list(sliding_window(data, 3))}")
    print(f"  batched(3):        {list(batched(data, 3))}")
    dupes = [1, 2, 2, 3, 1, 4, 3, 5]
    print(f"  unique_everseen:   {list(unique_everseen(dupes))}")

    # Flatten with chain.from_iterable
    nested = [[1, 2], [3, [4, 5]], [6]]
    flat = list(itertools.chain.from_iterable(nested))
    print(f"  flatten 1 level:   {flat}")

    # Round-robin from multiple iterables
    def roundrobin(*iterables):
        pending = len(iterables)
        nexts = itertools.cycle(iter(it).__next__ for it in iterables)
        while pending:
            try:
                for n in nexts:
                    yield n()
            except StopIteration:
                pending -= 1
                nexts = itertools.cycle(itertools.islice(nexts, pending))

    rr = list(roundrobin("ABCD", "EF", "GHI"))
    print(f"  roundrobin:        {rr}")
