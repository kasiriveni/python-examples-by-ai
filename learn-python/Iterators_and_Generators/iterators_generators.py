# Iterators & Generators
# Custom iterator
class CountUp:
    def __init__(self, n):
        self.i = 0
        self.n = n
    def __iter__(self):
        return self
    def __next__(self):
        if self.i < self.n:
            val = self.i
            self.i += 1
            return val
        raise StopIteration

for x in CountUp(3):
    print(x)

# Generator
def gen_numbers(n):
    for i in range(n):
        yield i

for g in gen_numbers(3):
    print('gen', g)
