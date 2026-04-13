"""
Deployment: Environment-specific configuration management.
"""
import os
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

# ═══════════════════════════════════════════
# 1. Environment enum
# ═══════════════════════════════════════════
class Environment(str, Enum):
    DEVELOPMENT = "development"
    TESTING     = "testing"
    STAGING     = "staging"
    PRODUCTION  = "production"

    @staticmethod
    def current() -> "Environment":
        env = os.environ.get("APP_ENV", "development").lower()
        try:
            return Environment(env)
        except ValueError:
            return Environment.DEVELOPMENT

# ═══════════════════════════════════════════
# 2. Hierarchical config
# ═══════════════════════════════════════════
@dataclass
class DatabaseConfig:
    host: str = "localhost"
    port: int = 5432
    name: str = "app"
    user: str = "postgres"
    password: str = ""
    pool_size: int = 5
    max_overflow: int = 10
    pool_timeout: int = 30
    ssl: bool = False

    @property
    def url(self) -> str:
        scheme = "postgresql+asyncpg"
        return f"{scheme}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

@dataclass
class RedisConfig:
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: str = ""
    max_connections: int = 20
    socket_timeout: int = 5

    @property
    def url(self) -> str:
        auth = f":{self.password}@" if self.password else ""
        return f"redis://{auth}{self.host}:{self.port}/{self.db}"

@dataclass
class AppConfig:
    env: Environment = Environment.DEVELOPMENT
    debug: bool = True
    secret_key: str = "change-me-in-production"
    allowed_hosts: list[str] = field(default_factory=lambda: ["localhost"])
    cors_origins: list[str] = field(default_factory=list)

    # Sub-configs
    db: DatabaseConfig = field(default_factory=DatabaseConfig)
    redis: RedisConfig = field(default_factory=RedisConfig)

    # Feature flags
    features: dict[str, bool] = field(default_factory=dict)

    # Limits
    max_upload_mb: int = 10
    rate_limit_per_min: int = 60
    session_timeout_mins: int = 30

# ═══════════════════════════════════════════
# 3. Config factory per environment
# ═══════════════════════════════════════════
def make_config(env: Environment) -> AppConfig:
    """Return the appropriate config for the given environment."""

    if env == Environment.DEVELOPMENT:
        return AppConfig(
            env=env,
            debug=True,
            secret_key="dev-secret-key-not-for-production",
            allowed_hosts=["localhost", "127.0.0.1"],
            cors_origins=["http://localhost:3000", "http://localhost:5173"],
            db=DatabaseConfig(name="app_dev"),
            redis=RedisConfig(db=1),
            features={"new_ui": True, "beta_api": True},
            rate_limit_per_min=1000,
        )

    elif env == Environment.TESTING:
        return AppConfig(
            env=env,
            debug=True,
            secret_key="test-secret-key",
            allowed_hosts=["testserver"],
            db=DatabaseConfig(name="app_test"),
            redis=RedisConfig(db=15),
            features={"new_ui": True, "beta_api": True},
            rate_limit_per_min=10000,
            session_timeout_mins=5,
        )

    elif env == Environment.STAGING:
        return AppConfig(
            env=env,
            debug=False,
            secret_key=os.environ.get("SECRET_KEY", "staging-secret"),
            allowed_hosts=["staging.example.com"],
            cors_origins=["https://staging.example.com"],
            db=DatabaseConfig(
                host=os.environ.get("DB_HOST", "db.staging"),
                password=os.environ.get("DB_PASSWORD", ""),
                ssl=True, pool_size=10,
            ),
            redis=RedisConfig(
                host=os.environ.get("REDIS_HOST", "redis.staging"),
            ),
            features={"new_ui": True, "beta_api": False},
        )

    else:  # PRODUCTION
        required = ["SECRET_KEY", "DB_HOST", "DB_PASSWORD"]
        missing = [k for k in required if not os.environ.get(k)]
        if missing:
            # In a real app you'd raise here; we just warn for demo purposes
            print(f"WARNING: Missing production env vars: {missing}")

        return AppConfig(
            env=env,
            debug=False,
            secret_key=os.environ.get("SECRET_KEY", "REPLACE_IN_PROD"),
            allowed_hosts=os.environ.get("ALLOWED_HOSTS", "example.com").split(","),
            cors_origins=os.environ.get("CORS_ORIGINS", "").split(","),
            db=DatabaseConfig(
                host=os.environ.get("DB_HOST", "db"),
                name=os.environ.get("DB_NAME", "app"),
                user=os.environ.get("DB_USER", "postgres"),
                password=os.environ.get("DB_PASSWORD", ""),
                pool_size=20, max_overflow=40, ssl=True,
            ),
            redis=RedisConfig(
                host=os.environ.get("REDIS_HOST", "redis"),
                password=os.environ.get("REDIS_PASSWORD", ""),
                max_connections=50,
            ),
            features={"new_ui": False, "beta_api": False},
            rate_limit_per_min=60,
        )

# ═══════════════════════════════════════════
# 4. Config validation
# ═══════════════════════════════════════════
class ConfigError(Exception): pass

def validate_config(config: AppConfig) -> list[str]:
    """Return list of validation errors."""
    errors = []

    if config.env == Environment.PRODUCTION:
        if config.debug:
            errors.append("debug must be False in production")
        if "change-me" in config.secret_key or len(config.secret_key) < 32:
            errors.append("secret_key too weak or not set for production")
        if not config.allowed_hosts or "*" in config.allowed_hosts:
            errors.append("allowed_hosts must be specific in production")
        if not config.db.ssl:
            errors.append("database SSL should be enabled in production")

    return errors

# ═══════════════════════════════════════════
# 5. Config serialization (safe — no secrets in output)
# ═══════════════════════════════════════════
REDACT = {"password", "secret_key", "token"}

def config_to_dict(config: AppConfig) -> dict:
    def _process(obj):
        if isinstance(obj, (str, int, float, bool, type(None))):
            return obj
        if isinstance(obj, Enum):
            return obj.value
        if isinstance(obj, list):
            return [_process(i) for i in obj]
        if isinstance(obj, dict):
            return {k: "***" if k in REDACT else _process(v) for k, v in obj.items()}
        if hasattr(obj, "__dataclass_fields__"):
            return {
                k: "***" if k in REDACT else _process(getattr(obj, k))
                for k in obj.__dataclass_fields__
            }
        return str(obj)
    return _process(config)

if __name__ == "__main__":
    print("=== Configuration by Environment ===\n")

    for env in Environment:
        config = make_config(env)
        errors = validate_config(config)

        print(f"--- {env.value.upper()} ---")
        safe = config_to_dict(config)
        print(f"  debug:        {safe['debug']}")
        print(f"  secret_key:   {safe['secret_key']}")
        print(f"  db url:       {config.db.url.split('@')[0]}@***  (password redacted)")
        print(f"  redis url:    {config.redis.url}")
        print(f"  features:     {safe['features']}")
        print(f"  rate limit:   {safe['rate_limit_per_min']}/min")
        if errors:
            print(f"  ⚠ Issues: {errors}")
        print()

    print("=== Current Environment ===")
    current_env = Environment.current()
    print(f"APP_ENV={os.environ.get('APP_ENV', 'not set')} → {current_env.value}")
