from copy import deepcopy
from itertools import cycle
from typing import Iterable

from aoc import DEBUG, read_input

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


def simulate(jets: Iterable[str], total_rocks: int) -> int:
    rocks_iter = cycle(ROCKS)
    jets_iter = cycle(enumerate(jets))

    grid: Img = []
    width = 7
    drop_height = 3

    rocks_stopped = 0
    height = 0
    height_skipped = 0

    cache: dict[tuple, tuple] = {}

    while rocks_stopped < total_rocks:
        rock = next(rocks_iter)

        for _ in range(height - len(grid) + len(rock) + drop_height):
            grid.append(["."] * width)

        sprite: Img = [
            ["."] * 2 + list(row) + (["."] * (width - len(row) - 2))
            for row in reversed(rock)
        ]

        for y in range(height + drop_height, -1, -1):
            jet_id, jet = next(jets_iter)
            sprite = push(y, jet, sprite, grid)

            if DEBUG:
                print_grid(grid, y, sprite)
                input(f"h={height} - {jet}")

            if collides(y - 1, sprite, grid):
                blit(y, sprite, grid)
                rocks_stopped += 1
                height = max(y + len(rock), height)

                grid_hash = "".join("".join(row) for row in grid[-50:])
                state = (rock, jet_id, grid_hash)
                if state in cache:
                    prev_rocks, prev_height = cache[state]

                    diff_rocks = rocks_stopped - prev_rocks
                    diff_height = height - prev_height
                    reps = (total_rocks - rocks_stopped) // diff_rocks

                    rocks_stopped += diff_rocks * reps
                    height_skipped += diff_height * reps
                else:
                    cache[state] = (rocks_stopped, height)

                break

    return height + height_skipped


jets = list(read_input())
print("Part 1:", simulate(jets, total_rocks=2022))
print("Part 2:", simulate(jets, total_rocks=1_000_000_000_000))
