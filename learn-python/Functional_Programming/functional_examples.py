# Functional programming: map, filter, reduce, functools
from functools import reduce, partial

nums = [1,2,3,4]
print(list(map(lambda x: x*2, nums)))
print(list(filter(lambda x: x%2==0, nums)))
print(reduce(lambda a,b: a+b, nums))

add5 = partial(lambda a,b: a+b, 5)
print(add5(10))
