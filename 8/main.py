def main():
    with open("input.txt") as f:
        lines = list(f)
    part1(lines)
    part2(lines)


def part1(lines):
    answer = 0
    known_lengths = (2, 3, 4, 7)
    for line in lines:
        _, outputs = (part.split() for part in line.split(" | "))
        for o in outputs:
            if len(o) in known_lengths:
                answer += 1
    print("Part 1:", answer)


def part2(lines):
    """
    segment count -> digit(s)
    -------------------------
    2: 1
    3: 7
    4: 4
    5: 2, 3, 5
    6: 0, 6, 9
    7: 8
    """
    answer = 0
    known = {2: 1, 3: 7, 4: 4, 7: 8}
    for line in lines:
        signals, outputs = (
            [set(s) for s in side.split()] for side in line.split(" | ")
        )
        map = {}
        while len(map) < 10:
            for s in list(signals):
                n = len(s)
                if n in known:
                    # 1, 4, 7, 8
                    d = known[n]
                else:
                    try:
                        if n == 5:
                            # 2, 3, 5
                            if map[1] < s:
                                d = 3
                            elif len(map[4] & s) == 2:
                                d = 2
                            else:
                                d = 5
                        elif n == 6:
                            # 0, 6, 9
                            if not map[5] < s:
                                d = 0
                            elif map[1] < s:
                                d = 9
                            else:
                                d = 6
                    except KeyError:
                        continue
                map[d] = s
                signals.remove(s)
        digits = ""
        for o in outputs:
            for d, s in map.items():
                if o == s:
                    digits += str(d)
                    break
        answer += int(digits)
    print("Part 2:", answer)


if __name__ == "__main__":
    main()
