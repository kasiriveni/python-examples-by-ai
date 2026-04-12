# Example: Context Managers
# Demonstrates how to use and create context managers in Python

# Using a built-in context manager
with open("example.txt", "w") as file:
    file.write("Hello, AI Engineer!")

# Creating a custom context manager
class MyContextManager:
    def __enter__(self):
        print("Entering the context")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Exiting the context")

with MyContextManager() as manager:
    print("Inside the context")
