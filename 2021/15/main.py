import heapq
import sys

with open("input.txt") as f:
    grid = [[int(x) for x in line] for line in f.read().splitlines()]

h, w = len(grid), len(grid[0])


def neighbours(x, y):
    for dy, dx in ((1, 0), (0, 1), (-1, 0), (0, -1)):
        j = y + dy
        i = x + dx
        if 0 <= j < h and 0 <= i < w:
            yield i, j, grid[j][i]


def lowest_risk(x0, y0):
    dist = {(x0, y0): 0}
    q = []

    for y in range(h):
        for x in range(w):
            v = x, y
            if v != (x0, y0):
                dist[v] = sys.maxsize
            heapq.heappush(q, (grid[y][x], v))

    while q:
        _, u = heapq.heappop(q)
        for x, y, d in neighbours(*u):
            v = x, y
            alt = dist[u] + d
            if alt < dist[v]:
                dist[v] = alt
                decrease_priority(q, v, alt)

    return dist[(w - 1, h - 1)]


def decrease_priority(q, item, p):
    for entry in q:
        if entry[1] == item:
            q.remove(entry)
            break
    heapq.heappush(q, (p, item))


print("Part 1:", lowest_risk(0, 0))

grid2 = [[0 for _ in range(w * 5)] for _ in range(h * 5)]
for j in range(5):
    for i in range(5):
        for y in range(h):
            for x in range(w):
                r = grid[y][x]
                for _ in range(i + j):
                    r = (r + 1) % 10 or 1
                grid2[j * h + y][i * w + x] = r
grid = grid2
h, w = len(grid), len(grid[0])
print("Part 2:", lowest_risk(0, 0))
