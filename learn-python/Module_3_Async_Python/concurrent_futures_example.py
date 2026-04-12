# Example: concurrent.futures
# Demonstrates concurrency using ThreadPoolExecutor

from concurrent.futures import ThreadPoolExecutor
import time

def worker(name):
    print(f"Task {name} starting")
    time.sleep(2)
    print(f"Task {name} finished")

with ThreadPoolExecutor(max_workers=3) as executor:
    tasks = [executor.submit(worker, f"Task{i}") for i in range(3)]

    for future in tasks:
        future.result()
