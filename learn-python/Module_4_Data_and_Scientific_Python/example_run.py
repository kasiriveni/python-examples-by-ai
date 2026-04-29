"""Example runner for Module 4: Data & Scientific Python (stdlib-only)"""
import statistics


def main():
    print("Module 4 - Data example")
    data = [2, 4, 4, 4, 5, 5, 7, 9]
    print("Data:", data)
    print("Mean:", statistics.mean(data))
    print("Median:", statistics.median(data))
    print("Stdev:", round(statistics.pstdev(data), 3))


if __name__ == "__main__":
    main()
