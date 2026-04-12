# Working with databases: sqlite3 example
import sqlite3

conn = sqlite3.connect(':memory:')
c = conn.cursor()
c.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)')
c.execute("INSERT INTO users (name) VALUES ('Alice')")
conn.commit()
for row in c.execute('SELECT * FROM users'):
    print(row)
conn.close()
