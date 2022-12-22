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

R = (1, 0)
D = (0, 1)
L = (-1, 0)
U = (0, -1)


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
        if d == R:
            c = ">"
        elif d == D:
            c = "v"
        elif d == L:
            c = "<"
        elif d == U:
            c = "^"
        else:
            raise ValueError(d)
        map[y][x] = c  # type: ignore

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
    folds: dict[int, dict[Dir, tuple[int, Dir]]]


class CubeSample(Cube):
    # ..1.
    # 234.
    # ..56
    faces = [(2, 0), (0, 1), (1, 1), (2, 1), (2, 2), (3, 2)]
    folds = {
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
    folds = {
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

    x, y = x - dx, y - dy

    side = math.gcd(w, h)
    cube = CubeSample if side == 4 else CubeReal

    # Determine old face and direction:
    u, v = x // side, y // side
    old_face = cube.faces.index((u, v)) + 1
    old_dir = dx, dy

    # Transform coordinates to local (face) space:
    lx = x - (u * side)
    ly = y - (v * side)

    # Determine new face and direction:
    new_face, new_dir = cube.folds[old_face][old_dir]

    # Update local coordinates:
    old_lx, old_ly = lx, ly
    s = side - 1
    ix = s - lx
    iy = s - ly
    lx, ly = {
        (D, D): (lx, 0),
        (D, L): (s, lx),
        (D, R): (0, lx),
        (D, U): (ix, s),
        (L, D): (ly, 0),
        (L, L): (s, ly),
        (L, R): (0, iy),
        (L, U): (iy, s),
        (R, D): (iy, 0),
        (R, L): (s, iy),
        (R, R): (0, ly),
        (R, U): (ly, s),
        (U, D): (ix, 0),
        (U, L): (s, ix),
        (U, R): (0, lx),
        (U, U): (lx, s),
    }[(old_dir, new_dir)]

    if DEBUG:
        print(
            old_face,
            "RDLU"[[R, D, L, U].index(old_dir)],
            (old_lx, old_ly),
            "->",
            new_face,
            "RDLU"[[R, D, L, U].index(new_dir)],
            (lx, ly),
        )
        input(">>> ")

    # Transform coordinates to global (flat) space:
    u, v = cube.faces[new_face - 1]
    x = lx + (u * side)
    y = ly + (v * side)

    if map[y][x] != WALL:
        dx, dy = new_dir

    return x, y, dx, dy


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
                nx, ny, dx, dy = wrap(x, y, dx, dy, w, h)

                if map[ny][nx] == WALL:
                    break

                x, y = nx, ny
                path.append((x, y, dx, dy))

                if DEBUG:
                    print_path(map, path)

    return 1000 * (y + 1) + 4 * (x + 1) + [R, D, L, U].index((dx, dy))


map, instr = parse_notes(read_input())
print("Part 1:", walk(map, instr, wrap_flat))
print("Part 2:", walk(map, instr, wrap_cube))
