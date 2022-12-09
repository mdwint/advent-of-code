from dataclasses import dataclass
from itertools import pairwise
from pathlib import Path

lines = Path("input.txt").read_text().splitlines()
moves = []
for line in lines:
    d, n = line.split()
    moves.append((d, int(n)))


@dataclass
class Point:
    x: int
    y: int

    def __sub__(self, other: "Point") -> "Point":
        x = self.x - other.x
        y = self.y - other.y
        return Point(x, y)


def print_grid(rope: list[Point], visited: set[tuple[int, int]]) -> None:
    w = max(6, *(p.x for p in rope), *(x for x, _ in visited))
    h = max(6, *(p.y for p in rope), *(y for _, y in visited))
    t = len(rope) - 1
    for y in range(-h, h + 1):
        for x in range(-w, w + 1):
            for i, p in enumerate(rope):
                if p.x == x and p.y == y:
                    char = "H" if i == 0 else ("T" if i == t else str(i))
                    break
            else:
                char = " " if (x, y) in visited else "."
            print(char, end="")
        print("")
    input(">")


def sign(x: int) -> int:
    return (1 if x > 0 else -1) if x else 0


def simulate(knots: int) -> int:
    rope = [Point(0, 0) for _ in range(knots)]
    visited = set()

    for d, n in moves:
        for _ in range(n):
            # print_grid(rope, visited)
            head = rope[0]

            if d == "L":
                head.x -= 1
            elif d == "R":
                head.x += 1
            elif d == "U":
                head.y -= 1
            elif d == "D":
                head.y += 1

            for head, tail in pairwise(rope):
                diff = head - tail
                if max(abs(diff.x), abs(diff.y)) > 1:
                    tail.x += sign(diff.x)
                    tail.y += sign(diff.y)

            visited.add((tail.x, tail.y))

    return len(visited)


print("Part 1:", simulate(2))
print("Part 2:", simulate(10))
