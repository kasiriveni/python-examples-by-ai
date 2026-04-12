# Example: Itertools and Collections
# Demonstrates defaultdict, Counter, and deque

from collections import defaultdict, Counter, deque
from itertools import permutations, combinations

# defaultdict
word_count = defaultdict(int)
words = ["apple", "banana", "apple"]
for word in words:
    word_count[word] += 1
print("Word Count:", dict(word_count))

# Counter
counter = Counter(words)
print("Counter:", counter)

# deque
d = deque([1, 2, 3])
d.append(4)
d.appendleft(0)
print("Deque:", d)

# Itertools
print("Permutations:", list(permutations([1, 2, 3], 2)))
print("Combinations:", list(combinations([1, 2, 3], 2)))
