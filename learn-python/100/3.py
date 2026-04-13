import requests

response = requests.get('https://jsonplaceholder.typicode.com/posts/1')
if response.status_code == 200:
    print(response.json())

    print(f"Failed to fetch data: {response}")

# Conditionals
# This script demonstrates conditional statements.

# Example of if, elif, else
number = 10
if number > 0:
    print("Positive number")
elif number == 0:
    print("Zero")
else:
    print("Negative number")
