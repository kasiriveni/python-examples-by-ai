"""
Module 9: Production AI Apps - deployment, monitoring, caching.
"""
import time
import json
import hashlib
import functools
from collections import OrderedDict
from dataclasses import dataclass, field
from datetime import datetime

# === LRU Cache for API responses ===
print("=== Response Caching ===")

class TTLCache:
    """Cache with time-to-live expiration."""

    def __init__(self, maxsize=100, ttl=300):
        self.maxsize = maxsize
        self.ttl = ttl
        self._cache = OrderedDict()
        self._timestamps = {}

    def get(self, key):
        if key in self._cache:
            if time.time() - self._timestamps[key] < self.ttl:
                self._cache.move_to_end(key)
                return self._cache[key]
            else:
                del self._cache[key]
                del self._timestamps[key]
        return None

    def set(self, key, value):
        if key in self._cache:
            self._cache.move_to_end(key)
        elif len(self._cache) >= self.maxsize:
            oldest = next(iter(self._cache))
            del self._cache[oldest]
            del self._timestamps[oldest]
        self._cache[key] = value
        self._timestamps[key] = time.time()

    @property
    def stats(self):
        return {"size": len(self._cache), "maxsize": self.maxsize}

cache = TTLCache(maxsize=50, ttl=60)
cache.set("query:hello", {"response": "Hi there!", "tokens": 10})
result = cache.get("query:hello")
print(f"Cached: {result}")
print(f"Stats: {cache.stats}")

# === Request/Response Logging ===
print("\n=== Request Logging ===")

@dataclass
class RequestLog:
    timestamp: str
    endpoint: str
    method: str
    status_code: int
    latency_ms: float
    tokens_used: int = 0
    error: str = None

class RequestLogger:
    def __init__(self):
        self.logs = []

    def log(self, **kwargs):
        entry = RequestLog(timestamp=datetime.now().isoformat(), **kwargs)
        self.logs.append(entry)
        return entry

    def summary(self):
        if not self.logs:
            return {}
        latencies = [l.latency_ms for l in self.logs]
        errors = [l for l in self.logs if l.error]
        return {
            "total_requests": len(self.logs),
            "error_count": len(errors),
            "avg_latency_ms": sum(latencies) / len(latencies),
            "max_latency_ms": max(latencies),
            "total_tokens": sum(l.tokens_used for l in self.logs),
        }

logger = RequestLogger()
logger.log(endpoint="/api/chat", method="POST", status_code=200, latency_ms=150, tokens_used=80)
logger.log(endpoint="/api/chat", method="POST", status_code=200, latency_ms=200, tokens_used=120)
logger.log(endpoint="/api/chat", method="POST", status_code=500, latency_ms=50, error="Rate limited")
print(f"Summary: {json.dumps(logger.summary(), indent=2)}")

# === Circuit Breaker ===
print("\n=== Circuit Breaker ===")

class CircuitBreaker:
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

    def __init__(self, failure_threshold=3, recovery_timeout=10):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state = self.CLOSED
        self.failure_count = 0
        self.last_failure_time = 0

    def call(self, func, *args, **kwargs):
        if self.state == self.OPEN:
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = self.HALF_OPEN
                print(f"  [CB] State: HALF_OPEN (trying recovery)")
            else:
                raise Exception("Circuit breaker is OPEN")

        try:
            result = func(*args, **kwargs)
            if self.state == self.HALF_OPEN:
                self.state = self.CLOSED
                self.failure_count = 0
                print(f"  [CB] State: CLOSED (recovered)")
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = self.OPEN
                print(f"  [CB] State: OPEN (threshold reached)")
            raise

cb = CircuitBreaker(failure_threshold=2, recovery_timeout=5)

def unreliable_api():
    raise ConnectionError("Service unavailable")

for i in range(4):
    try:
        cb.call(unreliable_api)
    except Exception as e:
        print(f"  Attempt {i+1}: {e}")

# === Health Check ===
print("\n=== Health Check ===")

class HealthChecker:
    def __init__(self):
        self.checks = {}

    def register(self, name, check_func):
        self.checks[name] = check_func

    def run_all(self):
        results = {}
        all_healthy = True
        for name, check in self.checks.items():
            try:
                check()
                results[name] = {"status": "healthy"}
            except Exception as e:
                results[name] = {"status": "unhealthy", "error": str(e)}
                all_healthy = False
        return {"status": "healthy" if all_healthy else "unhealthy", "checks": results}

health = HealthChecker()
health.register("cache", lambda: None)  # Always healthy
health.register("database", lambda: None)  # Always healthy
health.register("external_api", lambda: (_ for _ in ()).throw(ConnectionError("timeout")))

result = health.run_all()
print(json.dumps(result, indent=2))
