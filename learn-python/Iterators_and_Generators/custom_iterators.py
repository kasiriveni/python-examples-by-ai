"""
Iterators and Generators: Custom iterator classes.
Demonstrates __iter__, __next__, StopIteration, and advanced patterns.
"""
from __future__ import annotations
from typing import Iterator, TypeVar, Generic

T = TypeVar("T")

# ═══════════════════════════════════════════
# 1. Simple range-like iterator
# ═══════════════════════════════════════════
class CountUp:
    """Counts from start to stop (exclusive) by step."""

    def __init__(self, start: int = 0, stop: int = 10, step: int = 1):
        if step == 0:
            raise ValueError("step cannot be 0")
        self.start = start
        self.stop = stop
        self.step = step

    def __iter__(self) -> Iterator[int]:
        current = self.start
        while (self.step > 0 and current < self.stop) or \
              (self.step < 0 and current > self.stop):
            yield current
            current += self.step

# ═══════════════════════════════════════════
# 2. Stateful iterator using a class
# ═══════════════════════════════════════════
class Fibonacci:
    """Infinite Fibonacci iterator."""

    def __init__(self, limit: int | None = None):
        self.limit = limit
        self._a = 0
        self._b = 1
        self._count = 0

    def __iter__(self):
        return self

    def __next__(self) -> int:
        if self.limit is not None and self._count >= self.limit:
            raise StopIteration
        value = self._a
        self._a, self._b = self._b, self._a + self._b
        self._count += 1
        return value

    def reset(self):
        self._a, self._b, self._count = 0, 1, 0

# ═══════════════════════════════════════════
# 3. Linked list iterator
# ═══════════════════════════════════════════
class Node(Generic[T]):
    def __init__(self, value: T, next: Node | None = None):
        self.value = value
        self.next = next

class LinkedList(Generic[T]):
    def __init__(self):
        self._head: Node[T] | None = None
        self._size = 0

    def append(self, value: T):
        node = Node(value)
        if not self._head:
            self._head = node
        else:
            curr = self._head
            while curr.next:
                curr = curr.next
            curr.next = node
        self._size += 1

    def __iter__(self) -> Iterator[T]:
        current = self._head
        while current:
            yield current.value
            current = current.next

    def __len__(self):
        return self._size

    def __reversed__(self):
        # Collect, then yield in reverse
        values = list(self)
        for v in reversed(values):
            yield v

    def __contains__(self, value: T) -> bool:
        return any(v == value for v in self)

# ═══════════════════════════════════════════
# 4. Tree in-order iterator
# ═══════════════════════════════════════════
class BSTNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

class InOrderIterator:
    """Iterative in-order BST traversal using an explicit stack."""

    def __init__(self, root: BSTNode | None):
        self._stack: list[BSTNode] = []
        self._push_left(root)

    def _push_left(self, node):
        while node:
            self._stack.append(node)
            node = node.left

    def __iter__(self):
        return self

    def __next__(self) -> int:
        if not self._stack:
            raise StopIteration
        node = self._stack.pop()
        value = node.val
        self._push_left(node.right)
        return value

# ═══════════════════════════════════════════
# 5. Chunked iterator
# ═══════════════════════════════════════════
class Chunked:
    """Yields fixed-size chunks from an iterable."""

    def __init__(self, iterable, size: int):
        self._it = iter(iterable)
        self.size = size
        self._done = False

    def __iter__(self):
        return self

    def __next__(self) -> list:
        if self._done:
            raise StopIteration
        chunk = []
        try:
            for _ in range(self.size):
                chunk.append(next(self._it))
        except StopIteration:
            self._done = True
        if not chunk:
            raise StopIteration
        return chunk

# ═══════════════════════════════════════════
# 6. Zip-lookahead iterator
# ═══════════════════════════════════════════
class PeekableIterator:
    """Iterator that lets you peek at the next value without consuming it."""

    _SENTINEL = object()

    def __init__(self, iterable):
        self._it = iter(iterable)
        self._peeked = self._SENTINEL

    def peek(self, default=_SENTINEL):
        if self._peeked is self._SENTINEL:
            try:
                self._peeked = next(self._it)
            except StopIteration:
                if default is self._SENTINEL:
                    raise
                return default
        return self._peeked

    def __iter__(self):
        return self

    def __next__(self):
        if self._peeked is not self._SENTINEL:
            value = self._peeked
            self._peeked = self._SENTINEL
            return value
        return next(self._it)

    def has_next(self) -> bool:
        try:
            self.peek()
            return True
        except StopIteration:
            return False

# ═══════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════
if __name__ == "__main__":
    print("=== CountUp ===")
    print(list(CountUp(0, 10, 2)))
    print(list(CountUp(10, 0, -3)))

    print("\n=== Fibonacci ===")
    fib = Fibonacci(limit=12)
    print(list(fib))
    fib.reset()
    print(list(fib))

    print("\n=== LinkedList ===")
    ll: LinkedList[int] = LinkedList()
    for v in [5, 1, 9, 3, 7]:
        ll.append(v)
    print(f"Forward:  {list(ll)}")
    print(f"Reversed: {list(reversed(ll))}")
    print(f"Contains 9: {9 in ll}, Contains 4: {4 in ll}")

    print("\n=== BST In-Order Iterator ===")
    root = BSTNode(5)
    root.left = BSTNode(3); root.right = BSTNode(8)
    root.left.left = BSTNode(1); root.left.right = BSTNode(4)
    root.right.left = BSTNode(7); root.right.right = BSTNode(9)
    print(list(InOrderIterator(root)))

    print("\n=== Chunked ===")
    for chunk in Chunked(range(11), 3):
        print(f"  {chunk}")

    print("\n=== PeekableIterator ===")
    pit = PeekableIterator([10, 20, 30, 40])
    print(f"Peek: {pit.peek()}")
    print(f"Next: {next(pit)}")
    print(f"Next (peek again): {pit.peek()}")
    print(f"Rest: {list(pit)}")
    print(f"Has next: {pit.has_next()}")
