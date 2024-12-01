def main():
    with open("input.txt") as f:
        grid = [[int(x) for x in row.strip()] for row in f]
    part1(grid)
    part2(grid)


def part1(grid):
    risk = sum(cell + 1 for _, _, cell in low_points(grid))
    print("Part 1:", risk)


def part2(grid):
    m, n = len(grid), len(grid[0])

    def fill(basin, y, x):
        if grid[y][x] == 9:
            return
        basin.add((y, x))
        for j, i in neighbours(y, x, m, n):
            if (j, i) not in basin:
                fill(basin, j, i)

    basin_sizes = []
    for y, x, _ in low_points(grid):
        basin = set()
        fill(basin, y, x)
        basin_sizes.append(len(basin))

    a, b, c = sorted(basin_sizes)[-3:]
    print("Part 2:", a * b * c)


def low_points(grid):
    m, n = len(grid), len(grid[0])
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            for j, i in neighbours(y, x, m, n):
                if grid[j][i] <= cell:
                    break
            else:
                yield y, x, cell


def neighbours(y, x, m, n):
    for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        j = y + dy
        i = x + dx
        if 0 <= j < m and 0 <= i < n:
            yield j, i


if __name__ == "__main__":
    main()
