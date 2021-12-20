import itertools


def main():
    with open("input.txt") as f:
        lines = f.read().splitlines()

    head, _, *lines = lines
    algo = [int(s == "#") for s in head]
    img = {
        (y, x): int(s == "#")
        for y, line in enumerate(lines)
        for x, s in enumerate(line)
    }
    show(img)

    print("Part 1:", compute(img, algo, 2))
    print("Part 2:", compute(img, algo, 50))


def compute(img: dict, algo: dict, n: int) -> int:
    for i in range(n):
        img = enhance(img, algo, fill=algo[0] and i % 2)
        if n <= 2:
            show(img)
    return sum(img.values())


offsets = list(itertools.product(range(-1, 2), repeat=2))


def enhance(img: dict, algo: dict, fill: int, pad: int = 3) -> dict:
    ymin, _ = min(img)
    ymax, _ = max(img)
    out = {}
    for y, x in itertools.product(range(ymin - pad - 1, ymax + pad + 2), repeat=2):
        key = "".join(str(img.get((y + j, x + i), fill)) for j, i in offsets)
        out[(y, x)] = algo[int(key, 2)]
    return out


def show(img: dict):
    yprev = min(y for y, _ in img)
    for (y, _), p in sorted(img.items()):
        print(end="\n" if y > yprev else "")
        print("#" if p else ".", end="")
        yprev = y
    print("\n")


if __name__ == "__main__":
    main()
