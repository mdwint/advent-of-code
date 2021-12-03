from collections import Counter
from typing import Callable, List, Tuple


def main():
    with open("input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    # part1(lines)
    part2(lines)


def part1(lines: List[str]):
    gamma_bin = most_common_bits(lines)
    gamma = int(gamma_bin, 2)

    epsilon_bin = flip(gamma_bin)
    epsilon = int(epsilon_bin, 2)

    print(gamma * epsilon)


def part2(lines: List[str]):
    oxygen = int(find_line(lambda zeros, ones: "1" if zeros <= ones else "0", lines), 2)
    co2 = int(find_line(lambda zeros, ones: "0" if zeros <= ones else "1", lines), 2)
    print(oxygen * co2)


BitCriteria = Callable[[int, int], str]


def find_line(bit_crit: BitCriteria, lines: List[str]) -> str:
    for i in range(len(lines[0])):
        zeros, ones = count_ith_bits(i, lines)
        bit = bit_crit(zeros, ones)
        lines = [line for line in lines if line[i] == bit]
        if len(lines) == 1:
            return lines[0]
    raise ValueError("not found")


def most_common_bits(lines: List[str]) -> str:
    result = ""
    for i in range(len(lines[0])):
        zeros, ones = count_ith_bits(i, lines)
        result += "0" if zeros > ones else "1"
    return result


def count_ith_bits(i: int, lines: List[str]) -> Tuple[int, int]:
    c = Counter([line[i] for line in lines])
    return c["0"], c["1"]


def flip(bits: str) -> str:
    return bits.replace("0", "_").replace("1", "0").replace("_", "1")


if __name__ == "__main__":
    main()
