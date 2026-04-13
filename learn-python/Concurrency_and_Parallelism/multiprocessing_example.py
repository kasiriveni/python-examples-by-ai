"""
Example of using multiprocessing for parallel computation.
"""
from multiprocessing import Process

def worker(task_id):
    print(f"Task {task_id} is running")

if __name__ == "__main__":
    processes = []
    for i in range(5):
        p = Process(target=worker, args=(i,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    print("All processes completed.")
