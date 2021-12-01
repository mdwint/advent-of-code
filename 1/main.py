from typing import List


def main():
    with open("input.txt") as f:
        numbers = [int(x) for x in f.readlines()]

    # Part 1:
    # print(count_increasing(numbers))

    # Part 2:
    windows = [sum(numbers[i : i + 3]) for i in range(len(numbers) - 2)]
    print(count_increasing(windows))


def count_increasing(numbers: List[int]) -> int:
    num_increasing = 0
    prev, *tail = numbers
    for current in tail:
        if current > prev:
            num_increasing += 1
        prev = current
    return num_increasing


if __name__ == "__main__":
    main()
