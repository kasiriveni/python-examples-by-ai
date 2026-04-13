"""
Context Managers: Database transaction patterns and connection management.
"""
import contextlib
import sqlite3
import threading
from dataclasses import dataclass, field
from typing import Any, Iterator

# ═══════════════════════════════════════════
# 1. SQLite transaction context manager
# ═══════════════════════════════════════════
@contextlib.contextmanager
def transaction(conn: sqlite3.Connection) -> Iterator[sqlite3.Connection]:
    """Wrap a block in a DB transaction; rollback on exception."""
    try:
        yield conn
        conn.commit()
        print("  [DB] Transaction committed")
    except Exception as e:
        conn.rollback()
        print(f"  [DB] Rollback after: {e}")
        raise

@contextlib.contextmanager
def savepoint(conn: sqlite3.Connection, name: str = "sp1") -> Iterator:
    """Nested savepoint (nested transactions in SQLite)."""
    conn.execute(f"SAVEPOINT {name}")
    try:
        yield conn
        conn.execute(f"RELEASE SAVEPOINT {name}")
    except Exception:
        conn.execute(f"ROLLBACK TO SAVEPOINT {name}")
        raise

# ═══════════════════════════════════════════
# 2. Connection pool context manager
# ═══════════════════════════════════════════
class DatabaseConnectionPool:
    """Thread-safe connection pool with context manager support."""

    def __init__(self, db_path: str, max_connections: int = 5):
        self._db_path = db_path
        self._max = max_connections
        self._pool: list[sqlite3.Connection] = []
        self._in_use: set[int] = set()
        self._lock = threading.Lock()
        self._not_empty = threading.Condition(self._lock)

        # Pre-create connections
        for _ in range(max_connections):
            conn = sqlite3.connect(db_path, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            self._pool.append(conn)

    @contextlib.contextmanager
    def acquire(self) -> Iterator[sqlite3.Connection]:
        """Get a connection from the pool; return when done."""
        conn = self._checkout()
        try:
            yield conn
        finally:
            self._checkin(conn)

    def _checkout(self) -> sqlite3.Connection:
        with self._not_empty:
            while not self._pool:
                self._not_empty.wait(timeout=30)
                if not self._pool:
                    raise TimeoutError("No connections available in pool")
            conn = self._pool.pop()
            self._in_use.add(id(conn))
            return conn

    def _checkin(self, conn: sqlite3.Connection) -> None:
        with self._not_empty:
            self._in_use.discard(id(conn))
            self._pool.append(conn)
            self._not_empty.notify()

    def __enter__(self): return self
    def __exit__(self, *_): self.close()

    def close(self) -> None:
        for conn in self._pool:
            conn.close()
        self._pool.clear()

    @property
    def available(self) -> int:
        return len(self._pool)

    @property
    def in_use(self) -> int:
        return len(self._in_use)

# ═══════════════════════════════════════════
# 3. Repository pattern with context manager
# ═══════════════════════════════════════════
@dataclass
class User:
    id:    int | None
    name:  str
    email: str
    active: bool = True

class UserRepository:
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn
        self._setup()

    def _setup(self):
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id     INTEGER PRIMARY KEY AUTOINCREMENT,
                name   TEXT NOT NULL,
                email  TEXT NOT NULL UNIQUE,
                active INTEGER DEFAULT 1
            )
        """)

    def add(self, user: User) -> User:
        cur = self._conn.execute(
            "INSERT INTO users (name, email, active) VALUES (?,?,?)",
            (user.name, user.email, int(user.active))
        )
        return User(cur.lastrowid, user.name, user.email, user.active)

    def get(self, user_id: int) -> User | None:
        row = self._conn.execute(
            "SELECT id, name, email, active FROM users WHERE id=?", (user_id,)
        ).fetchone()
        if row:
            return User(row["id"], row["name"], row["email"], bool(row["active"]))
        return None

    def list_active(self) -> list[User]:
        rows = self._conn.execute(
            "SELECT id, name, email, active FROM users WHERE active=1"
        ).fetchall()
        return [User(r["id"], r["name"], r["email"], True) for r in rows]

    def deactivate(self, user_id: int) -> bool:
        cur = self._conn.execute(
            "UPDATE users SET active=0 WHERE id=?", (user_id,)
        )
        return cur.rowcount > 0

    def delete(self, user_id: int) -> bool:
        cur = self._conn.execute("DELETE FROM users WHERE id=?", (user_id,))
        return cur.rowcount > 0

# ═══════════════════════════════════════════
# 4. Unit of Work pattern
# ═══════════════════════════════════════════
class UnitOfWork:
    """Batch multiple DB operations under one transaction."""

    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn
        self._dirty: list[tuple[str, tuple]] = []
        self._committed = False

    def add_operation(self, sql: str, params: tuple = ()) -> "UnitOfWork":
        self._dirty.append((sql, params))
        return self

    def __enter__(self): return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            for sql, params in self._dirty:
                self._conn.execute(sql, params)
            self._conn.commit()
            self._committed = True
        else:
            self._conn.rollback()
        return False

    @property
    def committed(self) -> bool:
        return self._committed

# ═══════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════
if __name__ == "__main__":
    print("=== Transaction Context Manager ===")
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("CREATE TABLE accounts (id INTEGER PRIMARY KEY, balance REAL)")
    conn.execute("INSERT INTO accounts VALUES (1, 1000), (2, 500)")
    conn.commit()

    # Successful transaction
    with transaction(conn):
        conn.execute("UPDATE accounts SET balance=balance-200 WHERE id=1")
        conn.execute("UPDATE accounts SET balance=balance+200 WHERE id=2")
    row = conn.execute("SELECT balance FROM accounts WHERE id=1").fetchone()
    print(f"  Alice balance: {row[0]}")

    # Failed transaction (rollback)
    try:
        with transaction(conn):
            conn.execute("UPDATE accounts SET balance=balance-300 WHERE id=2")
            raise ValueError("Payment processor error!")
    except ValueError:
        pass
    row = conn.execute("SELECT balance FROM accounts WHERE id=2").fetchone()
    print(f"  Bob balance after rollback: {row[0]}")  # unchanged

    print("\n=== Repository Pattern ===")
    repo_conn = sqlite3.connect(":memory:")
    repo_conn.row_factory = sqlite3.Row
    repo = UserRepository(repo_conn)

    u1 = repo.add(User(None, "Alice", "alice@example.com"))
    u2 = repo.add(User(None, "Bob",   "bob@example.com"))
    u3 = repo.add(User(None, "Carol", "carol@example.com"))
    repo_conn.commit()

    print(f"  Added: {u1}, {u2}")
    active = repo.list_active()
    print(f"  Active users: {[u.name for u in active]}")

    repo.deactivate(u2.id)
    repo_conn.commit()
    active = repo.list_active()
    print(f"  After deactivate Bob: {[u.name for u in active]}")

    print("\n=== Unit of Work ===")
    uow_conn = sqlite3.connect(":memory:")
    uow_conn.execute("CREATE TABLE log (msg TEXT, ts TEXT)")
    uow_conn.commit()

    with UnitOfWork(uow_conn) as uow:
        uow.add_operation("INSERT INTO log VALUES (?,datetime('now'))", ("Started",))
        uow.add_operation("INSERT INTO log VALUES (?,datetime('now'))", ("Processing",))
        uow.add_operation("INSERT INTO log VALUES (?,datetime('now'))", ("Done",))
    print(f"  Unit of Work committed: {uow.committed}")
    rows = uow_conn.execute("SELECT msg FROM log").fetchall()
    print(f"  Log entries: {[r[0] for r in rows]}")

    print("\n=== Connection Pool ===")
    with DatabaseConnectionPool(":memory:", max_connections=3) as pool:
        print(f"  Available connections: {pool.available}")
        with pool.acquire() as c1:
            print(f"  After checkout: available={pool.available}, in_use={pool.in_use}")
            c1.execute("CREATE TABLE test (id INTEGER)")
        print(f"  After return:   available={pool.available}, in_use={pool.in_use}")
