from collections import Counter


def main():
    with open("input.txt") as f:
        lines = f.read().splitlines()

    template, _, *tail = lines
    rules = dict(line.split(" -> ") for line in tail)

    part1 = run(template, rules, 10)
    print("Part 1:", part1)

    part2 = run(template, rules, 40)
    print("Part 2", part2)


def run(template, rules, steps):
    elems = Counter(template)
    pairs = Counter()

    for i in range(len(template)):
        pair = template[i : i + 2]
        pairs[pair] += 1

    for _ in range(steps):
        tmp_pairs = Counter()
        for pair, n in pairs.items():
            if pair in rules:
                l, r = pair
                c = rules[pair]
                tmp_pairs[l + c] += n
                tmp_pairs[c + r] += n
                elems[c] += n
        pairs = tmp_pairs

    counts = elems.values()
    return max(counts) - min(counts)


if __name__ == "__main__":
    main()
