# Example: Generators
def generate_numbers():
    for i in range(5):
        yield i

gen = generate_numbers()
for number in gen:
    print(number)
