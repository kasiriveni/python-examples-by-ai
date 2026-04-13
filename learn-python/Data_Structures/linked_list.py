"""
Data Structures: Linked List implementation.
"""

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __repr__(self):
        return f"Node({self.data})"

class LinkedList:
    def __init__(self):
        self.head = None
        self._size = 0

    def __len__(self):
        return self._size

    def __repr__(self):
        items = []
        current = self.head
        while current:
            items.append(str(current.data))
            current = current.next
        return " -> ".join(items) + " -> None"

    def __iter__(self):
        current = self.head
        while current:
            yield current.data
            current = current.next

    def __contains__(self, value):
        return any(item == value for item in self)

    # Insert operations
    def prepend(self, data):
        node = Node(data)
        node.next = self.head
        self.head = node
        self._size += 1

    def append(self, data):
        node = Node(data)
        if not self.head:
            self.head = node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = node
        self._size += 1

    def insert_at(self, index, data):
        if index <= 0:
            self.prepend(data)
            return
        node = Node(data)
        current = self.head
        for _ in range(index - 1):
            if not current.next:
                break
            current = current.next
        node.next = current.next
        current.next = node
        self._size += 1

    # Delete operations
    def delete(self, value):
        if not self.head:
            return False
        if self.head.data == value:
            self.head = self.head.next
            self._size -= 1
            return True
        current = self.head
        while current.next:
            if current.next.data == value:
                current.next = current.next.next
                self._size -= 1
                return True
            current = current.next
        return False

    def pop_front(self):
        if not self.head:
            raise IndexError("Pop from empty list")
        data = self.head.data
        self.head = self.head.next
        self._size -= 1
        return data

    # Search
    def find(self, value):
        for i, item in enumerate(self):
            if item == value:
                return i
        return -1

    # Utility
    def reverse(self):
        prev = None
        current = self.head
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev

    def to_list(self):
        return list(self)

    @classmethod
    def from_list(cls, items):
        ll = cls()
        for item in items:
            ll.append(item)
        return ll

if __name__ == "__main__":
    print("=== Linked List ===")
    ll = LinkedList.from_list([1, 2, 3, 4, 5])
    print(f"List: {ll}")
    print(f"Length: {len(ll)}")
    print(f"Contains 3: {3 in ll}")

    ll.prepend(0)
    print(f"After prepend(0): {ll}")

    ll.append(6)
    print(f"After append(6): {ll}")

    ll.insert_at(3, 99)
    print(f"After insert_at(3, 99): {ll}")

    ll.delete(99)
    print(f"After delete(99): {ll}")

    ll.reverse()
    print(f"Reversed: {ll}")

    print(f"Find 4: index={ll.find(4)}")
    print(f"As list: {ll.to_list()}")

    print(f"\nPop front: {ll.pop_front()}")
    print(f"After pop: {ll}")
