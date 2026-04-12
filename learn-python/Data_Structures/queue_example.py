# Queue Implementation in Python
class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, item):
        self.queue.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.queue.pop(0)
        return "Queue is empty"

    def peek(self):
        if not self.is_empty():
            return self.queue[0]
        return "Queue is empty"

    def is_empty(self):
        return len(self.queue) == 0

# Example Usage
queue = Queue()
queue.enqueue(10)
queue.enqueue(20)
print("Front of queue:", queue.peek())
print("Dequeued item:", queue.dequeue())
print("Is queue empty?", queue.is_empty())
