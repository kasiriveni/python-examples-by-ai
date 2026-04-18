# Core Python Concepts

## Core Themes
- Iterator protocol and stateful iteration.
- Generators, lazy pipelines, and infinite sequences.
- Advanced generator control with send, throw, close, and itertools.

## Core Theme Examples
- Example 1: Custom iterator class implementing __iter__ and __next__ methods.
- Example 2: Generator function with yield for lazy Fibonacci sequence.
- Example 3: send() method for generator messaging or itertools.chain composition.

## Files and Concepts
- custom_iterators.py: custom iter and next methods, CountUp and Fibonacci iterators
- generator_pipelines.py: generator stages, lazy composition, streaming data flow
- infinite_sequences.py: infinite generators, lazy Fibonacci and prime generation
- iterators_generators.py: basic iterator classes, generator functions
- iterators_generators_comprehensive.py: countdown iterators, send, generator expressions, comprehensive patterns
- itertools_tour.py: count, cycle, repeat, permutations, combinations, product, islice
- send_throw_close.py: generator messaging, exception injection, graceful generator shutdown

## Core Example
This example uses a generator to lazily produce values.

```python
def countdown(start):
	while start > 0:
		yield start
		start -= 1

for value in countdown(3):
	print(value)
```
