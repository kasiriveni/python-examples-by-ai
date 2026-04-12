# Context managers: with, contextlib
from contextlib import contextmanager

@contextmanager
def simple_ctx(name):
    print(f"enter {name}")
    try:
        yield
    finally:
        print(f"exit {name}")

with simple_ctx('test'):
    print('inside')

# Custom class-based context manager
class FileOp:
    def __init__(self, path):
        self.path = path
    def __enter__(self):
        self.f = open(self.path, 'w')
        return self.f
    def __exit__(self, exc_type, exc, tb):
        self.f.close()

with FileOp('ctx.txt') as f:
    f.write('hello')
