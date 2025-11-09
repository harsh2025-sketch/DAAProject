from collections import deque

class Graph:
    """Undirected graph via adjacency list."""
    def __init__(self):
        self.adj = {}
        self._edges = 0

    def add_node(self, u):
        if u not in self.adj:
            self.adj[u] = set()

    def add_edge(self, u, v):
        self.add_node(u)
        self.add_node(v)
        if v not in self.adj[u]:
            self.adj[u].add(v)
            self.adj[v].add(u)
            self._edges += 1

    def bfs_search(self, target):
        if not self.adj:
            return False
        start = next(iter(self.adj))
        visited = {start}
        q = deque([start])
        while q:
            node = q.popleft()
            if node == target:
                return True
            for nei in self.adj[node]:
                if nei not in visited:
                    visited.add(nei)
                    q.append(nei)
        return False

    def delete_node(self, u):
        if u not in self.adj:
            return False
        for v in list(self.adj[u]):
            self.adj[v].remove(u)
            self._edges -= 1
        del self.adj[u]
        return True

    def node_count(self):
        return len(self.adj)

    def edge_count(self):
        return self._edges
