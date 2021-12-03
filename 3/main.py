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
    oxygen = int(find_line(oxygen_crit, lines), 2)
    co2 = int(find_line(co2_crit, lines), 2)
    print(oxygen * co2)


Ranking = List[Tuple[str, int]]
BitCriteria = Callable[[Ranking], str]


def oxygen_crit(rank: Ranking) -> str:
    (bit, n), (_, m) = rank
    if n == m:
        bit = "1"
    return bit


def co2_crit(rank: Ranking) -> str:
    (_, n), (bit, m) = rank
    if n == m:
        bit = "0"
    return bit


def find_line(bit_crit: BitCriteria, lines: List[str]) -> str:
    for i in range(len(lines[0])):
        rank = count_ith_bits(i, lines)
        bit = bit_crit(rank) if len(rank) == 2 else rank[0][0]
        lines = [line for line in lines if line[i] == bit]
        if len(lines) == 1:
            return lines[0]
    raise ValueError("not found")


def most_common_bits(lines: List[str]) -> str:
    result = ""
    for i in range(len(lines[0])):
        result += count_ith_bits(i, lines)[0][0]
    return result


def count_ith_bits(i: int, lines: List[str]) -> Ranking:
    return Counter([line[i] for line in lines]).most_common(2)


def flip(bits: str) -> str:
    return bits.replace("0", "_").replace("1", "0").replace("_", "1")


if __name__ == "__main__":
    main()
