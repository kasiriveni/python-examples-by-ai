# map, filter, reduce

from functools import reduce

# map example
numbers = [1, 2, 3, 4]
squared = list(map(lambda x: x ** 2, numbers))
print("Squared:", squared)

# filter example
even = list(filter(lambda x: x % 2 == 0, numbers))
print("Even:", even)

# reduce example
product = reduce(lambda x, y: x * y, numbers)
print("Product:", product)
