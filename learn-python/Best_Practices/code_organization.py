"""
Best practices: Code organization and project structure.
"""

# === 1. Project structure ===
PROJECT_STRUCTURE = """
myproject/
├── src/
│   └── myproject/
│       ├── __init__.py
│       ├── main.py           # Entry point
│       ├── config.py          # Configuration
│       ├── models/            # Data models
│       │   ├── __init__.py
│       │   ├── user.py
│       │   └── product.py
│       ├── services/          # Business logic
│       │   ├── __init__.py
│       │   ├── user_service.py
│       │   └── product_service.py
│       ├── api/               # API layer
│       │   ├── __init__.py
│       │   ├── routes.py
│       │   └── middleware.py
│       └── utils/             # Utilities
│           ├── __init__.py
│           └── helpers.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # Shared fixtures
│   ├── test_user.py
│   └── test_product.py
├── docs/
├── pyproject.toml            # Project config
├── README.md
└── .gitignore
"""

# === 2. Configuration management ===
from dataclasses import dataclass, field
import os

@dataclass
class DatabaseConfig:
    host: str = "localhost"
    port: int = 5432
    name: str = "mydb"
    user: str = "admin"

    @classmethod
    def from_env(cls):
        return cls(
            host=os.environ.get("DB_HOST", "localhost"),
            port=int(os.environ.get("DB_PORT", "5432")),
            name=os.environ.get("DB_NAME", "mydb"),
            user=os.environ.get("DB_USER", "admin"),
        )

@dataclass
class AppConfig:
    debug: bool = False
    db: DatabaseConfig = field(default_factory=DatabaseConfig)
    log_level: str = "INFO"

# === 3. Dependency injection ===
from abc import ABC, abstractmethod

class Repository(ABC):
    @abstractmethod
    def find(self, id):
        pass

    @abstractmethod
    def save(self, entity):
        pass

class InMemoryRepository(Repository):
    def __init__(self):
        self._store = {}

    def find(self, id):
        return self._store.get(id)

    def save(self, entity):
        self._store[entity["id"]] = entity
        return entity

class UserService:
    def __init__(self, repo: Repository):
        self.repo = repo  # injected dependency

    def get_user(self, user_id):
        user = self.repo.find(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        return user

    def create_user(self, name, email):
        user = {"id": len(self.repo._store) + 1, "name": name, "email": email}
        return self.repo.save(user)

# === 4. Constants module ===
class HttpStatus:
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    NOT_FOUND = 404
    INTERNAL_ERROR = 500

# === Demo ===
if __name__ == "__main__":
    print("=== Project Structure ===")
    print(PROJECT_STRUCTURE)

    # Dependency injection
    print("=== Dependency Injection ===")
    repo = InMemoryRepository()
    service = UserService(repo)

    user = service.create_user("Alice", "alice@example.com")
    print(f"Created: {user}")

    found = service.get_user(1)
    print(f"Found: {found}")

    # Config
    print("\n=== Config ===")
    config = AppConfig(debug=True)
    print(f"Config: debug={config.debug}, db.host={config.db.host}")
