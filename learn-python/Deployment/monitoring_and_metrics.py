"""
Deployment: Monitoring, metrics collection, and structured logging.
"""
import time
import threading
import statistics
import json
import logging
import sys
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Callable

# ═══════════════════════════════════════════
# 1. Structured logging
# ═══════════════════════════════════════════
class StructuredFormatter(logging.Formatter):
    """Emit log records as JSON for log aggregation systems."""

    def format(self, record: logging.LogRecord) -> str:
        doc = {
            "timestamp":  self.formatTime(record, "%Y-%m-%dT%H:%M:%S.%f"),
            "level":      record.levelname,
            "logger":     record.name,
            "message":    record.getMessage(),
            "module":     record.module,
            "line":       record.lineno,
        }
        if record.exc_info:
            doc["exception"] = self.formatException(record.exc_info)
        # Include any extra kwargs passed as 'extra=...'
        for k, v in record.__dict__.items():
            if k not in logging.LogRecord("", 0, "", 0, "", (), None).__dict__:
                doc[k] = v
        return json.dumps(doc)

def get_logger(name: str, json_mode: bool = False) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        if json_mode:
            handler.setFormatter(StructuredFormatter())
        else:
            handler.setFormatter(logging.Formatter(
                "%(asctime)s %(levelname)-8s %(name)s: %(message)s",
                datefmt="%H:%M:%S",
            ))
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
    return logger

# ═══════════════════════════════════════════
# 2. Metrics collector
# ═══════════════════════════════════════════
@dataclass
class Histogram:
    """Rolling histogram of observed values."""
    _values: list = field(default_factory=list)
    max_samples: int = 10_000

    def observe(self, value: float) -> None:
        if len(self._values) >= self.max_samples:
            self._values.pop(0)
        self._values.append(value)

    def summary(self) -> dict:
        if not self._values:
            return {"count": 0}
        v = sorted(self._values)
        n = len(v)
        return {
            "count": n,
            "min": v[0],
            "max": v[-1],
            "mean": statistics.mean(v),
            "p50": v[int(n * 0.50)],
            "p95": v[int(n * 0.95)],
            "p99": v[int(n * 0.99)],
        }

class MetricsRegistry:
    """Thread-safe metrics registry (Prometheus-like)."""

    def __init__(self):
        self._lock = threading.Lock()
        self._counters:   dict[str, float] = defaultdict(float)
        self._gauges:     dict[str, float] = defaultdict(float)
        self._histograms: dict[str, Histogram] = defaultdict(Histogram)

    def counter_inc(self, name: str, value: float = 1, **labels) -> None:
        key = self._key(name, labels)
        with self._lock:
            self._counters[key] += value

    def gauge_set(self, name: str, value: float, **labels) -> None:
        key = self._key(name, labels)
        with self._lock:
            self._gauges[key] = value

    def histogram_observe(self, name: str, value: float, **labels) -> None:
        key = self._key(name, labels)
        with self._lock:
            self._histograms[key].observe(value)

    def snapshot(self) -> dict:
        with self._lock:
            return {
                "counters":   dict(self._counters),
                "gauges":     dict(self._gauges),
                "histograms": {k: v.summary() for k, v in self._histograms.items()},
            }

    @staticmethod
    def _key(name: str, labels: dict) -> str:
        if not labels:
            return name
        parts = ",".join(f"{k}={v}" for k, v in sorted(labels.items()))
        return f"{name}{{{parts}}}"

# ═══════════════════════════════════════════
# 3. Timing decorator / context manager
# ═══════════════════════════════════════════
registry = MetricsRegistry()

def timed(name: str):
    """Decorator that records function latency to the registry."""
    def decorator(fn: Callable) -> Callable:
        import functools
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            status = "ok"
            try:
                result = fn(*args, **kwargs)
                return result
            except Exception:
                status = "error"
                raise
            finally:
                elapsed_ms = (time.perf_counter() - start) * 1000
                registry.histogram_observe(f"{name}_duration_ms", elapsed_ms, status=status)
                registry.counter_inc(f"{name}_calls_total", status=status)
        return wrapper
    return decorator

import contextlib

@contextlib.contextmanager
def measure(name: str):
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = (time.perf_counter() - start) * 1000
        registry.histogram_observe(f"{name}_ms", elapsed)

# ═══════════════════════════════════════════
# 4. Rate limiter (token bucket)
# ═══════════════════════════════════════════
class TokenBucketRateLimiter:
    def __init__(self, rate: float, burst: float):
        """rate = tokens per second, burst = max bucket size."""
        self.rate  = rate
        self.burst = burst
        self._tokens = burst
        self._last   = time.monotonic()
        self._lock   = threading.Lock()

    def consume(self, tokens: float = 1.0) -> bool:
        """Return True if allowed, False if rate-limited."""
        with self._lock:
            now = time.monotonic()
            self._tokens = min(self.burst,
                               self._tokens + (now - self._last) * self.rate)
            self._last = now
            if self._tokens >= tokens:
                self._tokens -= tokens
                return True
            return False

    def __repr__(self):
        return f"TokenBucket(rate={self.rate}/s, burst={self.burst}, tokens={self._tokens:.2f})"

# ═══════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════
@timed("database_query")
def fake_db_query(n: int) -> list:
    time.sleep(0.001 * n)  # simulate variable latency
    return list(range(n))

if __name__ == "__main__":
    print("=== Structured Logging ===")
    log = get_logger("myapp", json_mode=False)
    log.info("Application started")
    log.warning("Connection pool low", extra={"pool_size": 2, "threshold": 5})
    try:
        1/0
    except ZeroDivisionError:
        log.exception("Unexpected error in request handler")

    print("\n=== JSON Logging ===")
    jlog = get_logger("json.app", json_mode=True)
    jlog.info("User login", extra={"user_id": 42, "ip": "127.0.0.1"})

    print("\n=== Metrics ===")
    import random
    random.seed(42)
    for _ in range(20):
        n = random.randint(1, 10)
        fake_db_query(n)

    registry.gauge_set("active_connections", 37)
    registry.counter_inc("http_requests_total", endpoint="/api/users", method="GET")
    registry.counter_inc("http_requests_total", endpoint="/api/users", method="GET")
    registry.counter_inc("http_requests_total", endpoint="/api/login",  method="POST")

    snap = registry.snapshot()
    print("Counters:")
    for k, v in snap["counters"].items():
        print(f"  {k} = {v}")
    print("Gauges:")
    for k, v in snap["gauges"].items():
        print(f"  {k} = {v}")
    print("Histograms:")
    for k, s in snap["histograms"].items():
        print(f"  {k}: count={s['count']}, "
              f"p50={s.get('p50', 0):.2f}ms, p99={s.get('p99', 0):.2f}ms")

    print("\n=== Rate Limiter ===")
    limiter = TokenBucketRateLimiter(rate=5, burst=3)
    results = []
    for i in range(8):
        allowed = limiter.consume()
        results.append("✓" if allowed else "✗")
        time.sleep(0.05)  # 50ms between requests → 20 rps > 5 rps limit
    print(f"  Results: {results[:3]} burst, then limited")
