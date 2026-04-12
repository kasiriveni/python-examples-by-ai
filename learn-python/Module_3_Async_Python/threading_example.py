# Example: Threading
# Demonstrates concurrency using threading

import threading
import time

def worker(name):
    print(f"Thread {name} starting")
    time.sleep(2)
    print(f"Thread {name} finished")

threads = []
for i in range(3):
    t = threading.Thread(target=worker, args=(f"T{i}",))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
