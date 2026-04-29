"""Example runner for Module 5: LLM & API Integration (mock example)"""


def count_tokens_naive(prompt: str) -> int:
    # naive token count: whitespace-separated words
    return len(prompt.split())


def main():
    print("Module 5 - LLM/API example")
    prompt = "Translate 'Hello' to Spanish."
    print("Prompt:", prompt)
    print("Naive token count:", count_tokens_naive(prompt))


if __name__ == "__main__":
    main()
