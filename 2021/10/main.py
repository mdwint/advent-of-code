OPEN = "([{<"
CLOSE = ")]}>"


def main():
    with open("input.txt") as f:
        lines = [line.strip() for line in f]
    part1(lines)
    part2(lines)


def part1(lines):
    SCORE = {")": 3, "]": 57, "}": 1197, ">": 25137}
    score = 0
    for line in lines:
        stack = []
        for c in line:
            if c in OPEN:
                stack.append(c)
            elif c in CLOSE:
                x = stack.pop()
                if OPEN.index(x) != CLOSE.index(c):
                    score += SCORE[c]
                    break
    print("Part 1:", score)


def part2(lines):
    scores = []
    for line in lines:
        stack = []
        for c in line:
            if c in OPEN:
                stack.append(c)
            elif c in CLOSE:
                x = stack.pop()
                if OPEN.index(x) != CLOSE.index(c):
                    break
        else:
            score = 0
            for c in reversed(stack):
                i = OPEN.index(c)
                score = score * 5 + i + 1
            if score:
                scores.append(score)

    score = sorted(scores)[len(scores) // 2]
    print("Part 2:", score)


if __name__ == "__main__":
    main()
