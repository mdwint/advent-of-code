from collections import Counter, defaultdict


def main():
    with open("input.txt") as f:
        lines = list(f)

    adj = defaultdict(list)
    for line in lines:
        a, b = line.strip().split("-")
        for x, y in ((a, b), (b, a)):
            if x != "end" and y != "start":
                adj[x].append(y)

    # paths = part1(adj)
    paths = part2(adj)

    # for p in paths:
    #     print(",".join(p))
    print(len(paths))


def part1(adj):
    paths = [["start"]]
    for p in paths:
        a = p[-1]
        for b in adj[a]:
            if b.isupper() or b not in p:
                paths.append(p + [b])
    return [p for p in paths if p[-1] == "end"]


def part2(adj):
    seen = set()
    paths = [["start"]]
    for p in paths:
        a = p[-1]
        c = Counter([x for x in p if x.islower() and x not in ("start", "end")])
        ok_repeat = c and c.most_common(1)[0][1] < 2
        for b in adj[a]:
            if b.isupper() or b not in p or ok_repeat:
                q = p + [b]
                s = ",".join(q)
                if s not in seen:
                    paths.append(q)
                    seen.add(s)
    return [p for p in paths if p[-1] == "end"]


if __name__ == "__main__":
    main()
