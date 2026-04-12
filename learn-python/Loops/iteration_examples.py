# Loops & Iteration: for, while, enumerate, zip, loop-else
items = ['a','b','c']
for idx, val in enumerate(items):
    print(idx, val)

for i, j in zip(range(3), 'xyz'):
    print(i, j)

# loop-else
for i in range(3):
    if i == 5:
        break
else:
    print('completed loop without break')



#example break and continue
for i in range(5):
    if i == 2:
        continue
    if i == 4:
        break
    print(i)

# example of pass
for i in range(5):
    if i == 2:
        pass
    print(i)
