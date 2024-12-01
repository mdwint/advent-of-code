from itertools import count
from pathlib import Path

lines = Path("input.txt").read_text().splitlines()
program = iter(lines)

X = {1: 1}
deadline = -1

for cycle in count(start=1):
    if cycle < deadline:
        X[cycle] = X[cycle - 1]
        continue

    try:
        instr = next(program)
    except StopIteration:
        break

    x = X[cycle]

    if instr == "noop":
        deadline = cycle + 1
        X[deadline] = x
    else:
        n = int(instr.split()[1])
        deadline = cycle + 2
        X[deadline] = x + n

print("Part 1:", sum(X[c] * c for c in range(20, 220 + 1, 40)))

print("Part 2:")
width, height = 40, 6
for cycle in range(1, width * height + 1):
    x = X[cycle]
    pixel = (cycle - 1) % width
    lit = x - 1 <= pixel <= x + 1
    print("#" if lit else ".", end="")
    if pixel == width - 1:
        print()
