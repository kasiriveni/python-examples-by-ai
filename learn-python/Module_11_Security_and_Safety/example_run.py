"""Example runner for Module 11: Security & Safety (simple sanitizer)"""
import re


def sanitize_prompt(prompt: str) -> str:
    # very small example: remove control characters and suspicious sequences
    cleaned = re.sub(r"[\x00-\x1f\x7f]+", "", prompt)
    cleaned = cleaned.replace("$$$", "$")
    return cleaned


def main():
    print("Module 11 - Security example")
    p = "Hello\x00\x07; DROP TABLE users; $$$"
    print("Before:", repr(p))
    print("After:", repr(sanitize_prompt(p)))


if __name__ == "__main__":
    main()
