import math
from typing import Callable, NewType, Union

from aoc import DEBUG, read_input

Cell = NewType("Cell", str)
VOID = Cell(" ")
FREE = Cell(".")
WALL = Cell("#")

Map = list[list[Cell]]
Instr = Union[int, str]

Pos = tuple[int, int]
Dir = tuple[int, int]

DIRS = R, D, L, U = (1, 0), (0, 1), (-1, 0), (0, -1)


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

    dirs = {R: ">", D: "v", L: "<", U: "^"}
    for x, y, dx, dy in path:
        map[y][x] = dirs[(dx, dy)]  # type: ignore

    print("-" * 50)
    for row in map:
        print("".join(row))


State = tuple[int, int, int, int]
Wrapping = Callable[[int, int, int, int, int, int], State]


def wrap_flat(x: int, y: int, dx: int, dy: int, w: int, h: int) -> State:
    x = (x + dx) % w
    y = (y + dy) % h

    while map[y][x] == VOID:
        x = (x + dx) % w
        y = (y + dy) % h

    return x, y, dx, dy


class Cube:
    faces: list[Pos]
    edges: dict[int, dict[Dir, tuple[int, Dir]]]


class CubeSample(Cube):
    # ..1.
    # 234.
    # ..56
    faces = [(2, 0), (0, 1), (1, 1), (2, 1), (2, 2), (3, 2)]
    edges = {
        1: {R: (6, L), D: (4, D), L: (3, D), U: (2, D)},
        2: {R: (3, R), D: (5, U), L: (6, U), U: (1, D)},
        3: {R: (4, R), D: (5, R), L: (2, L), U: (1, R)},
        4: {R: (6, D), D: (5, D), L: (3, L), U: (1, U)},
        5: {R: (6, R), D: (2, U), L: (3, U), U: (4, U)},
        6: {R: (1, L), D: (2, R), L: (5, L), U: (4, L)},
    }


class CubeReal(Cube):
    # .12
    # .3.
    # 45.
    # 6..
    faces = [(1, 0), (2, 0), (1, 1), (0, 2), (1, 2), (0, 3)]
    edges = {
        1: {R: (2, R), D: (3, D), L: (4, R), U: (6, R)},
        2: {R: (5, L), D: (3, L), L: (1, L), U: (6, U)},
        3: {R: (2, U), D: (5, D), L: (4, D), U: (1, U)},
        4: {R: (5, R), D: (6, D), L: (1, R), U: (3, R)},
        5: {R: (2, L), D: (6, L), L: (4, L), U: (3, U)},
        6: {R: (5, U), D: (2, D), L: (1, D), U: (4, U)},
    }


def wrap_cube(x: int, y: int, dx: int, dy: int, w: int, h: int) -> State:
    x, y = x + dx, y + dy

    if 0 <= x < w and 0 <= y < h and map[y][x] != VOID:
        return x, y, dx, dy

    # We crossed an edge, so take a step back:
    x, y = x - dx, y - dy

    side = math.gcd(w, h)
    cube = CubeSample if side == 4 else CubeReal

    # Determine old face, new face, and new direction:
    u, v = x // side, y // side
    old_face, old_dir = cube.faces.index((u, v)) + 1, (dx, dy)
    new_face, new_dir = cube.edges[old_face][old_dir]

    # Transform coordinates to local (face) space:
    lx = x - (u * side)
    ly = y - (v * side)

    # Transform coordinates to new face:
    old_lx, old_ly = lx, ly
    s = side - 1
    ix = s - lx
    iy = s - ly
    lx, ly = {
        D: {D: (lx, 0), L: (s, lx), R: (0, lx), U: (ix, s)},
        L: {D: (ly, 0), L: (s, ly), R: (0, iy), U: (iy, s)},
        R: {D: (iy, 0), L: (s, iy), R: (0, ly), U: (ly, s)},
        U: {D: (ix, 0), L: (s, ix), R: (0, lx), U: (lx, s)},
    }[old_dir][new_dir]

    if DEBUG:
        old = old_face, "RDLU"[DIRS.index(old_dir)], (old_lx, old_ly)
        new = new_face, "RDLU"[DIRS.index(new_dir)], (lx, ly)
        print(*old, "->", *new)
        input(">>> ")

    # Transform coordinates to global (flat) space:
    u, v = cube.faces[new_face - 1]
    x = lx + (u * side)
    y = ly + (v * side)

    return x, y, *new_dir


def walk(map: Map, instr: list[Instr], wrap: Wrapping) -> int:
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
                nx, ny, ndx, ndy = wrap(x, y, dx, dy, w, h)

                if map[ny][nx] == WALL:
                    break

                x, y, dx, dy = nx, ny, ndx, ndy
                path.append((x, y, dx, dy))

                if DEBUG:
                    print_path(map, path)

    return 1000 * (y + 1) + 4 * (x + 1) + DIRS.index((dx, dy))


map, instr = parse_notes(read_input())
print("Part 1:", walk(map, instr, wrap_flat))
print("Part 2:", walk(map, instr, wrap_cube))
