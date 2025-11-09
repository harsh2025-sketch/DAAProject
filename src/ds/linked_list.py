class LinkedListNode:
    __slots__ = ("value", "next")
    def __init__(self, value, next=None):
        self.value = value
        self.next = next

class LinkedList:
    """Singly linked list with basic operations for benchmarking."""
    def __init__(self, iterable=None):
        self.head = None
        self._size = 0
        if iterable:
            for item in iterable:
                self.append(item)

    def append(self, value):
        if not self.head:
            self.head = LinkedListNode(value)
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = LinkedListNode(value)
        self._size += 1

    def find(self, value):
        cur = self.head
        while cur:
            if cur.value == value:
                return True
            cur = cur.next
        return False

    def delete(self, value):
        prev = None
        cur = self.head
        while cur:
            if cur.value == value:
                if prev:
                    prev.next = cur.next
                else:
                    self.head = cur.next
                self._size -= 1
                return True
            prev, cur = cur, cur.next
        return False

    def __len__(self):
        return self._size
