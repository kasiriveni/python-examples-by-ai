# Example: Iterators and Generators
# Demonstrates how to use iterators and generators in Python

# Iterator
class MyIterator:
    def __init__(self, limit):
        self.limit = limit
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current < self.limit:
            self.current += 1
            return self.current
        else:
            raise StopIteration

# Using the iterator
for value in MyIterator(5):
    print(value)

# Generator
def my_generator(limit):
    for i in range(1, limit + 1):
        yield i

# Using the generator
for value in my_generator(5):
    print(value)