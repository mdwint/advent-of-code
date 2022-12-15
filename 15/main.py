from dataclasses import dataclass
from pathlib import Path
from typing import NewType

Cls = NewType("Cls", int)
SENSOR = Cls(1)
BEACON = Cls(2)
EXCLUDED = Cls(3)

Pos = tuple[int, int]
Map = dict[Pos, Cls]


@dataclass
class Report:
    sensors_and_beacons: list[tuple[Pos, Pos]]


def parse_report(lines: list[str]) -> Report:
    sensors_and_beacons = []
    for line in lines:
        parts = line.split()
        x1, y1, x2, y2 = (int(c.strip("xy=,:")) for c in parts[2:4] + parts[-2:])
        sensors_and_beacons.append(((x1, y1), (x2, y2)))
    return Report(sensors_and_beacons)


def print_map(r: Report, m: Map, pad: int = 4) -> None:
    xmin = min(x for x, _ in m)
    ymin = min(y for _, y in m)
    xmax = max(x for x, _ in m)
    ymax = max(y for _, y in m)
    w = xmax - xmin + 1
    h = ymax - ymin + 1

    # Zoom out factor:
    z = max(1, w // 80)

    b = 2 * pad
    chars = {SENSOR: "S", BEACON: "B", EXCLUDED: "#"}
    grid = [["." for _ in range(w // z + 1 + b)] for _ in range(h // z + 1 + b)]

    for (x, y), c in m.items():
        xx = (x - xmin) // z + pad
        yy = (y - ymin) // z + pad
        grid[yy][xx] = chars[c]

    for row in grid:
        print("".join(row))


def simulate(r: Report, check_row: int) -> Map:
    m: Map = {}

    for (sx, sy), (bx, by) in r.sensors_and_beacons:
        d = abs(sx - bx) + abs(sy - by)
        y1 = sy - d
        y2 = sy + d
        # for y in range(y1, y2 + 1):
        if y1 <= check_row <= y2:
            y = check_row
            u = d if y == sy else ((y - y1) if y < sy else (y2 - y))
            x1 = sx - u
            x2 = sx + u
            for x in range(x1, x2 + 1):
                m[(x, y)] = EXCLUDED

    for s, b in r.sensors_and_beacons:
        m[s] = SENSOR
        m[b] = BEACON

    return m


def main():
    # name, check_row, bound = "sample.txt", 10, 20
    name, check_row, bound = "input.txt", 2000000, 4000000
    lines = Path(name).read_text().splitlines()

    r = parse_report(lines)
    m = simulate(r, check_row)
    print_map(r, m)

    s = sum(char == EXCLUDED for (_, y), char in m.items() if y == check_row)
    print("Part 1:", s)

    # This solution is waaaay too slow... :(
    for y in range(bound):
        m = simulate(r, check_row=y)
        xs = [x for x in range(bound) if (x, y) not in m]
        if len(xs) == 1:
            x = xs[0]
            print("Part 2:", x * 4000000 + y)
            break


if __name__ == "__main__":
    main()
