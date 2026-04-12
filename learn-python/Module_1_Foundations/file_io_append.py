# Example: File I/O - Appending to a File
# Demonstrates how to append to a file and read line by line

# Append to a file
with open("example.txt", "a") as file:
    file.write("Appending a new line.\n")

# Read line by line
with open("example.txt", "r") as file:
    for line in file:
        print(line.strip())
