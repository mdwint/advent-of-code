from pathlib import Path

lines = Path("input.txt").read_text().splitlines()


def common_item(rucksack: str) -> str:
    n = len(rucksack) // 2
    (item,) = set(rucksack[:n]) & set(rucksack[n:])
    return item


def badge_item(a: str, b: str, c: str) -> str:
    (item,) = set(a) & set(b) & set(c)
    return item


def priority(item: str) -> int:
    start, offset = ("a", 1) if item.islower() else ("A", 27)
    return ord(item) - ord(start) + offset


s = sum(priority(common_item(rucksack)) for rucksack in lines)
print("Part 1:", s)

s = sum(priority(badge_item(*lines[i : i + 3])) for i in range(0, len(lines), 3))
print("Part 2:", s)
