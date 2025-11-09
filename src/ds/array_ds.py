class ArrayDS:
    """Wrapper around Python list to standardize operations for benchmarking."""
    def __init__(self, iterable=None):
        self.data = list(iterable) if iterable is not None else []

    def append(self, value):
        self.data.append(value)

    def insert_front(self, value):
        self.data.insert(0, value)

    def pop_back(self):
        if self.data:
            self.data.pop()

    def remove_value(self, value):
        try:
            self.data.remove(value)
            return True
        except ValueError:
            return False

    def search_linear(self, value):
        return value in self.data

    def __len__(self):
        return len(self.data)
