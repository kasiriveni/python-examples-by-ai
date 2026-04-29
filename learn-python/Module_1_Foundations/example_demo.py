"""Foundations demo: small utilities and unpacking examples"""
def head_tail(seq):
    head, *tail = seq
    return head, tail


def main():
    print("Foundations demo")
    items = [10, 20, 30, 40]
    h, t = head_tail(items)
    print("Head:", h)
    print("Tail:", t)
    print("Reversed:", list(reversed(items)))


if __name__ == '__main__':
    main()
