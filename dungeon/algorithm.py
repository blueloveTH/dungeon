"""Common algorithms for dungeon generation."""

import heapq

class Rect:
    def __init__(self, left: int, top: int, right: int, bottom: int):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    def width(self) -> int:
        return self.right - self.left
    
    def height(self) -> int:
        return self.bottom - self.top
    
    def area(self) -> int:
        return self.width() * self.height()
    
    def intersect(self, other: 'Rect') -> 'Rect':
        return Rect(
            max(self.left, other.left),
            max(self.top, other.top),
            min(self.right, other.right),
            min(self.bottom, other.bottom)
        )
    

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