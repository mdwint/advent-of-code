import argparse
from collections import deque
from pathlib import Path

DEBUG = False

Pos = tuple[int, int, int]


def neighbours(pos: Pos) -> list[Pos]:
    x, y, z = pos
    deltas = ((-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1))
    return [(x + dx, y + dy, z + dz) for dx, dy, dz in deltas]


def reaches_exterior(start: Pos, points: set[Pos], max_dist: int = 20) -> bool:
    todo = deque([start])
    seen = set()

    while todo:
        pos = todo.popleft()
        if pos in seen:
            continue
        seen.add(pos)

        if any(d >= max_dist for d in pos):
            return True

        for other in neighbours(pos):
            if other not in points:
                todo.append(other)

    return False


def main() -> None:
    global DEBUG
    p = argparse.ArgumentParser()
    p.add_argument("input", nargs="?", default="input.txt")
    p.add_argument("-d", "--debug", action="store_true")
    args = p.parse_args()
    DEBUG = args.debug

    scan = Path(args.input).read_text().splitlines()
    points: set[Pos] = {tuple(int(x) for x in line.split(",")) for line in scan}  # type: ignore

    free_area = 0
    exterior_area = 0

    for pos in points:
        for other in neighbours(pos):
            if other not in points:
                free_area += 1
                if reaches_exterior(other, points):
                    exterior_area += 1

    print("Part 1:", free_area)
    print("Part 2:", exterior_area)


if __name__ == "__main__":
    main()
