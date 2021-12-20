def main():
    with open("input.txt") as f:
        lines = f.read().splitlines()

    head, _, *lines = lines
    enhancement = [1 if s == "#" else 0 for s in head]
    img = {
        (y, x): 1 if s == "#" else 0
        for y, line in enumerate(lines)
        for x, s in enumerate(line)
    }
    show(img)

    lit = compute(2, img, enhancement)
    print("Part 1:", lit)

    lit = compute(50, img, enhancement)
    print("Part 2:", lit)


def compute(n: int, img: dict, enhancement: dict) -> int:
    for i in range(n):
        fill = 0 if not enhancement[0] or i % 2 == 0 else 1
        img = enhance(img, enhancement, fill)
        if n <= 2:
            show(img)
    return sum(img.values())


def enhance(img: dict, enhancement: dict, fill: int) -> dict:
    img = img.copy()
    min_y, min_x = min(img)
    max_y, max_x = max(img)
    pad = 1
    for y in range(min_y - pad, max_y + pad + 1):
        for x in range(min_x - pad, max_x + pad + 1):
            if (y, x) not in img:
                img[(y, x)] = fill

    out = {}
    for (y, x) in sorted(img):
        key = ""
        for j in range(-1, 1 + 1):
            for i in range(-1, 1 + 1):
                try:
                    key += str(img[(y + j, x + i)])
                except KeyError:
                    key += str(fill)
        index = int(key, 2)
        out[(y, x)] = enhancement[index]
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
