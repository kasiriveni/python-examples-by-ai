"""Example runner for Module 8: AI Agents & Tool Use (toy loop)"""


def decide(task):
    # trivial rule-based "agent"
    if "summarize" in task.lower():
        return "summarize"
    return "noop"


def main():
    print("Module 8 - Agent example")
    tasks = ["Summarize this document.", "Do nothing"]
    for t in tasks:
        action = decide(t)
        print(f"Task: {t!r} -> Action: {action}")


if __name__ == "__main__":
    main()
