"""
Python Standard Library highlights.
"""
import os
import sys
import math
import random
import hashlib
import itertools
import collections
import functools
import textwrap
import statistics
import string

# === os module ===
print("=== os ===")
print(f"CWD: {os.getcwd()}")
print(f"Platform: {sys.platform}")
print(f"Python version: {sys.version}")
print(f"Environment HOME: {os.environ.get('HOME', os.environ.get('USERPROFILE', 'N/A'))}")

# === math module ===
print("\n=== math ===")
print(f"pi: {math.pi}")
print(f"e: {math.e}")
print(f"ceil(4.2): {math.ceil(4.2)}")
print(f"floor(4.8): {math.floor(4.8)}")
print(f"sqrt(144): {math.sqrt(144)}")
print(f"log2(1024): {math.log2(1024)}")
print(f"gcd(48, 18): {math.gcd(48, 18)}")
print(f"factorial(10): {math.factorial(10)}")
print(f"comb(10, 3): {math.comb(10, 3)}")
print(f"perm(10, 3): {math.perm(10, 3)}")

# === random module ===
print("\n=== random ===")
random.seed(42)
print(f"randint(1,100): {random.randint(1, 100)}")
print(f"random(): {random.random():.4f}")
print(f"choice(['a','b','c']): {random.choice(['a', 'b', 'c'])}")
print(f"sample(range(100), 5): {random.sample(range(100), 5)}")
items = [1, 2, 3, 4, 5]
random.shuffle(items)
print(f"shuffled: {items}")

# === hashlib ===
print("\n=== hashlib ===")
text = "Hello, World!"
print(f"MD5: {hashlib.md5(text.encode()).hexdigest()}")
print(f"SHA256: {hashlib.sha256(text.encode()).hexdigest()}")

# === collections ===
print("\n=== collections ===")
# Counter
words = "the quick brown fox jumps over the lazy dog the fox".split()
word_count = collections.Counter(words)
print(f"Most common: {word_count.most_common(3)}")

# deque
dq = collections.deque(maxlen=5)
for i in range(7):
    dq.append(i)
print(f"Deque (maxlen=5): {list(dq)}")

# defaultdict
graph = collections.defaultdict(list)
edges = [(1, 2), (1, 3), (2, 3), (3, 4)]
for u, v in edges:
    graph[u].append(v)
print(f"Graph: {dict(graph)}")

# === itertools ===
print("\n=== itertools ===")
print(f"product('AB','12'): {list(itertools.product('AB', '12'))}")
print(f"combinations('ABCD',2): {list(itertools.combinations('ABCD', 2))}")
print(f"chain([1,2],[3,4]): {list(itertools.chain([1,2], [3,4]))}")
print(f"islice(count(),5): {list(itertools.islice(itertools.count(10), 5))}")

# === statistics ===
print("\n=== statistics ===")
data = [2, 4, 6, 8, 10, 12, 14]
print(f"mean: {statistics.mean(data)}")
print(f"median: {statistics.median(data)}")
print(f"stdev: {statistics.stdev(data):.2f}")
print(f"variance: {statistics.variance(data):.2f}")

# === textwrap ===
print("\n=== textwrap ===")
long_text = "This is a very long text that needs to be wrapped to fit within a specific width for better readability."
print(textwrap.fill(long_text, width=40))

# === string ===
print(f"\n=== string ===")
print(f"ascii_letters: {string.ascii_letters[:10]}...")
print(f"digits: {string.digits}")
print(f"punctuation: {string.punctuation}")
