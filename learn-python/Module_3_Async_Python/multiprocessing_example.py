# Example: Multiprocessing
# Demonstrates parallelism using multiprocessing

from multiprocessing import Process
import os

def worker(name):
    print(f"Process {name} starting (PID: {os.getpid()})")
    print(f"Process {name} finished")

if __name__ == "__main__":
    processes = []
    for i in range(3):
        p = Process(target=worker, args=(f"P{i}",))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
