"""
Data Structures: Stack and Queue implementations.
"""

# === Stack (LIFO) ===
class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("Peek from empty stack")
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)

    def __repr__(self):
        return f"Stack({self._items})"

# === Queue (FIFO) ===
from collections import deque

class Queue:
    def __init__(self):
        self._items = deque()

    def enqueue(self, item):
        self._items.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Dequeue from empty queue")
        return self._items.popleft()

    def peek(self):
        if self.is_empty():
            raise IndexError("Peek from empty queue")
        return self._items[0]

    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)

    def __repr__(self):
        return f"Queue({list(self._items)})"

# === Priority Queue ===
import heapq

class PriorityQueue:
    def __init__(self):
        self._heap = []
        self._counter = 0

    def push(self, item, priority):
        heapq.heappush(self._heap, (priority, self._counter, item))
        self._counter += 1

    def pop(self):
        if self.is_empty():
            raise IndexError("Pop from empty priority queue")
        priority, _, item = heapq.heappop(self._heap)
        return item, priority

    def peek(self):
        if self.is_empty():
            raise IndexError("Peek from empty priority queue")
        return self._heap[0][2], self._heap[0][0]

    def is_empty(self):
        return len(self._heap) == 0

    def __len__(self):
        return len(self._heap)

# === Applications ===

# Balanced parentheses checker
def is_balanced(expression):
    stack = Stack()
    pairs = {'(': ')', '[': ']', '{': '}'}
    for char in expression:
        if char in pairs:
            stack.push(char)
        elif char in pairs.values():
            if stack.is_empty():
                return False
            opening = stack.pop()
            if pairs[opening] != char:
                return False
    return stack.is_empty()

# Reverse Polish Notation calculator
def eval_rpn(tokens):
    stack = Stack()
    ops = {'+': lambda a, b: a + b, '-': lambda a, b: a - b,
           '*': lambda a, b: a * b, '/': lambda a, b: int(a / b)}
    for token in tokens:
        if token in ops:
            b, a = stack.pop(), stack.pop()
            stack.push(ops[token](a, b))
        else:
            stack.push(int(token))
    return stack.pop()

if __name__ == "__main__":
    # Stack
    print("=== Stack ===")
    s = Stack()
    for x in [1, 2, 3, 4, 5]:
        s.push(x)
    print(f"Stack: {s}")
    print(f"Pop: {s.pop()}, Peek: {s.peek()}")

    # Queue
    print("\n=== Queue ===")
    q = Queue()
    for x in ["first", "second", "third"]:
        q.enqueue(x)
    print(f"Queue: {q}")
    print(f"Dequeue: {q.dequeue()}")

    # Priority Queue
    print("\n=== Priority Queue ===")
    pq = PriorityQueue()
    tasks = [("Low priority", 3), ("High priority", 1), ("Medium priority", 2)]
    for task, priority in tasks:
        pq.push(task, priority)
    while not pq.is_empty():
        item, priority = pq.pop()
        print(f"  [{priority}] {item}")

    # Applications
    print("\n=== Balanced Parentheses ===")
    expressions = ["(()[]{})", "(()", "({[]})", "([)]"]
    for expr in expressions:
        print(f"  '{expr}': {is_balanced(expr)}")

    print("\n=== RPN Calculator ===")
    tokens = ["3", "4", "+", "2", "*", "7", "/"]
    print(f"  {' '.join(tokens)} = {eval_rpn(tokens)}")
