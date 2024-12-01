import copy
from pathlib import Path

text = Path("input.txt").read_text()
layout, procedure = text.split("\n\n")

layout_lines = layout.splitlines()[:-1]
num_stacks = len(layout_lines[-1]) // 4 + 1
stacks = [[] for _ in range(num_stacks)]

for line in reversed(layout_lines):
    for i in range(num_stacks):
        try:
            crate = line[(i * 4) + 1].strip()
        except IndexError:
            break
        if crate:
            stacks[i].append(crate)

moves = []
for line in procedure.splitlines():
    parts = line.split()
    count, a, b = (int(parts[i]) for i in (1, 3, 5))
    moves.append((count, a - 1, b - 1))


def move(stacks: list[list[str]], preserve_order: bool = False) -> str:
    for count, a, b in moves:
        s1, s2 = stacks[a], stacks[b]
        if preserve_order:
            s2.extend(s1[-count:])
            del s1[-count:]
        else:
            for _ in range(count):
                s2.append(s1.pop())

    return "".join(s[-1] for s in stacks)


print("Part 1:", move(copy.deepcopy(stacks)))
print("Part 2:", move(stacks, preserve_order=True))
