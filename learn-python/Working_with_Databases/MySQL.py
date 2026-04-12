# MySQL: Relational Database

import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="user",
    password="password",
    database="exampledb"
)

cur = conn.cursor()

# Create a table
cur.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100), age INT)")

# Insert data
cur.execute("INSERT INTO users (name, age) VALUES (%s, %s)", ("Alice", 30))

# Query data
cur.execute("SELECT * FROM users")
for row in cur.fetchall():
    print(row)

conn.commit()
cur.close()
conn.close()
