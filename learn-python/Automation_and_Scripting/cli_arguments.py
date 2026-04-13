"""
Automation: Command-line argument parsing.
"""
import argparse
import sys

# === Basic argparse ===
def basic_example():
    parser = argparse.ArgumentParser(
        description="A sample CLI tool",
        epilog="Example: python cli_args.py -n Alice --age 30 --verbose"
    )

    # Positional argument
    parser.add_argument("filename", help="Input file to process")

    # Optional arguments
    parser.add_argument("-n", "--name", default="World", help="Your name")
    parser.add_argument("--age", type=int, help="Your age")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--count", type=int, default=1, help="Number of greetings")
    parser.add_argument("--format", choices=["json", "text", "csv"], default="text")

    # Simulate args for demo
    args = parser.parse_args(["input.txt", "-n", "Alice", "--age", "30", "-v", "--count", "3"])

    if args.verbose:
        print(f"Processing file: {args.filename}")

    for i in range(args.count):
        print(f"Hello, {args.name}! (age: {args.age})")

basic_example()

# === Subcommands ===
print("\n=== Subcommands ===")

def create_subcommand_parser():
    parser = argparse.ArgumentParser(description="Project management tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # 'init' command
    init_parser = subparsers.add_parser("init", help="Initialize a new project")
    init_parser.add_argument("name", help="Project name")
    init_parser.add_argument("--template", default="basic", choices=["basic", "web", "api"])

    # 'build' command
    build_parser = subparsers.add_parser("build", help="Build the project")
    build_parser.add_argument("--release", action="store_true")
    build_parser.add_argument("--target", default="all")

    # 'test' command
    test_parser = subparsers.add_parser("test", help="Run tests")
    test_parser.add_argument("--coverage", action="store_true")
    test_parser.add_argument("-k", "--filter", help="Test name filter")

    return parser

parser = create_subcommand_parser()

# Simulate different commands
for cmd_args in [
    ["init", "myproject", "--template", "web"],
    ["build", "--release"],
    ["test", "--coverage", "-k", "test_auth"],
]:
    args = parser.parse_args(cmd_args)
    print(f"Command: {args.command}, Args: {vars(args)}")

# === Mutually exclusive groups ===
print("\n=== Mutually Exclusive ===")
parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=False)
group.add_argument("--json", action="store_true", help="Output as JSON")
group.add_argument("--csv", action="store_true", help="Output as CSV")
group.add_argument("--table", action="store_true", help="Output as table")

args = parser.parse_args(["--json"])
print(f"Output format: JSON={args.json}, CSV={args.csv}, Table={args.table}")

# === Type validation ===
print("\n=== Custom Types ===")

def positive_int(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(f"{value} is not a positive integer")
    return ivalue

def valid_email(value):
    if "@" not in value:
        raise argparse.ArgumentTypeError(f"{value} is not a valid email")
    return value

parser = argparse.ArgumentParser()
parser.add_argument("--port", type=positive_int, default=8080)
parser.add_argument("--email", type=valid_email)
args = parser.parse_args(["--port", "3000", "--email", "user@example.com"])
print(f"Port: {args.port}, Email: {args.email}")
