# comment in python
import math
import random
from datetime import datetime
import os
import sys

import hashlib

# print("hello world in python")
# print("the value of pi is", math.pi)

# print("a random number between 1 and 10 is", random.randint(1, 10))
# print("a random float between 0 and 1 is", random.random());
# print("a random choice from a list is", random.choice(["apple", "banana", "cherry"]))
# print("current date and time is", datetime.now())

# print("Python version is", sys.version)

# print("current working directory is", os.getcwd())

text = "hello".encode()
hash_obj = hashlib.md5(text)
print(hash_obj.hexdigest())
