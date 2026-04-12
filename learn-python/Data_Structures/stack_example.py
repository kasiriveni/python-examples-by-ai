# Stack Implementation in Python
class Stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        return "Stack is empty"

    def peek(self):
        if not self.is_empty():
            return self.stack[-1]
        return "Stack is empty"

    def is_empty(self):
        return len(self.stack) == 0

# Example Usage
stack = Stack()
stack.push(10)
stack.push(20)
print("Top of stack:", stack.peek())
print("Popped item:", stack.pop())
print("Is stack empty?", stack.is_empty())
