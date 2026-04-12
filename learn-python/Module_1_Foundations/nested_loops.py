# Example: Control Flow with Nested Loops
# Demonstrates break and continue in nested loops

for i in range(1, 4):
    for j in range(1, 4):
        if i == j:
            continue  # Skip when i equals j
        print(f"i: {i}, j: {j}")

# Break example
for i in range(1, 4):
    for j in range(1, 4):
        if i * j > 4:
            break  # Exit inner loop
        print(f"i: {i}, j: {j}")
