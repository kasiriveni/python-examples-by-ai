# Comprehensions: list, dict, set, generator
nums = [1,2,3,4]
squares = [x*x for x in nums]
print(squares)

sq_set = {x*x for x in nums}
print(sq_set)

double_map = {x: x*2 for x in nums}
print(double_map)

gen = (x for x in range(5))
print(next(gen))