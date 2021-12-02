def main():
    with open("input.txt") as f:
        lines = f.readlines()

    commands = [(cmd, int(x)) for cmd, x in (line.split() for line in lines)]
    h, d, a = 0, 0, 0

    for cmd, x in commands:
        if cmd == "forward":
            h += x
            d += a * x
        elif cmd == "down":
            a += x
        elif cmd == "up":
            a -= x

    print(h, "*", d, "=", h * d)


if __name__ == "__main__":
    main()
