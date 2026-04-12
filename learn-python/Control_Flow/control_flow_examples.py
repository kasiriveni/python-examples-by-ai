# Control flow: if/elif/else, match-case (3.10+), short-circuit
x = 10
if x > 0:
    print("positive")
elif x == 0:
    print("zero")
else:
    print("negative")

# Short-circuit
a = None
b = 5
print(a or b)  # prints 5

# match-case (simple example)
try:
    match x:
        case 1:
            print("one")
        case 10:
            print("ten")
        case _:
            print("other")
except Exception:
    pass  # running on older Python will ignore match-case
