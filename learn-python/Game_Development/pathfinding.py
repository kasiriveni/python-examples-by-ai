"""
Game Development: A* and Dijkstra pathfinding algorithms.
"""
import heapq
import math
from dataclasses import dataclass, field
from typing import Iterator

# ═══════════════════════════════════════════
# Grid types
# ═══════════════════════════════════════════
WALL  = "#"
EMPTY = "."
START = "S"
END   = "E"
PATH  = "·"

@dataclass(frozen=True, order=True)
class Cell:
    row: int
    col: int

    def __add__(self, o: "Cell") -> "Cell":
        return Cell(self.row + o.row, self.col + o.col)

    def manhattan(self, other: "Cell") -> int:
        return abs(self.row - other.row) + abs(self.col - other.col)

    def euclidean(self, other: "Cell") -> float:
        return math.hypot(self.row - other.row, self.col - other.col)

class Grid:
    CARDINAL  = [Cell(-1,0), Cell(1,0), Cell(0,-1), Cell(0,1)]
    DIAGONAL  = CARDINAL + [Cell(-1,-1), Cell(-1,1), Cell(1,-1), Cell(1,1)]

    def __init__(self, rows: list[str]):
        self._grid = rows
        self.height = len(rows)
        self.width  = max(len(r) for r in rows)

    def __getitem__(self, cell: Cell) -> str:
        return self._grid[cell.row][cell.col]

    def walkable(self, cell: Cell) -> bool:
        return (0 <= cell.row < self.height and
                0 <= cell.col < self.width and
                self._grid[cell.row][cell.col] != WALL)

    def neighbors(self, cell: Cell, diagonal: bool = False) -> list[Cell]:
        dirs = self.DIAGONAL if diagonal else self.CARDINAL
        return [cell + d for d in dirs if self.walkable(cell + d)]

    def cost(self, a: Cell, b: Cell) -> float:
        """Cost of moving from a to b (diagonal = √2)."""
        dr, dc = abs(a.row - b.row), abs(a.col - b.col)
        return math.sqrt(2) if dr + dc == 2 else 1.0

    def find(self, char: str) -> Cell | None:
        for r, row in enumerate(self._grid):
            for c, ch in enumerate(row):
                if ch == char:
                    return Cell(r, c)
        return None

    def render(self, path: list[Cell] = (), visited: set[Cell] = ()) -> str:
        path_set = set(path)
        rows = []
        for r, row in enumerate(self._grid):
            cols = []
            for c, ch in enumerate(row):
                cell = Cell(r, c)
                if ch in (START, END, WALL):
                    cols.append(ch)
                elif cell in path_set:
                    cols.append(PATH)
                elif cell in visited:
                    cols.append("○")
                else:
                    cols.append(ch)
            rows.append("".join(cols))
        return "\n".join(rows)

# ═══════════════════════════════════════════
# Dijkstra's shortest path
# ═══════════════════════════════════════════
def dijkstra(grid: Grid, start: Cell, end: Cell,
             diagonal: bool = False) -> tuple[list[Cell], dict[Cell, float]]:
    """Returns (path, dist_map)."""
    dist   = {start: 0.0}
    prev   = {start: None}
    pq     = [(0.0, start)]

    while pq:
        d, cell = heapq.heappop(pq)
        if d > dist.get(cell, float("inf")):
            continue
        if cell == end:
            break
        for nb in grid.neighbors(cell, diagonal):
            nd = d + grid.cost(cell, nb)
            if nd < dist.get(nb, float("inf")):
                dist[nb] = nd
                prev[nb] = cell
                heapq.heappush(pq, (nd, nb))

    # Reconstruct path
    path = []
    cur  = end
    while cur is not None:
        path.append(cur)
        cur = prev.get(cur)
    path.reverse()
    if not path or path[0] != start:
        return [], dist  # no path found
    return path, dist

# ═══════════════════════════════════════════
# A* search
# ═══════════════════════════════════════════
def astar(grid: Grid, start: Cell, end: Cell,
          heuristic=None, diagonal: bool = False) -> tuple[list[Cell], int]:
    """Returns (path, nodes_expanded)."""
    if heuristic is None:
        heuristic = Cell.manhattan if not diagonal else Cell.euclidean

    g_score = {start: 0.0}
    f_score = {start: heuristic(start, end)}
    prev    = {start: None}
    pq      = [(f_score[start], 0, start)]   # (f, tiebreak, cell)
    closed: set[Cell] = set()
    counter = 0
    expanded = 0

    while pq:
        _, _, cell = heapq.heappop(pq)
        if cell in closed:
            continue
        closed.add(cell)
        expanded += 1

        if cell == end:
            break

        for nb in grid.neighbors(cell, diagonal):
            if nb in closed:
                continue
            tg = g_score[cell] + grid.cost(cell, nb)
            if tg < g_score.get(nb, float("inf")):
                g_score[nb] = tg
                f_score[nb] = tg + heuristic(nb, end)
                prev[nb]    = cell
                counter += 1
                heapq.heappush(pq, (f_score[nb], counter, nb))

    # Reconstruct
    path = []
    cur  = end
    while cur is not None:
        path.append(cur)
        cur = prev.get(cur)
    path.reverse()
    if not path or path[0] != start:
        return [], expanded
    return path, expanded

# ═══════════════════════════════════════════
# BFS (breadth-first — unweighted)
# ═══════════════════════════════════════════
from collections import deque

def bfs(grid: Grid, start: Cell, end: Cell) -> tuple[list[Cell], set[Cell]]:
    """BFS — optimal for unweighted grids."""
    queue   = deque([(start, [start])])
    visited = {start}

    while queue:
        cell, path = queue.popleft()
        if cell == end:
            return path, visited
        for nb in grid.neighbors(cell):
            if nb not in visited:
                visited.add(nb)
                queue.append((nb, path + [nb]))

    return [], visited

# ═══════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════
MAP = [
    "S...#....",
    ".###.###.",
    ".....#...",
    "##.###.##",
    "....#...E",
]

MAP2 = [   # more complex
    "S.......#.....",
    ".#######.####.",
    ".#......#...#.",
    ".#.####.#.#.#.",
    ".#.#..#.#.#.#.",
    ".#.####.#.#.#.",
    ".......##...#.",
    "######.#####..",
    ".......#......",
    ".##########.##",
    "..............E",
]

if __name__ == "__main__":
    for name, raw_map in [("Simple", MAP), ("Complex", MAP2)]:
        print(f"\n=== {name} map ===")
        grid  = Grid(raw_map)
        start = grid.find(START)
        end   = grid.find(END)

        # BFS
        bfs_path, bfs_visited = bfs(grid, start, end)
        print(f"\nBFS:    {len(bfs_path)} steps, {len(bfs_visited)} visited")
        if bfs_path:
            print(grid.render(bfs_path, bfs_visited))

        # A*
        astar_path, expanded = astar(grid, start, end)
        print(f"\nA*:     {len(astar_path)} steps, {expanded} expanded")
        if astar_path:
            print(grid.render(astar_path))

        # Dijkstra
        dijk_path, dists = dijkstra(grid, start, end)
        cost = dists.get(end, float("inf"))
        print(f"\nDijkstra: {len(dijk_path)} steps, cost={cost:.2f}")
        if dijk_path:
            print(grid.render(dijk_path))

    print("\n=== Algorithm comparison ===")
    print(f"{'Algorithm':12s} {'Path len':10s} {'Explored':10s} {'Optimal':8s}")
    grid  = Grid(MAP2)
    start = grid.find(START)
    end   = grid.find(END)

    bp, bv = bfs(grid, start, end)
    ap, ae = astar(grid, start, end)
    dp, dd = dijkstra(grid, start, end)

    print(f"{'BFS':12s} {len(bp):<10d} {len(bv):<10d} {'Yes'}")
    print(f"{'A*':12s} {len(ap):<10d} {ae:<10d} {'Yes'}")
    print(f"{'Dijkstra':12s} {len(dp):<10d} {len(dd):<10d} {'Yes'}")
