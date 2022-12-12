from pathlib import Path

Pos = tuple[int, int]
Map = dict[Pos, int]


def parse_map(text: str) -> tuple[Map, Pos, Pos]:
    H: Map = {}
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
            H[pos] = ord(char) - ord("a")

    return H, start, end


def shortest_path(H: Map, start: Pos, end: Pos) -> list[Pos]:
    dist = {pos: len(H) for pos in H}
    dist[start] = 0

    todo = set(H)
    prev: dict[Pos, Pos] = {}

    while todo:
        _, u = min((dist[u], u) for u in todo)
        if u == end:
            break
        todo.remove(u)

        x, y = u
        neighbours = ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))
        reachable = (v for v in neighbours if v in H and H[v] <= H[u] + 1)
        for v in todo.intersection(reachable):
            alt = dist[u] + 1
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u

    path = []
    pos: Pos | None = end
    if pos in prev or pos == start:
        while pos:
            path.append(pos)
            pos = prev.get(pos)

    return list(reversed(path))


def print_path(H: Map, path: list[Pos]) -> None:
    w = max(x for x, _ in H) + 1
    h = max(y for _, y in H) + 1

    grid = [["." for _ in range(w)] for _ in range(h)]
    for x, y in path:
        grid[y][x] = "#"

    for row in grid:
        print("".join(row))


def main():
    text = Path("input.txt").read_text()
    H, start, end = parse_map(text)

    path = shortest_path(H, start, end)
    print("Part 1:", len(path) - 1)
    # print_path(H, path)

    # HACK: The low points on the left edge are good candidates,
    # but all others are pits we can't escape.
    lowest = (pos for pos, h in H.items() if h == 0 and pos[0] == 0)
    paths = (shortest_path(H, start, end) for start in lowest)
    print("Part 2:", min(len(p) for p in paths if p) - 1)


if __name__ == "__main__":
    main()
