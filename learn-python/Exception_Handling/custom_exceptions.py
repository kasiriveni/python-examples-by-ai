# Exception handling: custom exceptions and chaining
class MyError(Exception):
    pass

try:
    raise MyError('something bad')
except MyError as e:
    raise RuntimeError('wrapped') from e


# example try catch throw
try:
    raise MyError('something bad')
except MyError as e:
    raise RuntimeError('wrapped') from e
