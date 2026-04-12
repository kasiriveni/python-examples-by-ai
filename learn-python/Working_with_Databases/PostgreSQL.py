# PostgreSQL: Relational Database

import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="exampledb",
    user="user",
    password="password",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

# Create a table
cur.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name VARCHAR(100), age INT)")

# Insert data
cur.execute("INSERT INTO users (name, age) VALUES (%s, %s)", ("Alice", 30))

# Query data
cur.execute("SELECT * FROM users")
for row in cur.fetchall():
    print(row)

conn.commit()
cur.close()
conn.close()
