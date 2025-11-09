from time import perf_counter
import random
import pandas as pd

from src.ds.array_ds import ArrayDS
from src.ds.linked_list import LinkedList
from src.ds.bst import BinarySearchTree
from src.ds.hash_table import HashTable
from src.ds.graph import Graph

RANDOM_SEED = 1337
random.seed(RANDOM_SEED)

class Benchmark:
    def __init__(self, sizes, trials=3):
        self.sizes = sizes
        self.trials = trials

    def _timeit(self, fn):
        start = perf_counter()
        fn()
        return (perf_counter() - start) * 1000.0  # ms

    def array_insert_end(self, n):
        arr = ArrayDS()
        return self._timeit(lambda: [arr.append(i) for i in range(n)])

    def array_insert_front(self, n):
        arr = ArrayDS()
        return self._timeit(lambda: [arr.insert_front(i) for i in range(n)])

    def array_search(self, n):
        data = list(range(n))
        arr = ArrayDS(data)
        target = n - 1
        return self._timeit(lambda: arr.search_linear(target))

    def array_delete(self, n):
        arr = ArrayDS(range(n))
        targets = list(range(0, n, max(1, n // 100)))  # Delete ~1% of elements
        return self._timeit(lambda: [arr.remove_value(t) for t in targets if t < len(arr.data)])

    def ll_insert_tail(self, n):
        ll = LinkedList()
        return self._timeit(lambda: [ll.append(i) for i in range(n)])

    def ll_search(self, n):
        ll = LinkedList(range(n))
        target = n - 1
        return self._timeit(lambda: ll.find(target))

    def ll_delete(self, n):
        ll = LinkedList(range(n))
        targets = list(range(0, n, max(1, n // 100)))
        return self._timeit(lambda: [ll.delete(t) for t in targets])

    def bst_insert(self, n):
        bst = BinarySearchTree()
        data = list(range(n))
        random.shuffle(data)
        return self._timeit(lambda: [bst.insert(x) for x in data])

    def bst_insert_ordered(self, n):
        """Worst case: ordered insertion creates degenerate tree"""
        bst = BinarySearchTree()
        data = list(range(n))
        return self._timeit(lambda: [bst.insert(x) for x in data])

    def bst_search(self, n):
        bst = BinarySearchTree()
        data = list(range(n))
        random.shuffle(data)
        for x in data:
            bst.insert(x)
        target = data[-1]
        return self._timeit(lambda: bst.search(target))

    def bst_delete(self, n):
        bst = BinarySearchTree()
        data = list(range(n))
        random.shuffle(data)
        for x in data:
            bst.insert(x)
        targets = data[:max(1, n // 100)]  # Delete ~1% of nodes
        return self._timeit(lambda: [bst.delete(t) for t in targets])

    def ht_put(self, n):
        ht = HashTable(capacity=max(1024, n * 2))
        keys = list(range(n))
        return self._timeit(lambda: [ht.put(k, k) for k in keys])

    def ht_get(self, n):
        ht = HashTable(capacity=max(1024, n * 2))
        keys = list(range(n))
        for k in keys:
            ht.put(k, k)
        target = keys[-1]
        return self._timeit(lambda: ht.get(target))

    def ht_delete(self, n):
        ht = HashTable(capacity=max(1024, n * 2))
        keys = list(range(n))
        for k in keys:
            ht.put(k, k)
        targets = keys[:max(1, n // 100)]
        return self._timeit(lambda: [ht.delete(t) for t in targets])

    def graph_add_edges_linear(self, n):
        g = Graph()
        return self._timeit(lambda: [g.add_edge(i, i+1) for i in range(n-1)])

    def graph_bfs_search_end(self, n):
        g = Graph()
        for i in range(n-1):
            g.add_edge(i, i+1)
        return self._timeit(lambda: g.bfs_search(n-1))

    def graph_delete_node(self, n):
        g = Graph()
        for i in range(n-1):
            g.add_edge(i, i+1)
        targets = list(range(0, n, max(1, n // 100)))
        return self._timeit(lambda: [g.delete_node(t) for t in targets if t in g.adj])

    def run(self, target: str):
        ops = {
            # arrays
            "Array: insert_end": self.array_insert_end,
            "Array: insert_front": self.array_insert_front,
            "Array: search": self.array_search,
            "Array: delete": self.array_delete,
            # linked list
            "LinkedList: insert_tail": self.ll_insert_tail,
            "LinkedList: search": self.ll_search,
            "LinkedList: delete": self.ll_delete,
            # bst
            "BST: insert": self.bst_insert,
            "BST: insert_ordered": self.bst_insert_ordered,
            "BST: search": self.bst_search,
            "BST: delete": self.bst_delete,
            # hash table
            "HashTable: put": self.ht_put,
            "HashTable: get": self.ht_get,
            "HashTable: delete": self.ht_delete,
            # graph
            "Graph: add_edges(line)": self.graph_add_edges_linear,
            "Graph: bfs_search(end)": self.graph_bfs_search_end,
            "Graph: delete_node": self.graph_delete_node,
        }
        fn = ops[target]
        records = []
        for n in self.sizes:
            for t in range(1, self.trials + 1):
                ms = fn(n)
                records.append({
                    "size": n,
                    "trial": t,
                    "time_ms": ms,
                    "operation": target,
                })
        return pd.DataFrame.from_records(records)
