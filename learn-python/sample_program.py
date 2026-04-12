# 1. Basics
print("Welcome to the Python Topics Demonstration!")
name = "Python Learner"
age = 25
print(f"Hello, {name}! You are {age} years old.")

# 2. Data Structures
numbers = [1, 2, 3, 4, 5]
print("Numbers List:", numbers)

# 3. Functions
def greet_user(name, *args, **kwargs):
    print(f"Hello, {name}!")
    print("Additional Arguments:", args)
    print("Keyword Arguments:", kwargs)

greet_user("Alice", "Python", level="Beginner")

# 4. OOP
class Animal:
    def speak(self):
        return "I make a sound"

class Dog(Animal):
    def speak(self):
        return "Woof!"

dog = Dog()
print("Dog says:", dog.speak())

# 5. File Handling
with open("sample.txt", "w") as file:
    file.write("Hello, File Handling!")

with open("sample.txt", "r") as file:
    content = file.read()
    print("File Content:", content)

# 6. Concurrency
import threading

def print_numbers():
    for i in range(5):
        print(f"Thread: {i}")

thread = threading.Thread(target=print_numbers)
thread.start()
thread.join()

# 7. Database Interaction
import sqlite3

connection = sqlite3.connect("sample.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
cursor.execute("INSERT INTO users (name) VALUES (?)", ("Alice",))
connection.commit()

cursor.execute("SELECT * FROM users")
print("Database Content:", cursor.fetchall())
connection.close()

# 8. Web Development
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to the Flask App!"

if __name__ == "__main__":
    app.run(debug=True)
