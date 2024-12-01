def main():
    with open("input.txt") as f:
        lines = [line.strip() for line in f]

    dots = set()
    folds = []

    parse_dots = True
    for line in lines:
        if line == "":
            parse_dots = False
            continue

        if parse_dots:
            dot = tuple(int(x) for x in line.split(","))
            dots.add(dot)
        else:
            axis, n = line.split()[-1].split("=")
            folds.append((axis, int(n)))

    for axis, n in folds:
        dim = 0 if axis == "x" else 1
        half = {dot for dot in dots if dot[dim] > n}
        dots = dots - half | {mirror(dot, dim, n) for dot in half}

        # print("Part 1:", len(dots))
        # return

    w = max(x for x, _ in dots) + 1
    h = max(y for _, y in dots) + 1

    grid = [[False for _ in range(w)] for _ in range(h)]
    for x, y in dots:
        grid[y][x] = True

    for row in grid:
        print("".join("#" if x else "." for x in row))


def mirror(dot, dim, n):
    x, y = dot
    if dim == 0:
        return n - (x - n), y
    return x, n - (y - n)


if __name__ == "__main__":
    main()
