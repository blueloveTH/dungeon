"""Common algorithms for dungeon generation."""

import heapq

# duck-type protocol
class _NodeLike:
    def get_neighbours(self) -> list[tuple('_NodeLike', int)]:
        raise NotImplementedError

def dijkstra(G: list[_NodeLike], node: _NodeLike) -> dict[_NodeLike, int]:
    """Dijkstra's algorithm for finding the shortest path from a node to all other nodes in a graph."""
    dist = {node: 0}
    queue = [(0, node)]
    while queue:
        d, u = heapq.heappop(queue)
        if d > dist[u]:
            continue
        for v, w in u.get_neighbours():
            if v not in dist or dist[v] > dist[u] + w:
                dist[v] = dist[u] + w
                heapq.heappush(queue, (dist[v], v))
    return dist