from pathlib import Path

lines = Path("input.txt").read_text().splitlines()
pairs = [[tuple(map(int, rng.split("-"))) for rng in line.split(",")] for line in lines]

s = sum(((a <= c and d <= b) or (c <= a and b <= d)) for ((a, b), (c, d)) in pairs)
print("Part 1:", s)

s = sum(((a <= c <= b) or (c <= a <= d)) for ((a, b), (c, d)) in pairs)
print("Part 2:", s)
