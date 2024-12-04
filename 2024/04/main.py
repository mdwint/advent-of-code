from itertools import product

from aoc import read_input

grid = tuple(tuple(line) for line in read_input().splitlines())
h, w = len(grid), len(grid[0])
dirs = tuple(d for d in product((1, 0, -1), repeat=2) if any(d))


def find(word: str) -> int:
    return sum(
        all(grid[y][x] == char for (y, x, char) in path)
        for pos, d in product(product(range(h), range(w)), dirs)
        if (path := make_path(word, *pos, *d))
    )


def make_path(word: str, sy: int, sx: int, dy: int, dx: int) -> list:
    path = []
    for i, char in enumerate(word):
        y = sy + i * dy
        x = sx + i * dx
        if not ((0 <= y < h) and (0 <= x < w)):
            return []
        path.append((y, x, char))
    return path


def find_x_mas() -> int:
    total = 0
    for pattern in ["M.M.A.S.S", "M.S.A.M.S", "S.M.A.S.M", "S.S.A.M.M"]:
        pat = list(list(pattern[i : i + 3]) for i in (0, 3, 6))
        total += sum(match(pat, *pos) for pos in product(range(h), range(w)))
    return total


def match(pat: list[list[str]], sy: int, sx: int) -> bool:
    for dy, dx in product(range(len(pat)), range(len(pat[0]))):
        src = pat[dy][dx]
        if src == ".":
            continue
        try:
            dst = grid[sy + dy][sx + dx]
        except IndexError:
            return False
        if src != dst:
            return False
    return True


print("Part 1:", find("XMAS"))
print("Part 2:", find_x_mas())
