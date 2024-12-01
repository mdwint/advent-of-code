import ast
from functools import cmp_to_key
from pathlib import Path


def compare(a, b) -> int:
    t, u = type(a), type(b)

    if t is u is int:
        return a - b

    if t is u is list:
        for x, y in zip(a, b):
            if res := compare(x, y):
                return res
        return len(a) - len(b)

    if t is int and u is list:
        return compare([a], b)

    if t is list and u is int:
        return compare(a, [b])

    raise ValueError((a, b))


def main():
    text = Path("input.txt").read_text()
    pairs = [
        tuple(ast.literal_eval(line) for line in block.splitlines())
        for block in text.split("\n\n")
    ]

    s = sum(i for i, pair in enumerate(pairs, start=1) if compare(*pair) < 0)
    print("Part 1:", s)

    d1, d2 = [[2]], [[6]]
    packets = [d1, d2]
    for pair in pairs:
        packets.extend(pair)

    packets = sorted(packets, key=cmp_to_key(compare))
    i = packets.index(d1) + 1
    j = packets.index(d2) + 1
    print("Part 2:", i * j)


if __name__ == "__main__":
    main()
