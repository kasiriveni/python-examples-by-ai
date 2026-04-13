"""
Debugging and Logging: Structured logging, pdb patterns, and profiling.
"""
import logging
import logging.handlers
import json
import sys
import time
import cProfile
import pstats
import io
import traceback
import functools
from pathlib import Path
from typing import Callable

# ═══════════════════════════════════════════
# 1. Structured JSON logging
# ═══════════════════════════════════════════
class StructuredFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_obj = {
            "timestamp": self.formatTime(record),
            "level":     record.levelname,
            "logger":    record.name,
            "message":   record.getMessage(),
            "module":    record.module,
            "func":      record.funcName,
            "line":      record.lineno,
        }
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)
        if hasattr(record, "extra"):
            log_obj.update(record.extra)
        return json.dumps(log_obj)

def setup_logger(name: str,
                 level: int = logging.DEBUG,
                 json_output: bool = False,
                 file_path: str | None = None,
                 max_bytes: int = 10 * 1024 * 1024,
                 backup_count: int = 5) -> logging.Logger:
    """Create a production-ready logger."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.handlers.clear()

    # Console handler
    console = logging.StreamHandler(sys.stdout)
    if json_output:
        console.setFormatter(StructuredFormatter())
    else:
        fmt = logging.Formatter(
            "%(asctime)s | %(name)-20s | %(levelname)-8s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        console.setFormatter(fmt)
    logger.addHandler(console)

    # Rotating file handler
    if file_path:
        fh = logging.handlers.RotatingFileHandler(
            file_path, maxBytes=max_bytes, backupCount=backup_count
        )
        fh.setFormatter(StructuredFormatter())
        logger.addHandler(fh)

    return logger

# ═══════════════════════════════════════════
# 2. Contextual logging (extra fields)
# ═══════════════════════════════════════════
class RequestLogger(logging.LoggerAdapter):
    """Injects request_id and user_id into every log record."""

    def process(self, msg, kwargs):
        extra = kwargs.setdefault("extra", {})
        extra.update(self.extra)
        return msg, kwargs

def get_request_logger(request_id: str, user_id: str | None = None) -> logging.LoggerAdapter:
    base = logging.getLogger("app.request")
    return RequestLogger(base, {"request_id": request_id, "user_id": user_id})

# ═══════════════════════════════════════════
# 3. Logging decorators
# ═══════════════════════════════════════════
def log_calls(logger: logging.Logger | None = None, level: int = logging.DEBUG):
    """Log function entry, exit, and duration."""
    def decorator(fn: Callable):
        _logger = logger or logging.getLogger(fn.__module__)
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            _logger.log(level, "CALL  %s(%s)", fn.__name__,
                        ", ".join([repr(a) for a in args[:3]] +
                                  [f"{k}={v!r}" for k, v in list(kwargs.items())[:3]]))
            start = time.perf_counter()
            try:
                result = fn(*args, **kwargs)
                elapsed = (time.perf_counter() - start) * 1000
                _logger.log(level, "RETURN %s → %r (%.1fms)", fn.__name__, result, elapsed)
                return result
            except Exception as exc:
                elapsed = (time.perf_counter() - start) * 1000
                _logger.exception("RAISE  %s: %s (%.1fms)", fn.__name__, exc, elapsed)
                raise
        return wrapper
    return decorator

def log_exceptions(logger: logging.Logger | None = None, reraise: bool = True):
    """Catch and log exceptions; optionally suppress."""
    def decorator(fn: Callable):
        _logger = logger or logging.getLogger(fn.__module__)
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except Exception:
                _logger.exception("Unhandled exception in %s", fn.__name__)
                if reraise: raise
                return None
        return wrapper
    return decorator

# ═══════════════════════════════════════════
# 4. cProfile profiling helper
# ═══════════════════════════════════════════
def profile(fn: Callable = None, *, sort_by: str = "cumulative", top_n: int = 10):
    """Profile a function or use as decorator."""
    if fn is None:
        return lambda f: profile(f, sort_by=sort_by, top_n=top_n)

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        result = fn(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats(sort_by)
        ps.print_stats(top_n)
        print(s.getvalue())
        return result
    return wrapper

def profile_block(sort_by: str = "cumulative", top_n: int = 10):
    """Context manager for profiling a block."""
    import contextlib

    class _Profiler:
        def __enter__(self):
            self._pr = cProfile.Profile()
            self._pr.enable()
            return self
        def __exit__(self, *_):
            self._pr.disable()
            s = io.StringIO()
            pstats.Stats(self._pr, stream=s).sort_stats(sort_by).print_stats(top_n)
            print(s.getvalue())
    return _Profiler()

# ═══════════════════════════════════════════
# 5. Traceback helpers
# ═══════════════════════════════════════════
def format_exception_chain(exc: BaseException) -> str:
    """Walk the full exception chain and format it."""
    parts = []
    tb_lines = traceback.format_exception(type(exc), exc, exc.__traceback__)
    parts.append("".join(tb_lines))
    if exc.__cause__:
        parts.insert(0, format_exception_chain(exc.__cause__) + "\nAbove exception caused:\n")
    return "".join(parts)

def capture_traceback() -> str:
    """Capture current exception traceback as string."""
    return traceback.format_exc()

# ═══════════════════════════════════════════
# 6. Log levels and filtering
# ═══════════════════════════════════════════
LOGGING_CONFIG_DICT = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {"()": "your_module.StructuredFormatter"},
        "plain": {
            "format": "%(asctime)s %(name)s %(levelname)s %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "plain",
            "level": "INFO",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "app.log",
            "maxBytes": 10485760,
            "backupCount": 5,
            "formatter": "json",
        },
    },
    "loggers": {
        "app": {"handlers": ["console", "file"], "level": "DEBUG", "propagate": False},
        "app.db": {"level": "WARNING", "propagate": True},
    },
    "root": {"level": "WARNING", "handlers": ["console"]},
}

# ═══════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════
if __name__ == "__main__":
    print("=== Plain Logger ===")
    plain_log = setup_logger("demo.plain", level=logging.DEBUG)
    plain_log.debug("Debug message")
    plain_log.info("Server started on port %d", 8080)
    plain_log.warning("Cache miss rate %.1f%%", 42.5)

    print("\n=== JSON Logger ===")
    json_log = setup_logger("demo.json", level=logging.INFO, json_output=True)
    json_log.info("Request received", extra={"method": "GET", "path": "/api/users"})

    try:
        1 / 0
    except ZeroDivisionError:
        json_log.exception("Unexpected error")

    print("\n=== log_calls decorator ===")
    dbg_log = setup_logger("demo.calls")
    @log_calls(dbg_log)
    def compute(a: int, b: int) -> int:
        return a * b + a
    compute(3, 7)

    print("\n=== Profiling a block ===")
    with profile_block(top_n=5):
        data = sorted([i**2 % 1000 for i in range(50_000)])

    print("\n=== Traceback capture ===")
    try:
        raise ValueError("something bad")
    except ValueError:
        tb = capture_traceback()
        print(tb[:200])
