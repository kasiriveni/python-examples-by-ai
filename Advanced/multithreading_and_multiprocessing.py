# Example: Multithreading and Multiprocessing
import threading
import multiprocessing

def print_numbers():
    for i in range(5):
        print(i)

# Multithreading
thread = threading.Thread(target=print_numbers)
thread.start()
thread.join()

# Multiprocessing
process = multiprocessing.Process(target=print_numbers)
process.start()
process.join()
