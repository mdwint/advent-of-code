import itertools
from collections import defaultdict

from aoc import read_input

top, bottom = read_input().split("\n\n")
rules = {tuple(int(x) for x in line.split("|")) for line in top.splitlines()}
updates = [[int(x) for x in line.split(",")] for line in bottom.splitlines()]

after = defaultdict(set)
before = defaultdict(set)
for a, b in rules:
    after[a].add(b)
    before[b].add(a)


def is_correctly_ordered(update: list[int]) -> bool:
    for i, x in enumerate(update):
        left, right = update[:i], update[i + 1 :]
        if after[x].intersection(left) or before[x].intersection(right):
            return False
    return True


def fix_order(update: list[int]) -> list[int]:
    while not is_correctly_ordered(update):
        for (i, x), (j, y) in itertools.product(enumerate(update), repeat=2):
            if i < j and (x in after[y] or y in before[x]):
                update[i], update[j] = y, x
                break
    return update


total = sum(u[len(u) // 2] for u in updates if is_correctly_ordered(u))
print("Part 1:", total)

fixed = [fix_order(u) for u in updates if not is_correctly_ordered(u)]
total = sum(u[len(u) // 2] for u in fixed)
print("Part 2:", total)
