from copy import deepcopy
from itertools import pairwise
from pathlib import Path
from typing import Iterator, NewType

Material = NewType("Material", int)
ROCK = Material(1)
SAND = Material(2)

Pos = tuple[int, int]
Cave = dict[Pos, Material]

sand_src: Pos = (500, 0)


def line_segment(start: Pos, end: Pos) -> Iterator[Pos]:
    x1, y1 = start
    x2, y2 = end

    if x1 == x2:
        return ((x1, y) for y in range(min(y1, y2), max(y1, y2) + 1))

    if y1 == y2:
        return ((x, y1) for x in range(min(x1, x2), max(x1, x2) + 1))

    raise ValueError((start, end))


def build_cave(scan: list[str]) -> Cave:
    cave: Cave = {}
    for line in scan:
        points: Iterator[Pos] = (
            tuple(int(p) for p in part.split(",", 1))  # type: ignore
            for part in line.split(" -> ")
        )
        for start, end in pairwise(points):
            for pos in line_segment(start, end):
                cave[pos] = ROCK
    return cave


def print_cave(cave: Cave) -> None:
    sx, sy = sand_src

    xmin = min(x for x, _ in cave)
    xmax = max(x for x, _ in cave)
    assert xmin <= sx <= xmax

    ymin = sy
    ymax = max(y for _, y in cave)

    w = xmax - xmin + 1
    h = ymax - ymin + 1

    grid = [["." for _ in range(w)] for _ in range(h)]
    grid[sy - ymin][sx - xmin] = "+"

    chars = {ROCK: "#", SAND: "O"}
    for y in range(ymin, ymax + 1):
        for x in range(xmin, xmax + 1):
            if mat := cave.get((x, y)):
                grid[y - ymin][x - xmin] = chars[mat]

    for line in grid:
        print("".join(line))


def simulate_sand(cave: Cave, floor: bool = False) -> int:
    ymax = max(y for _, y in cave) + (2 if floor else 0)
    sand_at_rest = 0

    sx, sy = sand_src
    while sy < ymax:
        steps = ((sx, sy + 1), (sx - 1, sy + 1), (sx + 1, sy + 1), (sx, sy))
        new = next((pos for pos in steps if pos not in cave), None)
        if not new:
            # Sand hit the top, so the source is blocked
            assert floor
            break
        elif new == (sx, sy) or (floor and sy == ymax - 1):
            # Sand can't move and comes to rest
            cave[(sx, sy)] = SAND
            sand_at_rest += 1
            sx, sy = sand_src
        else:
            sx, sy = new

    # print_cave(cave)
    return sand_at_rest


def main():
    scan = Path("input.txt").read_text().splitlines()
    cave = build_cave(scan)
    print("Part 1:", simulate_sand(deepcopy(cave)))
    print("Part 2:", simulate_sand(cave, floor=True))


if __name__ == "__main__":
    main()
