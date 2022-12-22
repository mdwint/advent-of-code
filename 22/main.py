from typing import NewType, Union

from aoc import DEBUG, read_input

Cell = NewType("Cell", str)
VOID = Cell(" ")
FREE = Cell(".")
WALL = Cell("#")

Map = list[list[Cell]]
Instr = Union[int, str]


def parse_notes(text: str) -> tuple[Map, list[Instr]]:
    grid, descr = text.split("\n\n")

    lines = grid.splitlines()
    width = max(len(line) for line in lines)
    map = []
    for line in lines:
        row = [Cell(char) for char in line]
        pad = [VOID for _ in range(width - len(row))]
        row.extend(pad)
        map.append(row)

    instr: list[Instr] = []
    numbers = []
    for char in descr:
        if char.isdigit():
            numbers.append(char)
        else:
            if numbers:
                instr.append(int("".join(numbers)))
                numbers.clear()
            instr.append(char)
    if numbers:
        instr.append(int("".join(numbers)))

    return map, instr


def print_path(map: Map, path: list[tuple[int, int, int, int]]) -> None:
    map = [row.copy() for row in map]
    for x, y, dx, dy in path:
        d = dx, dy
        if d == (1, 0):
            c = ">"
        elif d == (-1, 0):
            c = "<"
        elif d == (0, 1):
            c = "v"
        elif d == (0, -1):
            c = "^"
        else:
            c = "?"
        map[y][x] = c  # type: ignore
    for row in map:
        print("".join(row))


def walk(map: Map, instr: list[Instr]) -> int:
    w, h = len(map[0]), len(map)
    x, y = map[0].index(FREE), 0
    dx, dy = 1, 0

    path = [(x, y, dx, dy)]

    for move in instr:
        if move == "L":
            dx, dy = dy, -dx
            path.append((x, y, dx, dy))
        elif move == "R":
            dx, dy = -dy, dx
            path.append((x, y, dx, dy))
        elif isinstance(move, int):
            for _ in range(move):
                nx = (x + dx) % w
                ny = (y + dy) % h

                if map[ny][nx] == VOID:
                    nx = (nx - dx) % w
                    ny = (ny - dy) % h
                    while map[ny][nx] != VOID:
                        nx = (nx - dx) % w
                        ny = (ny - dy) % h
                    nx = (nx + dx) % w
                    ny = (ny + dy) % h
                assert map[ny][nx] != VOID

                if map[ny][nx] == WALL:
                    break

                x, y = nx, ny
                path.append((x, y, dx, dy))

    if DEBUG:
        print_path(map, path)

    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    return 1000 * (y + 1) + 4 * (x + 1) + dirs.index((dx, dy))


map, instr = parse_notes(read_input())
print("Part 1:", walk(map, instr))
