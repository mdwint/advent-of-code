import argparse
from pathlib import Path

DEBUG = False

Pos = tuple[int, int, int]


def parse_points(text: str) -> set[Pos]:
    return {tuple(int(x) for x in line.split(",")) for line in text.splitlines()}  # type: ignore


def count_surface_area(points: set[Pos]) -> int:
    free_sides: set[tuple[Pos, Pos]] = set()

    for x, y, z in points:
        for dx, dy, dz in (
            (-1, 0, 0),
            (1, 0, 0),
            (0, -1, 0),
            (0, 1, 0),
            (0, 0, -1),
            (0, 0, 1),
        ):
            other = (x + dx, y + dy, z + dz)
            if other not in points:
                side = ((x, y, z), other)
                free_sides.add(tuple(sorted(side)))  # type: ignore

    return len(free_sides)


def main():
    global DEBUG
    p = argparse.ArgumentParser()
    p.add_argument("input", nargs="?", default="input.txt")
    p.add_argument("-d", "--debug", action="store_true")
    args = p.parse_args()
    DEBUG = args.debug

    text = Path(args.input).read_text().strip()
    points = parse_points(text)

    print("Part 1:", count_surface_area(points))
    print("Part 2:", 0)


if __name__ == "__main__":
    main()
