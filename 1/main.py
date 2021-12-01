from typing import List


def main():
    with open("input.txt") as f:
        numbers = [int(x) for x in f.readlines()]

    # Part 1:
    # print("Increasing:", count_increasing(numbers))

    # Part 2:
    windows = sum_sliding_windows(numbers)
    print("Increasing:", count_increasing(windows))


def sum_sliding_windows(numbers: List[int]) -> List[int]:
    n = len(numbers)
    sums = []

    for i in range(n):
        j = i + 3
        if j > n:
            break
        sums.append(sum(numbers[i:j]))

    return sums


def count_increasing(numbers: List[int]) -> int:
    prev, *tail = numbers
    num_increasing = 0

    print(prev, ": (N/A)")
    for current in tail:
        diff = current - prev
        print(current, ":", diff)
        if diff > 0:
            num_increasing += 1
        prev = current

    return num_increasing


if __name__ == "__main__":
    main()
