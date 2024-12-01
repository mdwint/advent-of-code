from pathlib import Path
from typing import Callable, Iterable

lines = Path("input.txt").read_text().splitlines()
H = [[int(x) for x in line] for line in lines]
n = len(H)


def visible(y: int, x: int) -> bool:
    h = H[y][x]
    N = (H[yy][x] for yy in range(n) if yy < y)
    E = (H[y][xx] for xx in range(n) if xx > x)
    S = (H[yy][x] for yy in range(n) if yy > y)
    W = (H[y][xx] for xx in range(n) if xx < x)
    return any(all(other < h for other in side) for side in (N, E, S, W))


def walk(xs: Iterable[int], stop: Callable[[int], bool]) -> int:
    steps = 0
    for x in xs:
        steps += 1
        if stop(x):
            break
    return steps


def scenic_score(y: int, x: int) -> int:
    h = H[y][x]
    a = walk(range(y, 0, -1), lambda yy: H[yy - 1][x] >= h)
    b = walk(range(x, 0, -1), lambda xx: H[y][xx - 1] >= h)
    c = walk(range(y, n - 1), lambda yy: H[yy + 1][x] >= h)
    d = walk(range(x, n - 1), lambda xx: H[y][xx + 1] >= h)
    return a * b * c * d


inner = [(y, x) for y in range(1, n - 1) for x in range(1, n - 1)]

print("Part 1:", sum(visible(y, x) for y, x in inner) + 4 * (n - 1))
print("Part 2:", max(scenic_score(y, x) for y, x in inner))
