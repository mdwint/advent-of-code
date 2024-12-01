from collections import defaultdict, deque
from itertools import count

from aoc import DEBUG, read_input

Pos = tuple[int, int]
Map = set[Pos]

N, S, W, E = (0, -1), (0, 1), (-1, 0), (1, 0)
NW, NE, SW, SE = (-1, -1), (1, -1), (-1, 1), (1, 1)
DIRS = N, S, W, E, NW, NE, SW, SE


def parse_map(text: str) -> Map:
    elves = set()
    for y, line in enumerate(text.splitlines()):
        for x, char in enumerate(line):
            if char == "#":
                elves.add((x, y))
    return elves


def print_map(elves: Map) -> None:
    xmin, xmax, ymin, ymax = rect(elves)
    for y in range(ymin, ymax + 1):
        for x in range(xmin, xmax + 1):
            char = "#" if (x, y) in elves else "."
            print(char, end="")
        print()
    input()


def rect(elves: Map) -> tuple[int, int, int, int]:
    xmin = min(x for x, _ in elves)
    xmax = max(x for x, _ in elves)
    ymin = min(y for _, y in elves)
    ymax = max(y for _, y in elves)
    return xmin, xmax, ymin, ymax


def rect_area(elves: Map) -> int:
    xmin, xmax, ymin, ymax = rect(elves)
    w = xmax - xmin + 1
    h = ymax - ymin + 1
    return w * h


def simulate(elves: Map, rounds: int = 0) -> int:
    dirs = deque([(N, NE, NW), (S, SE, SW), (W, NW, SW), (E, NE, SE)])

    if DEBUG:
        print("== Initial State ==")
        print_map(elves)

    for round in range(1, rounds + 1) if rounds else count(1):
        proposals: dict[Pos, Pos] = {}
        dest_counts: dict[Pos, int] = defaultdict(int)

        for x, y in elves:
            if not any((x + dx, y + dy) in elves for dx, dy in DIRS):
                continue

            for attempt in dirs:
                if not any((x + dx, y + dy) in elves for dx, dy in attempt):
                    dx, dy = attempt[0]
                    dest = (x + dx, y + dy)
                    proposals[(x, y)] = dest
                    dest_counts[dest] += 1
                    break

        new_elves = set()
        for elf in elves:
            new = proposals.get(elf)
            if not new or dest_counts[new] > 1:
                new = elf
            new_elves.add(new)

        if not rounds and new_elves == elves:
            return round

        elves = new_elves
        dirs.rotate(-1)

        if DEBUG:
            print(f"== End of Round {round} ==")
            print_map(elves)

    return rect_area(elves) - len(elves)


elves = parse_map(read_input())
print("Part 1:", simulate(elves, rounds=10))
print("Part 2:", simulate(elves))
