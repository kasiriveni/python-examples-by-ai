"""Agent demo: simple tool dispatcher"""


def tool_echo(text):
    return text


def dispatch(tool_name, *args):
    tools = {"echo": tool_echo}
    fn = tools.get(tool_name)
    if not fn:
        return f"Unknown tool: {tool_name}"
    return fn(*args)


def main():
    print("Agent dispatch:", dispatch("echo", "hello world"))
    print("Agent dispatch unknown:", dispatch("foo"))


if __name__ == '__main__':
    main()
