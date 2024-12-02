import itertools
from typing import Iterator

from aoc import read_input

reports = [[int(x) for x in line.split()] for line in read_input().splitlines()]


def is_safe(report: list[int]) -> bool:
    diffs = [b - a for a, b in itertools.pairwise(report)]
    return len(set(d > 0 for d in diffs)) == 1 and all(1 <= abs(d) <= 3 for d in diffs)


safe = sum(is_safe(r) for r in reports)
print("Part 1:", safe)


def shrink(report: list[int]) -> Iterator[list[int]]:
    yield report
    for i in range(len(report)):
        yield [x for j, x in enumerate(report) if j != i]


safe = sum(any(is_safe(s) for s in shrink(r)) for r in reports)
print("Part 2:", safe)
