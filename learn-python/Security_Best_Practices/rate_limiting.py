"""
Security Best Practices: Rate limiting and DoS prevention patterns.
"""
import time
import threading
from collections import deque
from dataclasses import dataclass, field

# ═══════════════════════════════════════════
# 1. Fixed-window rate limiter
# ═══════════════════════════════════════════
class FixedWindowLimiter:
    """Allows up to `max_calls` per `window_seconds`."""

    def __init__(self, max_calls: int, window_seconds: float):
        self.max_calls = max_calls
        self.window_seconds = window_seconds
        self._lock = threading.Lock()
        self._window_start: float = time.monotonic()
        self._count: int = 0

    def is_allowed(self) -> bool:
        now = time.monotonic()
        with self._lock:
            if now - self._window_start >= self.window_seconds:
                self._window_start = now
                self._count = 0
            if self._count < self.max_calls:
                self._count += 1
                return True
            return False

    def remaining(self) -> int:
        return max(0, self.max_calls - self._count)

# ═══════════════════════════════════════════
# 2. Sliding-window log limiter
# ═══════════════════════════════════════════
class SlidingWindowLimiter:
    """More accurate than fixed-window; tracks each request timestamp."""

    def __init__(self, max_calls: int, window_seconds: float):
        self.max_calls = max_calls
        self.window_seconds = window_seconds
        self._timestamps: deque[float] = deque()
        self._lock = threading.Lock()

    def is_allowed(self) -> bool:
        now = time.monotonic()
        with self._lock:
            # Remove expired timestamps
            while self._timestamps and now - self._timestamps[0] >= self.window_seconds:
                self._timestamps.popleft()
            if len(self._timestamps) < self.max_calls:
                self._timestamps.append(now)
                return True
            return False

    def usage(self) -> int:
        return len(self._timestamps)

# ═══════════════════════════════════════════
# 3. Token bucket (burst-friendly)
# ═══════════════════════════════════════════
class TokenBucket:
    """Allows bursts up to `capacity`, refills at `rate` tokens/sec."""

    def __init__(self, capacity: float, rate: float):
        self.capacity = capacity
        self.rate = rate
        self._tokens = float(capacity)
        self._last_refill = time.monotonic()
        self._lock = threading.Lock()

    def _refill(self) -> None:
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._tokens = min(self.capacity, self._tokens + elapsed * self.rate)
        self._last_refill = now

    def consume(self, tokens: float = 1.0) -> bool:
        with self._lock:
            self._refill()
            if self._tokens >= tokens:
                self._tokens -= tokens
                return True
            return False

    @property
    def tokens(self) -> float:
        return self._tokens

# ═══════════════════════════════════════════
# 4. Leaky bucket (output-smooth)
# ═══════════════════════════════════════════
class LeakyBucket:
    """Smooths out bursty traffic to a steady rate."""

    def __init__(self, capacity: int, rate: float):
        self.capacity = capacity
        self.rate = rate          # items/second to drain
        self._queue: deque = deque()
        self._last_drain = time.monotonic()
        self._lock = threading.Lock()

    def _drain(self) -> None:
        now = time.monotonic()
        elapsed = now - self._last_drain
        drain_count = int(elapsed * self.rate)
        for _ in range(min(drain_count, len(self._queue))):
            self._queue.popleft()
        self._last_drain = now

    def add(self, request) -> bool:
        with self._lock:
            self._drain()
            if len(self._queue) < self.capacity:
                self._queue.append(request)
                return True
            return False  # overflow — drop

    @property
    def queue_size(self) -> int:
        return len(self._queue)

# ═══════════════════════════════════════════
# 5. Per-key rate limiting (by IP / user ID)
# ═══════════════════════════════════════════
class PerKeyLimiter:
    """Maintains separate rate limits per key (e.g., per-IP, per-user)."""

    def __init__(self, max_calls: int, window_seconds: float):
        self.max_calls = max_calls
        self.window_seconds = window_seconds
        self._limiters: dict[str, SlidingWindowLimiter] = {}
        self._lock = threading.Lock()

    def _get_limiter(self, key: str) -> SlidingWindowLimiter:
        with self._lock:
            if key not in self._limiters:
                self._limiters[key] = SlidingWindowLimiter(self.max_calls, self.window_seconds)
            return self._limiters[key]

    def is_allowed(self, key: str) -> bool:
        return self._get_limiter(key).is_allowed()

    def usage(self, key: str) -> int:
        return self._get_limiter(key).usage()

    def keys(self) -> list[str]:
        return list(self._limiters.keys())

# ═══════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════
if __name__ == "__main__":
    print("=== Fixed Window Limiter (5 req/10s) ===")
    fw = FixedWindowLimiter(5, 10)
    results = [fw.is_allowed() for _ in range(8)]
    print(f"  {results}")
    print(f"  Remaining: {fw.remaining()}")

    print("\n=== Sliding Window Limiter (5 req/1s) ===")
    sw = SlidingWindowLimiter(5, 1.0)
    results = []
    for i in range(7):
        ok = sw.is_allowed()
        results.append("✓" if ok else "✗")
    print(f"  Burst of 7: {results}")

    time.sleep(1.1)  # wait for window to slide
    after = sw.is_allowed()
    print(f"  After 1.1s: {'✓' if after else '✗'}")

    print("\n=== Token Bucket (cap=5, rate=2/s) ===")
    tb = TokenBucket(capacity=5, rate=2)
    results = []
    for i in range(8):
        ok = tb.consume()
        results.append(f"{'✓' if ok else '✗'}({tb.tokens:.1f})")
    print(f"  {results}")

    time.sleep(1)
    print(f"  After 1s sleep, tokens: {tb.tokens:.1f}")
    print(f"  Allow: {'✓' if tb.consume() else '✗'}")

    print("\n=== Leaky Bucket (cap=3, rate=5/s) ===")
    lb = LeakyBucket(capacity=3, rate=5)
    results = [lb.add(f"req{i}") for i in range(5)]
    print(f"  {['✓' if r else '✗' for r in results]}")
    print(f"  Queue: {lb.queue_size}")

    print("\n=== Per-Key Limiter (3 req/1s) ===")
    per_key = PerKeyLimiter(3, 1.0)
    ips = ["192.168.1.1"] * 5 + ["10.0.0.1"] * 3
    for ip in ips:
        ok = per_key.is_allowed(ip)
        print(f"  {ip}: {'✓' if ok else '✗'} (usage={per_key.usage(ip)})")
