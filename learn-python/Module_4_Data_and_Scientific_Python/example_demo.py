"""Data demo: CSV parsing and simple aggregation using stdlib"""
import csv
from io import StringIO


SAMPLE = """name,score
alice,10
bob,15
carol,12
"""


def parse_and_avg(text):
    f = StringIO(text)
    reader = csv.DictReader(f)
    scores = [int(r['score']) for r in reader]
    return sum(scores) / len(scores)


def main():
    print("Data demo")
    print("Average score:", parse_and_avg(SAMPLE))


if __name__ == '__main__':
    main()
