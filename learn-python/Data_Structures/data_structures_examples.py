# Data structures: list, tuple, set, dict, collections
from collections import defaultdict, Counter

lst = [1,2,3]
print(lst[::-1])  # advanced list ops

t = (1,2)
a, b = t  # unpackingclear
print(a,b)

s = set([1,2,2])
print(s)

d = {'a':1, 'b':2}
print(d.get('c', 0))

dd = defaultdict(list)
dd['x'].append(1)
print(dd)

cnt = Counter([1,1,2,3])
print(cnt)
