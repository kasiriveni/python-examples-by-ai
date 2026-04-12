# Profiling Example
import cProfile
import time

def slow_function():
    time.sleep(2)
    print("Finished slow function")

def main():
    slow_function()

cProfile.run('main()')
