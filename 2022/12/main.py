from collections import deque
from pathlib import Path

Pos = tuple[int, int]
Map = dict[Pos, int]


def parse_map(text: str) -> tuple[Map, Pos, Pos]:
    hmap: Map = {}
    start = end = (-1, -1)

    for y, line in enumerate(text.splitlines()):
        for x, char in enumerate(line):
            pos = (x, y)
            if char == "S":
                start = pos
                char = "a"
            elif char == "E":
                end = pos
                char = "z"
            hmap[pos] = ord(char) - ord("a")

    return hmap, start, end


def shortest_path(hmap: Map, start: list[Pos], end: Pos) -> int:
    todo = deque((pos, 0) for pos in start)
    seen = set()

    while todo:
        pos, dist = todo.popleft()
        if pos in seen:
            continue
        seen.add(pos)

        if pos == end:
            return dist

        x, y = pos
        for new in (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1):
            if new in hmap and hmap[new] <= hmap[pos] + 1:
                todo.append((new, dist + 1))

    raise Exception("No path found")


def main():
    text = Path("input.txt").read_text()
    hmap, start, end = parse_map(text)

    print("Part 1:", shortest_path(hmap, [start], end))

    lowest = [pos for pos, h in hmap.items() if h == 0]
    print("Part 2:", shortest_path(hmap, lowest, end))


if __name__ == "__main__":
    main()
