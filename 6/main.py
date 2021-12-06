def main():
    with open("input.txt") as f:
        fish = [int(x) for line in f for x in line.split(",")]

    counts = [0] * 9
    for x in fish:
        counts[x] += 1
    print("Initial fish:", len(counts))

    days = 256  # 80

    for _ in range(days):
        zeros = counts[0]
        counts = counts[1:] + [zeros]
        counts[6] += zeros
    print("Total fish:", sum(counts))


if __name__ == "__main__":
    main()
