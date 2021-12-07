def main():
    with open("input.txt") as f:
        xs = [int(x) for x in f.read().split(",")]

    a, b = min(xs), max(xs)
    fuel, x = min((sum(cost(abs(y - x)) for y in xs), x) for x in range(a, b + 1))
    print(fuel, "fuel for pos", x)


def cost(dist: int) -> int:
    # Part 1: return dist
    # Part 2:
    return dist * (dist + 1) // 2


if __name__ == "__main__":
    main()
