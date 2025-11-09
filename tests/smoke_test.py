from src.ds.array_ds import ArrayDS
from src.ds.linked_list import LinkedList
from src.ds.bst import BinarySearchTree
from src.ds.hash_table import HashTable
from src.ds.graph import Graph


def test_smoke():
    arr = ArrayDS([1,2,3])
    arr.append(4)
    assert len(arr) == 4

    ll = LinkedList([1,2,3])
    assert ll.find(2)

    bst = BinarySearchTree()
    for x in [3,1,4,2]:
        bst.insert(x)
    assert bst.search(2)

    ht = HashTable()
    ht.put('a', 1)
    assert ht.get('a') == 1

    g = Graph()
    g.add_edge(1,2)
    assert g.bfs_search(2)
