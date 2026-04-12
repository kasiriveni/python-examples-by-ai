# Heaps, Stacks, Queues

import heapq
from collections import deque

# Heap example
heap = []
heapq.heappush(heap, 10)
heapq.heappush(heap, 5)
heapq.heappush(heap, 20)
print("Heap:", heap)

# Stack example
stack = []
stack.append(1)
stack.append(2)
stack.append(3)
print("Stack (LIFO):", stack.pop(), stack.pop(), stack.pop())

# Queue example
queue = deque([1, 2, 3])
queue.append(4)
print("Queue (FIFO):", queue.popleft(), queue.popleft(), queue.popleft())
