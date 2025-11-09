class HashTable:
    """Simple separate chaining hash table for integer-like keys."""
    def __init__(self, capacity=1024):
        self.capacity = capacity
        self.buckets = [[] for _ in range(capacity)]
        self._size = 0

    def _index(self, key):
        return hash(key) % self.capacity

    def put(self, key, value):
        idx = self._index(key)
        bucket = self.buckets[idx]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self._size += 1

    def get(self, key):
        idx = self._index(key)
        for k, v in self.buckets[idx]:
            if k == key:
                return v
        return None

    def delete(self, key):
        idx = self._index(key)
        bucket = self.buckets[idx]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self._size -= 1
                return True
        return False

    def contains(self, key):
        return self.get(key) is not None

    def __len__(self):
        return self._size
