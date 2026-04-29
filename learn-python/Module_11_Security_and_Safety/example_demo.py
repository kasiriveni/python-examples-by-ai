"""Security demo: basic input validation examples"""
import re


def is_valid_email(s: str) -> bool:
    return re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", s) is not None


def main():
    print("Security demo")
    tests = ["alice@example.com", "bad@com", "no-at-symbol"]
    for t in tests:
        print(t, "=>", is_valid_email(t))


if __name__ == '__main__':
    main()
