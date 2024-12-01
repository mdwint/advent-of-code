from pathlib import Path

text = Path("input.txt").read_text()
elves = [sum(int(x) for x in block.splitlines()) for block in text.split("\n\n")]
print("Part 1:", max(elves))
print("Part 2:", sum(sorted(elves)[-3:]))
