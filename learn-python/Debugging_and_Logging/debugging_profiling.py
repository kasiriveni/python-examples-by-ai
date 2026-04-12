# Debugging & Profiling: pdb, logging, cProfile
import pdb
import logging
import cProfile

logging.basicConfig(level=logging.INFO)
logging.info('info message')

# Simple function to profile
def work(n):
    total = 0
    for i in range(n):
        total += i*i
    return total

# profile
if __name__ == '__main__':
    cProfile.run('work(10000)')
    # run with pdb: python -m pdb thisfile.py
    # or insert pdb.set_trace() to breakpoint
