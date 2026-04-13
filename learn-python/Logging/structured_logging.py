"""
Logging: Structured logging and log rotation.
"""
import logging
import logging.handlers
import json
import os
from datetime import datetime

# === Basic logging setup ===
print("=== Basic Logging ===")

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("myapp")

logger.debug("Debug message - detailed diagnostic")
logger.info("Info message - normal operation")
logger.warning("Warning - something unexpected")
logger.error("Error - operation failed")

# === Structured JSON Logging ===
print("\n=== Structured JSON Logging ===")

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        if record.exc_info and record.exc_info[0]:
            log_data["exception"] = self.formatException(record.exc_info)
        if hasattr(record, 'extra_data'):
            log_data["extra"] = record.extra_data
        return json.dumps(log_data)

json_logger = logging.getLogger("json_app")
json_logger.setLevel(logging.DEBUG)
json_logger.propagate = False

handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
json_logger.addHandler(handler)

json_logger.info("User logged in", extra={"extra_data": {"user_id": 123, "ip": "192.168.1.1"}})

# === Context-aware logging ===
print("\n=== Context Logging ===")

class ContextFilter(logging.Filter):
    def __init__(self, context=None):
        super().__init__()
        self.context = context or {}

    def filter(self, record):
        for key, value in self.context.items():
            setattr(record, key, value)
        return True

ctx_logger = logging.getLogger("context_app")
ctx_logger.setLevel(logging.DEBUG)
ctx_logger.propagate = False

ctx_handler = logging.StreamHandler()
ctx_handler.setFormatter(logging.Formatter('%(asctime)s [%(request_id)s] %(levelname)s: %(message)s'))
ctx_handler.addFilter(ContextFilter({"request_id": "req-abc123"}))
ctx_logger.addHandler(ctx_handler)

ctx_logger.info("Processing request")
ctx_logger.info("Database query completed")

# === Log levels and filtering ===
print("\n=== Custom Log Levels ===")

AUDIT = 25  # Between INFO (20) and WARNING (30)
logging.addLevelName(AUDIT, "AUDIT")

def audit(self, message, *args, **kwargs):
    if self.isEnabledFor(AUDIT):
        self._log(AUDIT, message, args, **kwargs)

logging.Logger.audit = audit

audit_logger = logging.getLogger("audit_app")
audit_logger.setLevel(logging.DEBUG)
audit_logger.propagate = False
audit_handler = logging.StreamHandler()
audit_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
audit_logger.addHandler(audit_handler)
audit_logger.audit("User admin performed action: delete_user(42)")

# === Performance logging ===
print("\n=== Performance Logging ===")

import time
import functools

def log_performance(logger):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                elapsed = time.perf_counter() - start
                logger.info(f"{func.__name__} completed in {elapsed:.4f}s")
                return result
            except Exception as e:
                elapsed = time.perf_counter() - start
                logger.error(f"{func.__name__} failed after {elapsed:.4f}s: {e}")
                raise
        return wrapper
    return decorator

perf_logger = logging.getLogger("perf")
perf_logger.setLevel(logging.DEBUG)
perf_logger.propagate = False
perf_handler = logging.StreamHandler()
perf_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
perf_logger.addHandler(perf_handler)

@log_performance(perf_logger)
def slow_operation():
    time.sleep(0.1)
    return "done"

slow_operation()
