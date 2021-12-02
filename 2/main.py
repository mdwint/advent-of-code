def main():
    with open("input.txt") as f:
        lines = f.readlines()

    commands = [(cmd, int(x)) for cmd, x in (line.split() for line in lines)]
    horiz, depth, aim = 0, 0, 0

    for cmd, x in commands:
        if cmd == "forward":
            horiz += x
            depth += aim * x
        elif cmd == "down":
            aim += x
        elif cmd == "up":
            aim -= x

    print(horiz * depth)


if __name__ == "__main__":
    main()
