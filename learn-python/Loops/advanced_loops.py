"""
Loops: Advanced loop patterns — comprehensions, zip, enumerate, itertools recipes.
"""
import itertools
import time
from typing import Iterator, Generator

# ═══════════════════════════════════════════
# 1. List / dict / set / generator comprehensions
# ═══════════════════════════════════════════
def demo_comprehensions():
    print("=== Comprehensions ===")

    # Flat list comprehension
    squares = [x**2 for x in range(10)]
    print(f"  squares: {squares}")

    # With condition
    evens = [x for x in range(20) if x % 2 == 0]
    print(f"  evens:   {evens}")

    # Nested (matrix flattening)
    matrix = [[1,2,3],[4,5,6],[7,8,9]]
    flat = [cell for row in matrix for cell in row]
    print(f"  flat:    {flat}")

    # Dict comprehension
    word_lengths = {w: len(w) for w in ["python", "is", "great"]}
    print(f"  word_lengths: {word_lengths}")

    # Inverted dict
    inv = {v: k for k, v in word_lengths.items()}
    print(f"  inverted: {inv}")

    # Set comprehension
    unique_mods = {x % 5 for x in range(20)}
    print(f"  unique_mods: {unique_mods}")

    # Generator expression (lazy)
    gen = (x**3 for x in range(5))
    print(f"  gen cubes: {list(gen)}")

    # Filtering nested structures
    people = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 17}, {"name": "Carol", "age": 25}]
    adults = [p["name"] for p in people if p["age"] >= 18]
    print(f"  adults: {adults}")

# ═══════════════════════════════════════════
# 2. enumerate, zip, zip_longest
# ═══════════════════════════════════════════
def demo_enumerate_zip():
    print("\n=== enumerate / zip ===")

    fruits = ["apple", "banana", "cherry"]
    for i, fruit in enumerate(fruits, start=1):
        print(f"  {i}. {fruit}")

    names  = ["Alice", "Bob", "Carol"]
    scores = [92, 87, 95]
    max_score, winner = max(zip(scores, names))
    print(f"  Winner: {winner} with {max_score}")

    for name, score in zip(names, scores):
        print(f"  {name}: {score}")

    # zip_longest pads shorter iterables
    a = [1, 2, 3]; b = ["a", "b"]
    paired = list(itertools.zip_longest(a, b, fillvalue="?"))
    print(f"  zip_longest: {paired}")

    # Transpose a matrix
    mat = [[1,2,3],[4,5,6],[7,8,9]]
    transposed = [list(row) for row in zip(*mat)]
    print(f"  transposed: {transposed}")

# ═══════════════════════════════════════════
# 3. for/else and while/else
# ═══════════════════════════════════════════
def demo_for_else():
    print("\n=== for/else ===")

    def find_prime(start: int, end: int) -> int | None:
        for n in range(start, end + 1):
            for d in range(2, int(n**0.5) + 1):
                if n % d == 0:
                    break
            else:
                return n   # for/else: loop ended without break → n is prime
        return None

    print(f"  First prime in 10-20: {find_prime(10, 20)}")
    print(f"  Prime search 14-15: {find_prime(14, 15)}")

    # while/else
    queue = [3, 1, 4, 1, 5, 9]
    target = 5
    while queue:
        val = queue.pop(0)
        if val == target:
            print(f"  Found {target} in queue")
            break
    else:
        print(f"  {target} not found in queue")

# ═══════════════════════════════════════════
# 4. Loop control: break, continue, nested break
# ═══════════════════════════════════════════
def demo_loop_control():
    print("\n=== Loop control ===")

    # continue — skip even numbers
    odds = []
    for x in range(10):
        if x % 2 == 0: continue
        odds.append(x)
    print(f"  odds via continue: {odds}")

    # break — find first composite
    for n in range(2, 20):
        for d in range(2, n):
            if n % d == 0:
                print(f"  First composite: {n} = {d} × {n//d}")
                break
        else:
            continue
        break

    # Nested break via function
    def nested_search(grid: list[list[int]], target: int) -> tuple[int,int] | None:
        for r, row in enumerate(grid):
            for c, val in enumerate(row):
                if val == target:
                    return (r, c)
        return None

    grid = [[1,2,3],[4,5,6],[7,8,9]]
    print(f"  Found 5 at: {nested_search(grid, 5)}")
    print(f"  Found 99 at: {nested_search(grid, 99)}")

# ═══════════════════════════════════════════
# 5. Generator-based loops
# ═══════════════════════════════════════════
def fibonacci_loop(n: int) -> Generator[int, None, None]:
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

def infinite_counter(start: int = 0, step: int = 1) -> Generator[int, None, None]:
    n = start
    while True:
        yield n
        n += step

def first_n(gen: Iterator, n: int) -> list:
    return [next(gen) for _ in range(n)]

def demo_generators_loops():
    print("\n=== Generator-based loops ===")
    print(f"  Fibonacci(10): {list(fibonacci_loop(10))}")
    counter = infinite_counter(100, 7)
    print(f"  Counter x5:    {first_n(counter, 5)}")

    # Chained generators as pipeline
    numbers = range(1, 21)
    pipeline = (x**2 for x in numbers if x % 2 == 0)
    print(f"  Even²<10: {[x for x in pipeline if x < 100]}")

# ═══════════════════════════════════════════
# 6. Performance: loop vs comprehension vs map
# ═══════════════════════════════════════════
def demo_performance():
    print("\n=== Performance comparison ===")
    N = 100_000

    def time_it(name: str, fn):
        start = time.perf_counter()
        result = fn()
        elapsed = (time.perf_counter() - start) * 1000
        print(f"  {name:30s}: {elapsed:.2f}ms  (len={len(result)})")

    time_it("for loop",         lambda: [x**2 for _ in range(1) for x in range(N)])
    time_it("list comprehension",lambda: [x**2 for x in range(N)])
    time_it("map+list",         lambda: list(map(lambda x: x**2, range(N))))
    time_it("gen+list",         lambda: list(x**2 for x in range(N)))

if __name__ == "__main__":
    demo_comprehensions()
    demo_enumerate_zip()
    demo_for_else()
    demo_loop_control()
    demo_generators_loops()
    demo_performance()
