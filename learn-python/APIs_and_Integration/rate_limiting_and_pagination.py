"""
API rate limiting and pagination examples.
"""
import time
from collections import defaultdict
from functools import wraps

# === Rate Limiter ===
class RateLimiter:
    """Token bucket rate limiter."""

    def __init__(self, rate, burst):
        self.rate = rate      # tokens per second
        self.burst = burst    # max tokens
        self.tokens = burst
        self.last_update = time.monotonic()

    def allow(self):
        now = time.monotonic()
        elapsed = now - self.last_update
        self.tokens = min(self.burst, self.tokens + elapsed * self.rate)
        self.last_update = now

        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False

def rate_limit(calls_per_second=10):
    """Decorator for rate limiting."""
    limiters = defaultdict(lambda: RateLimiter(calls_per_second, calls_per_second))
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = f"{func.__name__}"
            if not limiters[key].allow():
                raise Exception("Rate limit exceeded")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit(calls_per_second=2)
def api_call(endpoint):
    return f"Response from {endpoint}"

print("=== Rate Limiting ===")
for i in range(5):
    try:
        result = api_call(f"/api/data/{i}")
        print(f"  Request {i}: {result}")
    except Exception as e:
        print(f"  Request {i}: {e}")

# === Pagination ===
print("\n=== Pagination ===")

# Sample dataset
all_items = [{"id": i, "name": f"Item {i}"} for i in range(1, 51)]

# Offset-based pagination
def paginate_offset(items, page=1, per_page=10):
    start = (page - 1) * per_page
    end = start + per_page
    total = len(items)
    return {
        "data": items[start:end],
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": (total + per_page - 1) // per_page,
        "has_next": end < total,
        "has_prev": page > 1,
    }

result = paginate_offset(all_items, page=2, per_page=5)
print(f"Offset pagination (page 2):")
print(f"  Items: {[d['name'] for d in result['data']]}")
print(f"  Total pages: {result['total_pages']}")
print(f"  Has next: {result['has_next']}")

# Cursor-based pagination
def paginate_cursor(items, cursor=None, limit=10):
    start_idx = 0
    if cursor is not None:
        for i, item in enumerate(items):
            if item["id"] == cursor:
                start_idx = i + 1
                break

    page_items = items[start_idx:start_idx + limit]
    next_cursor = page_items[-1]["id"] if len(page_items) == limit else None

    return {
        "data": page_items,
        "next_cursor": next_cursor,
        "has_more": next_cursor is not None,
    }

print(f"\nCursor pagination:")
cursor = None
for page_num in range(1, 4):
    result = paginate_cursor(all_items, cursor=cursor, limit=5)
    print(f"  Page {page_num}: {[d['name'] for d in result['data']]}")
    cursor = result["next_cursor"]
    if not result["has_more"]:
        break

# === Retry with exponential backoff ===
print("\n=== Exponential Backoff ===")

def retry_with_backoff(func, max_retries=5, base_delay=0.1):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt)
            print(f"  Attempt {attempt + 1} failed: {e}. Retrying in {delay:.2f}s")
            time.sleep(delay)

call_count = 0
def flaky_api():
    global call_count
    call_count += 1
    if call_count < 3:
        raise ConnectionError("Service unavailable")
    return "Success!"

result = retry_with_backoff(flaky_api)
print(f"  Result: {result}")
