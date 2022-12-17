import sys
from copy import deepcopy
from itertools import cycle
from pathlib import Path
from typing import Iterable

DEBUG = len(sys.argv) > 1

ROCKS = [
    (("#", "#", "#", "#"),),
    (
        (".", "#", "."),
        ("#", "#", "#"),
        (".", "#", "."),
    ),
    (
        (".", ".", "#"),
        (".", ".", "#"),
        ("#", "#", "#"),
    ),
    (
        ("#",),
        ("#",),
        ("#",),
        ("#",),
    ),
    (
        ("#", "#"),
        ("#", "#"),
    ),
]

Row = list[str]
Img = list[Row]


def print_grid(grid: Img, y: int, sprite: Img) -> None:
    grid = deepcopy(grid)
    ghost = [[c.replace("#", "@") for c in row] for row in sprite]
    blit(y, ghost, grid)

    for row in reversed(grid):
        print("|" + "".join(row) + "|")
    print("+" + "-" * len(row) + "+")


def push(y: int, jet: str, sprite: Img, grid: Img) -> Img:
    ghost = deepcopy(sprite)
    h = len(ghost)

    if jet == ">":
        if all(ghost[y][-1] == "." for y in range(h)):
            for row in ghost:
                row.insert(0, row.pop())
    elif jet == "<":
        if all(ghost[y][0] == "." for y in range(h)):
            for row in ghost:
                row.append(row.pop(0))

    return sprite if collides(y, ghost, grid) else ghost


def collides(y: int, sprite: Img, grid: Img) -> bool:
    if y < 0:
        return True

    bg = grid[y : y + len(sprite)]
    for sprite_row, bg_row in zip(sprite, bg):
        for s, b in zip(sprite_row, bg_row):
            if s == b == "#":
                return True
    return False


def blit(y: int, sprite: Img, grid: Img) -> None:
    bg = grid[y : y + len(sprite)]
    for sprite_row, bg_row in zip(sprite, bg):
        for x, char in enumerate(sprite_row):
            if char != ".":
                bg_row[x] = char


def simulate(jets: Iterable[str], total_rocks: int, width: int = 7) -> int:
    rocks = cycle(ROCKS)
    jets = cycle(jets)
    grid: Img = []
    rocks_stopped = 0
    height = 0
    dy = 3

    for _ in range(dy):
        grid.append(["."] * width)

    while rocks_stopped < total_rocks:
        rock = next(rocks)

        for _ in range(height - len(grid) + dy + len(rock)):
            grid.append(["."] * width)

        sprite: Img = [
            ["."] * 2 + list(row) + (["."] * (width - len(row) - 2))
            for row in reversed(rock)
        ]

        for y in range(height + dy, -1, -1):
            jet = next(jets)
            sprite = push(y, jet, sprite, grid)

            if DEBUG:
                print_grid(grid, y, sprite)
                input(f"h={height} - {jet}")

            if collides(y - 1, sprite, grid):
                blit(y, sprite, grid)
                rocks_stopped += 1
                height = max(y + len(rock), height)
                break

    return height


jets = list(Path("input.txt").read_text().strip())
print("Part 1:", simulate(jets, total_rocks=2022))
