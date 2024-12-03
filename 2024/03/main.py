import re

from aoc import read_input

text = read_input()

total = 0
for m in re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", text):
    total += int(m[0]) * int(m[1])
print("Part 1:", total)

enabled = True
total = 0
for m in re.findall(r"mul\((\d{1,3}),(\d{1,3})\)|(do\(\)|don't\(\))", text):
    if m[2] == "don't()":
        enabled = False
    elif m[2] == "do()":
        enabled = True
    elif enabled:
        total += int(m[0]) * int(m[1])
print("Part 2:", total)
