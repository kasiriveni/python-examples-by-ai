# Example: File I/O
# Demonstrates reading and writing files in Python

# Writing to a file
with open("example.txt", "w") as file:
    file.write("Hello, AI Engineer!\n")

# Reading from a file
with open("example.txt", "r") as file:
    content = file.read()
    print("File Content:")
    print(content)
