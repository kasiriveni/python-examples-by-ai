# Example: Working with Databases
import sqlite3

connection = sqlite3.connect("example.db")
cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
cursor.execute("INSERT INTO users (name) VALUES ('Alice')")
connection.commit()

cursor.execute("SELECT * FROM users")
print(cursor.fetchall())

connection.close()
