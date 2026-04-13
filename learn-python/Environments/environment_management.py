"""
Environments: Managing Python environments and configuration.
"""
import os
import sys
import platform
from pathlib import Path

# === Environment Variables ===
print("=== Environment Variables ===")

# Reading
home = os.environ.get("HOME") or os.environ.get("USERPROFILE", "unknown")
path = os.environ.get("PATH", "")
print(f"Home: {home}")
print(f"PATH entries: {len(path.split(os.pathsep))}")

# Setting (for current process only)
os.environ["MY_APP_DEBUG"] = "true"
os.environ["MY_APP_PORT"] = "8080"
print(f"Debug: {os.environ['MY_APP_DEBUG']}")
print(f"Port: {os.environ['MY_APP_PORT']}")

# === .env file parser ===
def load_dotenv(filepath=".env"):
    """Simple .env file parser."""
    env_vars = {}
    try:
        with open(filepath) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    key, _, value = line.partition('=')
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    env_vars[key] = value
                    os.environ[key] = value
    except FileNotFoundError:
        pass
    return env_vars

# === Configuration Management ===
class AppConfig:
    """Configuration from environment with defaults and validation."""

    def __init__(self):
        self.debug = self._get_bool("APP_DEBUG", False)
        self.port = self._get_int("APP_PORT", 8000)
        self.host = os.environ.get("APP_HOST", "localhost")
        self.database_url = os.environ.get("DATABASE_URL", "sqlite:///db.sqlite3")
        self.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me")
        self.log_level = os.environ.get("LOG_LEVEL", "INFO").upper()

    @staticmethod
    def _get_bool(key, default=False):
        val = os.environ.get(key, str(default)).lower()
        return val in ("true", "1", "yes")

    @staticmethod
    def _get_int(key, default=0):
        try:
            return int(os.environ.get(key, default))
        except (ValueError, TypeError):
            return default

    def __repr__(self):
        return (f"AppConfig(debug={self.debug}, port={self.port}, "
                f"host='{self.host}', log_level='{self.log_level}')")

config = AppConfig()
print(f"\n{config}")

# === System Information ===
print("\n=== System Info ===")
print(f"Python: {sys.version}")
print(f"Platform: {platform.platform()}")
print(f"Architecture: {platform.machine()}")
print(f"Processor: {platform.processor()}")
print(f"In virtualenv: {sys.prefix != sys.base_prefix}")
print(f"Executable: {sys.executable}")

# === Path management ===
print("\n=== Important Paths ===")
print(f"Current dir: {Path.cwd()}")
print(f"Home dir: {Path.home()}")
print(f"Script dir: {Path(__file__).parent.resolve()}")
print(f"Site packages: {next(p for p in sys.path if 'site-packages' in p)}" if any('site-packages' in p for p in sys.path) else "")

# === Multi-environment config ===
print("\n=== Multi-Environment Config ===")

CONFIGS = {
    "development": {
        "debug": True,
        "database": "sqlite:///dev.db",
        "log_level": "DEBUG",
    },
    "testing": {
        "debug": True,
        "database": "sqlite:///:memory:",
        "log_level": "WARNING",
    },
    "production": {
        "debug": False,
        "database": os.environ.get("DATABASE_URL", "postgresql://localhost/prod"),
        "log_level": "ERROR",
    },
}

env = os.environ.get("APP_ENV", "development")
active_config = CONFIGS.get(env, CONFIGS["development"])
print(f"Environment: {env}")
for key, value in active_config.items():
    print(f"  {key}: {value}")
