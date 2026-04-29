"""LLM/API demo: prompt templating and simple response matcher (no external calls)"""


def render_template(template: str, **kwargs) -> str:
    return template.format(**kwargs)


def simple_reply(prompt: str) -> str:
    if "translate" in prompt.lower():
        return "Hola"
    return "I don't know"


def main():
    t = "Translate '{word}' to Spanish."
    p = render_template(t, word="Hello")
    print("Prompt:", p)
    print("Reply:", simple_reply(p))


if __name__ == '__main__':
    main()
