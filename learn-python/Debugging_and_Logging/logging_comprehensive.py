"""
Logging module comprehensive examples.
"""
import logging
import logging.handlers
import sys
import os
import tempfile

# === Basic logging ===
print("=== Basic Logging ===")
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger("myapp")
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")

# === Structured logging with extra fields ===
print("\n=== Structured Logging ===")
logger.info("User action", extra={"user": "alice", "action": "login"})

# === Logging exceptions ===
print("\n=== Exception Logging ===")
try:
    result = 1 / 0
except ZeroDivisionError:
    logger.exception("An error occurred")

# === Custom logger with multiple handlers ===
print("\n=== Custom Logger ===")

def setup_logger(name, log_file=None, level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.handlers.clear()

    # Console handler
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    console_format = logging.Formatter('%(name)s [%(levelname)s]: %(message)s')
    console.setFormatter(console_format)
    logger.addHandler(console)

    # File handler
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(name)s (%(filename)s:%(lineno)d): %(message)s'
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)

    return logger

tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.log', delete=False)
app_logger = setup_logger("myapp.custom", tmp.name)
app_logger.info("Application started")
app_logger.debug("Debug details (file only)")
app_logger.warning("Low disk space")

# Read the log file
print(f"\nLog file contents:")
with open(tmp.name, 'r') as f:
    for line in f:
        print(f"  {line.rstrip()}")

os.unlink(tmp.name)

# === Log filters ===
print("\n=== Log Filters ===")

class SensitiveDataFilter(logging.Filter):
    def filter(self, record):
        if hasattr(record, 'msg') and isinstance(record.msg, str):
            record.msg = record.msg.replace("password", "****")
        return True

filtered_logger = logging.getLogger("filtered")
filtered_logger.addHandler(logging.StreamHandler())
filtered_logger.addFilter(SensitiveDataFilter())
filtered_logger.warning("User sent password in request")

# === Context logging ===
print("\n=== Context Logging ===")

class RequestContext:
    def __init__(self, request_id):
        self.request_id = request_id

    def __enter__(self):
        self._old_factory = logging.getLogRecordFactory()
        rid = self.request_id
        old_factory = self._old_factory
        def record_factory(*args, **kwargs):
            record = old_factory(*args, **kwargs)
            record.request_id = rid
            return record
        logging.setLogRecordFactory(record_factory)
        return self

    def __exit__(self, *args):
        logging.setLogRecordFactory(self._old_factory)

ctx_logger = logging.getLogger("context")
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('[%(request_id)s] %(message)s'))
ctx_logger.addHandler(handler)

with RequestContext("req-123"):
    ctx_logger.info("Processing request")
