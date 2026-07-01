from heapq import heappop, heappush

INF = 10**30

def grid_dijkstra(grid, start, cost_func, passable_func=None):
    """
    grid: list[str] or list[list]
    start: (sy, sx)
    cost_func: (y, x, ny, nx, grid) -> 移動コスト
               移動不可なら None を返してもよい
    passable_func: (y, x, grid) -> bool
    """
    H = len(grid)
    W = len(grid[0])
    dist = [[INF] * W for _ in range(H)]

    if passable_func is None:
        passable_func = lambda y, x, g: g[y][x] != "#"

    sy, sx = start
    dist[sy][sx] = 0
    pq = [(0, sy, sx)]

    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while pq:
        d, y, x = heappop(pq)
        if dist[y][x] < d:
            continue

        for dy, dx in dirs:
            ny, nx = y + dy, x + dx
            if not (0 <= ny < H and 0 <= nx < W):
                continue
            if not passable_func(ny, nx, grid):
                continue

            c = cost_func(y, x, ny, nx, grid)
            if c is None:
                continue

            nd = d + c
            if nd < dist[ny][nx]:
                dist[ny][nx] = nd
                heappush(pq, (nd, ny, nx))

    return dist

# === Sample AWC0094

H, W = map(int, input().split())
C = [input() for _ in range(H)]

start = goal = None
for y in range(H):
    for x in range(W):
        if C[y][x] == "S":
            start = (y, x)
        elif C[y][x] == "G":
            goal = (y, x)

def passable(y, x, grid):
    return grid[y][x] != "X"

def cost(y, x, ny, nx, grid):
    now = grid[y][x]
    nxt = grid[ny][nx]

    if nxt == "V":
        if now == "V":
            return 0
        return 2
    return 1

dist = grid_dijkstra(C, start, cost, passable)

gy, gx = goal
ans = dist[gy][gx]
print(ans if ans < INF else "NO")
