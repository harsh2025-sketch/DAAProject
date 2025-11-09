class BSTNode:
    __slots__ = ("key", "left", "right")
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class BinarySearchTree:
    """Unbalanced BST for benchmarking average vs worst cases."""
    def __init__(self):
        self.root = None
        self._size = 0

    def insert(self, key):
        if self.root is None:
            self.root = BSTNode(key)
            self._size += 1
            return
        cur = self.root
        while True:
            if key < cur.key:
                if cur.left is None:
                    cur.left = BSTNode(key)
                    self._size += 1
                    return
                cur = cur.left
            elif key > cur.key:
                if cur.right is None:
                    cur.right = BSTNode(key)
                    self._size += 1
                    return
                cur = cur.right
            else:
                return  # duplicate ignore

    def search(self, key):
        cur = self.root
        while cur:
            if key == cur.key:
                return True
            cur = cur.left if key < cur.key else cur.right
        return False

    def delete(self, key):
        def delete_node(node, key):
            if not node:
                return node, False
            if key < node.key:
                node.left, deleted = delete_node(node.left, key)
                return node, deleted
            if key > node.key:
                node.right, deleted = delete_node(node.right, key)
                return node, deleted
            # node found
            if not node.left:
                return node.right, True
            if not node.right:
                return node.left, True
            # two children: find inorder successor
            succ_parent = node
            succ = node.right
            while succ.left:
                succ_parent = succ
                succ = succ.left
            if succ_parent != node:
                succ_parent.left = succ.right
            else:
                succ_parent.right = succ.right
            node.key = succ.key
            return node, True
        self.root, deleted = delete_node(self.root, key)
        if deleted:
            self._size -= 1
        return deleted

    def __len__(self):
        return self._size
