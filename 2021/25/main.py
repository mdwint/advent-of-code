import copy


def main():
    with open("input.txt") as f:
        lines = f.read().splitlines()

    grid = [[c for c in line] for line in lines]
    h, w = len(grid), len(grid[0])

    i = 0
    while True:
        moved = False
        step = copy.deepcopy(grid)
        for y in range(h):
            for x in range(w):
                x1 = (x + 1) % w
                if grid[y][x] == ">" and grid[y][x1] == ".":
                    step[y][x] = "."
                    step[y][x1] = ">"
                    moved = True
        grid = copy.deepcopy(step)
        for y in range(h):
            for x in range(w):
                y1 = (y + 1) % h
                if step[y][x] == "v" and step[y1][x] == ".":
                    grid[y][x] = "."
                    grid[y1][x] = "v"
                    moved = True
        i += 1
        if not moved:
            print(i)
            return


if __name__ == "__main__":
    main()
