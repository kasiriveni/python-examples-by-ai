"""
Working with Databases: SQLite comprehensive examples.
"""
import sqlite3
import json
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Optional

# === Database connection manager ===
@contextmanager
def get_db(db_path=":memory:"):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

# === Repository pattern ===
@dataclass
class User:
    id: Optional[int] = None
    name: str = ""
    email: str = ""
    age: int = 0

class UserRepository:
    def __init__(self, conn):
        self.conn = conn
        self._create_table()

    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                age INTEGER DEFAULT 0
            )
        """)

    def create(self, user: User) -> User:
        cursor = self.conn.execute(
            "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
            (user.name, user.email, user.age)
        )
        user.id = cursor.lastrowid
        return user

    def find_by_id(self, user_id: int) -> Optional[User]:
        row = self.conn.execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        return User(**dict(row)) if row else None

    def find_all(self, limit=100, offset=0) -> list[User]:
        rows = self.conn.execute(
            "SELECT * FROM users LIMIT ? OFFSET ?", (limit, offset)
        ).fetchall()
        return [User(**dict(row)) for row in rows]

    def find_by_email(self, email: str) -> Optional[User]:
        row = self.conn.execute(
            "SELECT * FROM users WHERE email = ?", (email,)
        ).fetchone()
        return User(**dict(row)) if row else None

    def update(self, user: User) -> bool:
        cursor = self.conn.execute(
            "UPDATE users SET name = ?, email = ?, age = ? WHERE id = ?",
            (user.name, user.email, user.age, user.id)
        )
        return cursor.rowcount > 0

    def delete(self, user_id: int) -> bool:
        cursor = self.conn.execute(
            "DELETE FROM users WHERE id = ?", (user_id,)
        )
        return cursor.rowcount > 0

    def count(self) -> int:
        return self.conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]

    def search(self, query: str) -> list[User]:
        rows = self.conn.execute(
            "SELECT * FROM users WHERE name LIKE ? OR email LIKE ?",
            (f"%{query}%", f"%{query}%")
        ).fetchall()
        return [User(**dict(row)) for row in rows]

if __name__ == "__main__":
    with get_db() as conn:
        repo = UserRepository(conn)

        # Create users
        print("=== Create ===")
        users_data = [
            User(name="Alice", email="alice@test.com", age=30),
            User(name="Bob", email="bob@test.com", age=25),
            User(name="Charlie", email="charlie@test.com", age=35),
            User(name="Diana", email="diana@test.com", age=28),
        ]
        for u in users_data:
            repo.create(u)
        print(f"Created {repo.count()} users")

        # Read
        print("\n=== Read ===")
        user = repo.find_by_id(1)
        print(f"By ID: {user}")

        user = repo.find_by_email("bob@test.com")
        print(f"By email: {user}")

        all_users = repo.find_all()
        print(f"All users: {[u.name for u in all_users]}")

        # Update
        print("\n=== Update ===")
        alice = repo.find_by_id(1)
        alice.age = 31
        repo.update(alice)
        print(f"Updated Alice: {repo.find_by_id(1)}")

        # Search
        print("\n=== Search ===")
        results = repo.search("ali")
        print(f"Search 'ali': {[u.name for u in results]}")

        # Delete
        print("\n=== Delete ===")
        repo.delete(4)
        print(f"After delete: {repo.count()} users")

        # Aggregation
        print("\n=== Aggregation ===")
        row = conn.execute("SELECT AVG(age), MIN(age), MAX(age) FROM users").fetchone()
        print(f"Avg age: {row[0]:.1f}, Min: {row[1]}, Max: {row[2]}")
