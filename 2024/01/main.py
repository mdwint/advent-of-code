from aoc import read_input

text = read_input()
a, b = [], []

for line in text.splitlines():
    x, y = line.split()
    a.append(int(x))
    b.append(int(y))

total = sum(abs(x - y) for x, y in zip(sorted(a), sorted(b)))
print("Part 1:", total)

score = sum(x * b.count(x) for x in a)
print("Part 2:", score)
