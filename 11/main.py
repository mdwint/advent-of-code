import itertools

W, H = 10, 10


def main():
    with open("input.txt") as f:
        grid = [[int(x) for x in line.strip()] for line in f]

    display("Start", grid)
    flashes_total = 0
    for step in itertools.count(1):
        flashes_this_step = 0

        for y, row in enumerate(grid):
            for x, _ in enumerate(row):
                grid[y][x] += 1

        for y, row in enumerate(grid):
            for x, _ in enumerate(row):

                def try_flash(y, x):
                    nonlocal flashes_total
                    nonlocal flashes_this_step
                    if grid[y][x] > 9:
                        flashes_total += 1
                        flashes_this_step += 1
                        grid[y][x] = 0
                        for j, i in neighbours(y, x):
                            if grid[j][i] > 0:
                                grid[j][i] += 1
                                try_flash(j, i)

                try_flash(y, x)

        display(f"Step {step}", grid)
        if step == 100:
            print("Part 1:", flashes_total)
            # break
        if flashes_this_step == W * H:
            print("Part 2:", step)
            break


def neighbours(y, x):
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            if dy == dx == 0:
                continue
            j, i = y + dy, x + dx
            if 0 <= j < H and 0 <= i < W:
                yield j, i


def display(msg, grid):
    print(f"{msg}:\n" + "-" * 10)
    for line in grid:
        print("".join(str(x) for x in line))
    print()


if __name__ == "__main__":
    main()
