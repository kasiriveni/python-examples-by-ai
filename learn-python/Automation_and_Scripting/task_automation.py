"""
Automation: Schedule and task automation.
"""
import time
import threading
from datetime import datetime, timedelta
import sched

# Simple scheduler using sched module
def scheduled_task(name):
    print(f"  [{datetime.now().strftime('%H:%M:%S')}] Running: {name}")

scheduler = sched.scheduler(time.time, time.sleep)

print("Scheduling tasks...")
scheduler.enter(0, 1, scheduled_task, ("Task A",))
scheduler.enter(1, 1, scheduled_task, ("Task B",))
scheduler.enter(2, 1, scheduled_task, ("Task C",))
scheduler.run()

# Retry decorator with backoff
def retry(max_attempts=3, delay=1, backoff=2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            current_delay = delay
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        raise
                    print(f"  Attempt {attempt} failed: {e}. Retrying in {current_delay}s...")
                    time.sleep(current_delay)
                    current_delay *= backoff
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.1, backoff=2)
def unreliable_task():
    import random
    if random.random() < 0.7:
        raise ConnectionError("Service unavailable")
    return "Success!"

print("\nRetrying unreliable task:")
try:
    result = unreliable_task()
    print(f"  Result: {result}")
except ConnectionError:
    print("  All attempts failed")

# Rate limiter
class RateLimiter:
    def __init__(self, max_calls, period):
        self.max_calls = max_calls
        self.period = period
        self.calls = []

    def allow(self):
        now = time.time()
        self.calls = [t for t in self.calls if now - t < self.period]
        if len(self.calls) < self.max_calls:
            self.calls.append(now)
            return True
        return False

limiter = RateLimiter(max_calls=3, period=1.0)
print("\nRate limiter (3 calls/sec):")
for i in range(5):
    allowed = limiter.allow()
    print(f"  Request {i+1}: {'allowed' if allowed else 'denied'}")

# Periodic task runner
class PeriodicTask:
    def __init__(self, interval, func, *args):
        self.interval = interval
        self.func = func
        self.args = args
        self._timer = None
        self._running = False
        self._count = 0

    def start(self, max_runs=3):
        self._running = True
        self._run(max_runs)

    def _run(self, max_runs):
        if self._running and self._count < max_runs:
            self.func(*self.args)
            self._count += 1
            self._timer = threading.Timer(self.interval, self._run, [max_runs])
            self._timer.start()

    def stop(self):
        self._running = False
        if self._timer:
            self._timer.cancel()

print("\nPeriodic task (3 runs):")
task = PeriodicTask(0.5, lambda: print(f"  Tick at {datetime.now().strftime('%H:%M:%S')}"))
task.start(max_runs=3)
time.sleep(2)
task.stop()
