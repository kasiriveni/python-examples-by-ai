"""
Recursion examples in Python.
"""
import sys

# Set recursion limit awareness
print(f"Default recursion limit: {sys.getrecursionlimit()}")

# Factorial
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print(f"5! = {factorial(5)}")

# Fibonacci
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(f"fib(10) = {fibonacci(10)}")

# Tower of Hanoi
def hanoi(n, source='A', target='C', auxiliary='B'):
    if n == 1:
        print(f"  Move disk 1 from {source} to {target}")
        return
    hanoi(n - 1, source, auxiliary, target)
    print(f"  Move disk {n} from {source} to {target}")
    hanoi(n - 1, auxiliary, target, source)

print("\nTower of Hanoi (3 disks):")
hanoi(3)

# Binary search (recursive)
def binary_search(arr, target, low=0, high=None):
    if high is None:
        high = len(arr) - 1
    if low > high:
        return -1
    mid = (low + high) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search(arr, target, mid + 1, high)
    else:
        return binary_search(arr, target, low, mid - 1)

sorted_list = [1, 3, 5, 7, 9, 11, 13, 15]
print(f"\nBinary search for 7: index {binary_search(sorted_list, 7)}")

# Flatten nested list
def flatten(lst):
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

nested = [1, [2, [3, 4], 5], [6, 7], 8]
print(f"Flatten: {flatten(nested)}")

# Tree traversal using recursion
def tree_sum(tree):
    """Sum all values in a nested dict tree."""
    if isinstance(tree, (int, float)):
        return tree
    return sum(tree_sum(v) for v in tree.values())

tree = {"a": 1, "b": {"c": 2, "d": {"e": 3}}, "f": 4}
print(f"Tree sum: {tree_sum(tree)}")

# Tail recursion optimization (manual with accumulator)
def factorial_tail(n, accumulator=1):
    if n <= 1:
        return accumulator
    return factorial_tail(n - 1, accumulator * n)

print(f"5! (tail): {factorial_tail(5)}")
