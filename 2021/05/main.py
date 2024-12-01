def main():
    with open("input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    segments = []
    w, h = 0, 0

    for line in lines:
        a, b = line.split(" -> ")
        x1, y1 = (int(x) for x in a.split(","))
        x2, y2 = (int(x) for x in b.split(","))
        w = max(w, x1 + 1, x2 + 1)
        h = max(h, y1 + 1, y2 + 1)
        segments.append(tuple(sorted([(x1, y1), (x2, y2)])))

    grid = [[0 for _ in range(w)] for _ in range(h)]

    for (x1, y1), (x2, y2) in segments:
        if x1 == x2 or y1 == y2:
            for y in range(y1, y2 + 1):
                for x in range(x1, x2 + 1):
                    grid[y][x] += 1
        else:
            # Part 1:
            # continue
            dy = 1 if y1 < y2 else -1
            y = y1
            for x in range(x1, x2 + 1):
                grid[y][x] += 1
                y += dy

    for row in grid:
        print("".join(str(n) if n else "." for n in row))

    answer = sum(1 for row in grid for n in row if n >= 2)
    print(answer)


if __name__ == "__main__":
    main()
