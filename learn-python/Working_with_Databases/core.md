# Core Python Concepts

## Core Themes
- SQL and NoSQL data-access patterns.
- ORM usage, driver-based queries, and transactions.
- Async database access and persistence-layer design.

## Core Theme Examples
- Example 1: Execute SQL queries and iterate over result rows.
- Example 2: Define ORM models and use query builders.
- Example 3: Execute async queries with await and async sessions.

## Files and Concepts
- db_examples.py: sqlite3 CRUD, in-memory databases, connection usage
- Django_ORM.py: Django models, migrations, queryset patterns
- Elasticsearch.py: document indexing, search queries, query DSL
- MongoDB.py: PyMongo clients, collection operations, document queries
- MySQL.py: mysql connector usage, SQL execution, connection management
- Peewee.py: lightweight ORM models, query construction
- PostgreSQL.py: psycopg2 connections, transactions, cursor operations
- Redis.py: Redis client use, caching, key-value operations
- SQLAlchemy.py: declarative models, sessions, ORM relationships
- sqlite_comprehensive.py: repository pattern, foreign keys, context-managed SQLite access
- Tortoise_ORM.py: async ORM models, await-based queries, schema generation

## Core Example
This example creates a SQLite table and reads rows back safely.

```python
import sqlite3

connection = sqlite3.connect(":memory:")
cursor = connection.cursor()
cursor.execute("CREATE TABLE users (name TEXT)")
cursor.executemany("INSERT INTO users VALUES (?)", [("Alice",), ("Bob",)])
cursor.execute("SELECT name FROM users")
print(cursor.fetchall())
connection.close()
```
