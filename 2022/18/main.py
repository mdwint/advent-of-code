from collections import deque

from aoc import read_input

Pos = tuple[int, int, int]


def neighbours(pos: Pos) -> list[Pos]:
    x, y, z = pos
    deltas = ((-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1))
    return [(x + dx, y + dy, z + dz) for dx, dy, dz in deltas]


class FloodFill:
    def __init__(self, points: set[Pos]):
        self.points = points
        self.exterior_points: set[Pos] = set()
        self.interior_points: set[Pos] = set()
        self.max_coord = max(c for pos in points for c in pos)

    def reaches_exterior(self, start: Pos) -> bool:
        if start in self.exterior_points:
            return True

        if start in self.interior_points:
            return False

        todo = deque([start])
        seen = set()

        while todo:
            pos = todo.popleft()
            if pos in seen:
                continue
            seen.add(pos)

            if any(c > self.max_coord for c in pos):
                self.exterior_points.update(seen)
                return True

            for other in neighbours(pos):
                if other not in self.points:
                    todo.append(other)

        self.interior_points.update(seen)
        return False


scan = read_input().splitlines()
points: set[Pos] = {tuple(int(x) for x in line.split(",")) for line in scan}  # type: ignore

free_area = 0
exterior_area = 0
fill = FloodFill(points)

for pos in points:
    for other in neighbours(pos):
        if other not in points:
            free_area += 1
            if fill.reaches_exterior(other):
                exterior_area += 1

print("Part 1:", free_area)
print("Part 2:", exterior_area)
