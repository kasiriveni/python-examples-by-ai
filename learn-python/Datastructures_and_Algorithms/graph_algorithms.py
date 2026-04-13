"""
Datastructures and Algorithms: Graph algorithms.
"""
from collections import defaultdict, deque

class Graph:
    def __init__(self, directed=False):
        self.adj = defaultdict(list)
        self.directed = directed

    def add_edge(self, u, v, weight=1):
        self.adj[u].append((v, weight))
        if not self.directed:
            self.adj[v].append((u, weight))

    def vertices(self):
        return set(self.adj.keys())

    # === BFS ===
    def bfs(self, start):
        visited = set()
        order = []
        queue = deque([start])
        visited.add(start)

        while queue:
            node = queue.popleft()
            order.append(node)
            for neighbor, _ in self.adj[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return order

    # === DFS ===
    def dfs(self, start):
        visited = set()
        order = []

        def _dfs(node):
            visited.add(node)
            order.append(node)
            for neighbor, _ in self.adj[node]:
                if neighbor not in visited:
                    _dfs(neighbor)

        _dfs(start)
        return order

    # === Shortest path (BFS for unweighted) ===
    def shortest_path_bfs(self, start, end):
        queue = deque([(start, [start])])
        visited = {start}

        while queue:
            node, path = queue.popleft()
            if node == end:
                return path
            for neighbor, _ in self.adj[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return None

    # === Dijkstra's Algorithm ===
    def dijkstra(self, start):
        import heapq
        distances = {v: float('inf') for v in self.vertices()}
        distances[start] = 0
        previous = {v: None for v in self.vertices()}
        pq = [(0, start)]

        while pq:
            dist, node = heapq.heappop(pq)
            if dist > distances[node]:
                continue
            for neighbor, weight in self.adj[node]:
                new_dist = dist + weight
                if new_dist < distances.get(neighbor, float('inf')):
                    distances[neighbor] = new_dist
                    previous[neighbor] = node
                    heapq.heappush(pq, (new_dist, neighbor))

        return distances, previous

    def shortest_path_dijkstra(self, start, end):
        distances, previous = self.dijkstra(start)
        path = []
        node = end
        while node is not None:
            path.append(node)
            node = previous.get(node)
        path.reverse()
        if path[0] == start:
            return path, distances[end]
        return None, float('inf')

    # === Cycle detection ===
    def has_cycle(self):
        visited = set()
        rec_stack = set()

        def _dfs(node):
            visited.add(node)
            rec_stack.add(node)
            for neighbor, _ in self.adj[node]:
                if neighbor not in visited:
                    if _dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            rec_stack.discard(node)
            return False

        for v in self.vertices():
            if v not in visited:
                if _dfs(v):
                    return True
        return False

    # === Topological Sort (DAG) ===
    def topological_sort(self):
        in_degree = defaultdict(int)
        for u in self.adj:
            for v, _ in self.adj[u]:
                in_degree[v] += 1

        queue = deque([v for v in self.vertices() if in_degree[v] == 0])
        result = []

        while queue:
            node = queue.popleft()
            result.append(node)
            for neighbor, _ in self.adj[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        return result if len(result) == len(self.vertices()) else None

if __name__ == "__main__":
    # Unweighted graph
    print("=== BFS & DFS ===")
    g = Graph()
    edges = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4), (2, 5)]
    for u, v in edges:
        g.add_edge(u, v)

    print(f"BFS from 0: {g.bfs(0)}")
    print(f"DFS from 0: {g.dfs(0)}")
    print(f"Shortest path 0->4: {g.shortest_path_bfs(0, 4)}")

    # Weighted graph
    print("\n=== Dijkstra ===")
    wg = Graph()
    wg.add_edge("A", "B", 4)
    wg.add_edge("A", "C", 2)
    wg.add_edge("B", "D", 3)
    wg.add_edge("C", "B", 1)
    wg.add_edge("C", "D", 5)
    wg.add_edge("D", "E", 1)

    distances, _ = wg.dijkstra("A")
    print(f"Distances from A: {dict(distances)}")
    path, dist = wg.shortest_path_dijkstra("A", "E")
    print(f"Shortest A->E: {path} (distance={dist})")

    # DAG topological sort
    print("\n=== Topological Sort ===")
    dag = Graph(directed=True)
    dag.add_edge("math", "physics")
    dag.add_edge("math", "cs")
    dag.add_edge("physics", "quantum")
    dag.add_edge("cs", "ai")
    dag.add_edge("cs", "databases")
    print(f"Order: {dag.topological_sort()}")