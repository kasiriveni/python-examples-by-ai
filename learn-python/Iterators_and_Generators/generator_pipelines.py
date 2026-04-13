"""
Iterators and Generators: Generator pipelines and coroutine patterns.
Efficient lazy data processing without loading everything into memory.
"""
import time
from typing import Generator, Iterable, TypeVar

T = TypeVar("T")

# ═══════════════════════════════════════════
# 1. Basic generator functions
# ═══════════════════════════════════════════
def infinite_counter(start=0, step=1):
    """Infinite counting generator."""
    n = start
    while True:
        yield n
        n += step

def take(n: int, iterable) -> list:
    """Take first n items from an iterable."""
    result = []
    it = iter(iterable)
    for _ in range(n):
        try:
            result.append(next(it))
        except StopIteration:
            break
    return result

# ═══════════════════════════════════════════
# 2. Pipeline components
# ═══════════════════════════════════════════
def read_lines(text: str) -> Generator[str, None, None]:
    """Simulate reading lines from a file/source."""
    for line in text.strip().split("\n"):
        yield line

def clean(lines: Iterable[str]) -> Generator[str, None, None]:
    """Strip whitespace, skip blank lines."""
    for line in lines:
        stripped = line.strip()
        if stripped:
            yield stripped

def to_lower(lines: Iterable[str]) -> Generator[str, None, None]:
    for line in lines:
        yield line.lower()

def split_words(lines: Iterable[str]) -> Generator[str, None, None]:
    for line in lines:
        for word in line.split():
            yield word

def remove_punctuation(words: Iterable[str]) -> Generator[str, None, None]:
    import string
    table = str.maketrans("", "", string.punctuation)
    for word in words:
        clean = word.translate(table)
        if clean:
            yield clean

def filter_stopwords(words: Iterable[str], stopwords: set) -> Generator[str, None, None]:
    for word in words:
        if word not in stopwords:
            yield word

def window(iterable, size: int) -> Generator[tuple, None, None]:
    """Sliding window of `size` items."""
    buf = []
    for item in iterable:
        buf.append(item)
        if len(buf) == size:
            yield tuple(buf)
            buf.pop(0)

def batch(iterable, size: int) -> Generator[list, None, None]:
    """Non-overlapping batches."""
    batch = []
    for item in iterable:
        batch.append(item)
        if len(batch) == size:
            yield batch
            batch = []
    if batch:
        yield batch

def transform(func, iterable) -> Generator:
    """Map via generator (like map())."""
    for item in iterable:
        yield func(item)

def where(pred, iterable) -> Generator:
    """Filter via generator (like filter())."""
    for item in iterable:
        if pred(item):
            yield item

def flatten(nested: Iterable) -> Generator:
    """Flatten one level of nesting."""
    for item in nested:
        try:
            yield from item
        except TypeError:
            yield item

# ═══════════════════════════════════════════
# 3. Pipeline builder
# ═══════════════════════════════════════════
class Pipeline:
    """Chainable lazy pipeline over an iterable."""

    def __init__(self, source):
        self._source = iter(source)

    def map(self, func) -> "Pipeline":
        self._source = (func(x) for x in self._source)
        return self

    def filter(self, pred) -> "Pipeline":
        self._source = (x for x in self._source if pred(x))
        return self

    def flatten(self) -> "Pipeline":
        self._source = flatten(self._source)
        return self

    def batch(self, size: int) -> "Pipeline":
        self._source = batch(self._source, size)
        return self

    def take(self, n: int) -> "Pipeline":
        self._source = (x for _, x in zip(range(n), self._source))
        return self

    def limit(self, n: int) -> "Pipeline":
        return self.take(n)

    def to_list(self) -> list:
        return list(self._source)

    def first(self, default=None):
        return next(self._source, default)

    def count(self) -> int:
        return sum(1 for _ in self._source)

    def __iter__(self):
        return self._source

# ═══════════════════════════════════════════
# 4. Coroutine (send/receive generator)
# ═══════════════════════════════════════════
def accumulator():
    """Coroutine that accumulates sent values."""
    total = 0
    count = 0
    while True:
        value = yield (total, count)
        if value is None:
            break
        total += value
        count += 1

def running_average():
    """Coroutine computing running average."""
    total = 0
    count = 0
    average = None
    while True:
        value = yield average
        if value is not None:
            total += value
            count += 1
            average = total / count

# ═══════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════
if __name__ == "__main__":
    print("=== Infinite Generator ===")
    evens = where(lambda x: x % 2 == 0, infinite_counter())
    print(f"First 8 evens: {take(8, evens)}")

    print("\n=== Text Processing Pipeline ===")
    TEXT = """
    The quick brown fox jumps over the lazy dog.
    Python is a great language for data processing.
    The fox ran quickly, but the dog was too lazy to chase.
    """
    STOP = {"the", "a", "is", "for", "to", "but", "was", "too",
            "over", "an", "and", "in", "of"}

    words = (
        filter_stopwords(
            remove_punctuation(
                split_words(
                    to_lower(
                        clean(read_lines(TEXT))))),
            STOP)
    )

    from collections import Counter
    freq = Counter(words).most_common(8)
    print(f"Top 8 words: {freq}")

    print("\n=== Sliding Window ===")
    data = list(range(1, 8))
    windows = list(window(data, 3))
    print(f"Windows(3): {windows}")
    averages = [sum(w)/len(w) for w in windows]
    print(f"Moving avg: {[f'{a:.2f}' for a in averages]}")

    print("\n=== Pipeline Builder ===")
    result = (Pipeline(range(100))
              .filter(lambda x: x % 3 == 0)
              .map(lambda x: x ** 2)
              .take(10)
              .to_list())
    print(f"Pipeline result: {result}")

    # Batch pipeline
    batches = (Pipeline(range(20))
               .filter(lambda x: x % 2 == 0)
               .batch(3)
               .to_list())
    print(f"Batches: {batches}")

    print("\n=== Coroutine Accumulator ===")
    acc = accumulator()
    next(acc)  # prime
    for v in [10, 20, 30, 40]:
        total, count = acc.send(v)
        print(f"  Sent {v}: total={total}, count={count}")

    print("\n=== Running Average Coroutine ===")
    avg_cr = running_average()
    next(avg_cr)  # prime
    for v in [4, 7, 2, 9, 5, 3]:
        avg = avg_cr.send(v)
        print(f"  After {v}: avg = {avg:.3f}")
