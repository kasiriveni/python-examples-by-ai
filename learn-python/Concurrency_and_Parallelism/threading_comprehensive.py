"""
Threading comprehensive examples.
"""
import threading
import time
import queue
from concurrent.futures import ThreadPoolExecutor, as_completed

# === Basic thread ===
print("=== Basic Thread ===")

def worker(name, delay):
    print(f"  [{name}] Starting")
    time.sleep(delay)
    print(f"  [{name}] Done")

t1 = threading.Thread(target=worker, args=("Thread-1", 0.5))
t2 = threading.Thread(target=worker, args=("Thread-2", 0.3))
t1.start()
t2.start()
t1.join()
t2.join()
print("  All threads done")

# === Thread with return value ===
print("\n=== Thread with Return Value ===")

class ResultThread(threading.Thread):
    def __init__(self, func, args=()):
        super().__init__()
        self.func = func
        self.args = args
        self.result = None

    def run(self):
        self.result = self.func(*self.args)

def compute_square(n):
    time.sleep(0.1)
    return n ** 2

threads = [ResultThread(compute_square, (i,)) for i in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(f"  Results: {[t.result for t in threads]}")

# === Lock ===
print("\n=== Lock (Thread Safety) ===")

class SafeCounter:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            current = self.value
            time.sleep(0.001)  # simulate work
            self.value = current + 1

counter = SafeCounter()
threads = [threading.Thread(target=counter.increment) for _ in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(f"  Counter value: {counter.value}")

# === Thread Pool ===
print("\n=== Thread Pool ===")

def download_page(url):
    time.sleep(0.2)  # simulate download
    return f"Content from {url}"

urls = [f"https://example.com/page{i}" for i in range(5)]

with ThreadPoolExecutor(max_workers=3) as executor:
    futures = {executor.submit(download_page, url): url for url in urls}
    for future in as_completed(futures):
        url = futures[future]
        result = future.result()
        print(f"  {url}: {result}")

# === Producer-Consumer with Queue ===
print("\n=== Producer-Consumer ===")

def producer(q, items):
    for item in items:
        q.put(item)
        print(f"  Produced: {item}")
        time.sleep(0.1)
    q.put(None)  # sentinel

def consumer(q):
    while True:
        item = q.get()
        if item is None:
            break
        print(f"  Consumed: {item}")
        q.task_done()

q = queue.Queue(maxsize=3)
prod = threading.Thread(target=producer, args=(q, ["a", "b", "c", "d"]))
cons = threading.Thread(target=consumer, args=(q,))
prod.start()
cons.start()
prod.join()
cons.join()

# === Event ===
print("\n=== Event ===")

event = threading.Event()

def waiter(name):
    print(f"  [{name}] Waiting for event...")
    event.wait()
    print(f"  [{name}] Event received!")

threads = [threading.Thread(target=waiter, args=(f"W{i}",)) for i in range(3)]
for t in threads:
    t.start()

time.sleep(0.5)
print("  Setting event!")
event.set()

for t in threads:
    t.join()

# === Daemon threads ===
print("\n=== Thread Info ===")
print(f"  Active threads: {threading.active_count()}")
print(f"  Current thread: {threading.current_thread().name}")
