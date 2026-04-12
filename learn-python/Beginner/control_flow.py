# Example: Control Flow
number = 10
if number > 0:
    print("Positive number")
else:
    print("Negative number")

for i in range(5):
    print(f"Iteration {i}")


# While loop example
i = 0
while i < 5:
    print(f"Iteration {i}")
    i += 1



# Example: Using break and continue
for i in range(10):
    if i == 5:
        break  # Exit the loop when i is 5
    if i % 2 == 0:
        continue  # Skip even numbers
    print(f"Current number: {i}")


# ternary operator example
age = 20
status = "Adult" if age >= 18 else "Minor"
print(f"Status: {status}")


# Example: Nested control flow
x = 10
if x > 30:
    if x % 2 == 0:
        print("Positive even number")
    else:
        print("Positive odd number")

# switch case example
def switch_case_example(value):
    print(f"Value: {value}")
    match value:
        case 1:
            return "One"
        case 2:
            return "Two"
        case 3:
            return "Three"
        case _:
            return "Other"

print(switch_case_example(2))
