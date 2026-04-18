# Core Python Concepts

## Core Themes
- Linear data structures such as stacks, queues, and linked lists.
- Tree structures and hash-based lookup patterns.
- Python collection utilities and custom implementations.

## Core Theme Examples
- Example 1: Stack and queue implementation with push, pop, enqueue, dequeue operations.
- Example 2: Binary search tree insertion and in-order traversal.
- Example 3: Counter and defaultdict for element frequency and nested grouping.

## Files and Concepts
- binary_tree.py: binary search trees, node structure, inorder, preorder, and postorder traversal
- binary_tree_example.py: tree insertion, traversal operations, recursive navigation
- data_structures_examples.py: lists, tuples, sets, dicts, unpacking, defaultdict, Counter
- hash_map.py: hash table implementation, collision chaining, load factor, resizing
- linked_list.py: node structure, append, prepend, insert, delete, search, iteration
- linked_list_example.py: linked-list basics, display, search, deletion
- queue_example.py: FIFO queue behavior, enqueue, dequeue, peek, empty checks
- stack_and_queue.py: stack LIFO behavior, queue FIFO behavior, priority queue with heapq
- stack_example.py: push, pop, peek, empty-state stack checks
- 1.py: introductory data-structure examples and basic operations
- 2.py: introductory data-structure examples and basic operations
- 3.py: introductory data-structure examples and basic operations
- moduel.py: module-level practice file and simple import-oriented examples
- mymodule.py: module-level practice file and simple import-oriented examples

## Core Example
This example builds a tiny stack with a class and a list.

```python
class Stack:
	def __init__(self):
		self.items = []

	def push(self, value):
		self.items.append(value)

	def pop(self):
		return self.items.pop() if self.items else None

stack = Stack()
stack.push(10)
print(stack.pop())
```
