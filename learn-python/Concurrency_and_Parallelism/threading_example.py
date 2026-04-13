"""
Example of using threading for parallel tasks.
"""
import threading
import time

def worker(task_id):
    print(f"Task {task_id} starting")
    time.sleep(2)
    print(f"Task {task_id} completed")

threads = []
for i in range(5):
    thread = threading.Thread(target=worker, args=(i,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print("All tasks completed.")
