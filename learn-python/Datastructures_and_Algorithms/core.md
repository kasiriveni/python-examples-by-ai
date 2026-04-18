# Core Python Concepts

## Core Themes
- Classic data structures and search techniques.
- Sorting, recursion, dynamic programming, and greedy methods.
- Graph traversal and algorithmic problem solving.

## Core Theme Examples
- Example 1: Binary search implementation on sorted array.
- Example 2: Fibonacci sequence using memoization for dynamic programming.
- Example 3: BFS traversal on adjacency-list graph representation.

## Files and Concepts
- Arrays_and_Linked_Lists.py: array versus linked-list operations, access patterns, insertion and deletion
- Binary_Search_Trees.py: BST insertion, traversal, binary search property
- Dynamic_Programming.py: memoization, Fibonacci caching, knapsack DP tables
- Greedy_Algorithms.py: greedy choice property, activity selection
- graph_algorithms.py: graph representation, BFS, DFS, weighted shortest-path thinking
- Graph_Data_Structures.py: adjacency lists, vertex neighbors, BFS and DFS traversal
- Hash_Tables.py: dictionary-style key-value storage, constant-time lookup ideas
- Heaps_Stacks_Queues.py: heapq usage, heap property, stack and queue patterns with deque
- Recursion.py: factorial, Fibonacci, recursive base cases
- Sorting_Algorithms.py: bubble sort, quick sort, partition logic, comparison sorting

## Core Example
This example combines recursion with binary search on sorted data.

```python
def binary_search(items, target):
	left, right = 0, len(items) - 1
	while left <= right:
		middle = (left + right) // 2
		if items[middle] == target:
			return middle
		if items[middle] < target:
			left = middle + 1
		else:
			right = middle - 1
	return -1

print(binary_search([2, 4, 6, 8], 6))
```
