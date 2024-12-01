from collections import deque
from copy import deepcopy
from dataclasses import dataclass
from math import prod
from operator import add, mul
from pathlib import Path
from typing import Callable


@dataclass
class Monkey:
    items: deque[int]
    op: Callable[[int, int], int]
    op_arg: str
    test_divisor: int
    if_true: int
    if_false: int
    inspected: int = 0


def parse(text: str) -> list[Monkey]:
    operators = {"+": add, "*": mul}
    monkeys = []
    for block in text.split("\n\n"):
        lines = (line.split(": ")[1] for line in block.splitlines()[1:])
        items = deque(int(x) for x in next(lines).split(", "))
        op_name, op_arg = next(lines).split(" ")[-2:]
        op = operators[op_name]
        test_divisor = int(next(lines).split(" ")[-1])
        if_true = int(next(lines).split(" ")[-1])
        if_false = int(next(lines).split(" ")[-1])
        m = Monkey(items, op, op_arg, test_divisor, if_true, if_false)
        monkeys.append(m)
    return monkeys


class Game:
    def __init__(self, monkeys: list[Monkey], divide_worry: bool = True):
        self.monkeys = monkeys
        self.divide_worry = divide_worry
        self.product_of_test_divisors = prod(m.test_divisor for m in self.monkeys)

    def turn(self, m: Monkey) -> None:
        while m.items:
            item = m.items.popleft()

            num = item if m.op_arg == "old" else int(m.op_arg)
            item = m.op(item, num)

            if self.divide_worry:
                item //= 3
            else:
                item %= self.product_of_test_divisors

            test = item % m.test_divisor == 0
            target = m.if_true if test else m.if_false

            self.monkeys[target].items.append(item)
            m.inspected += 1

    def play(self, rounds: int) -> int:
        for _ in range(rounds):
            for m in self.monkeys:
                self.turn(m)

        a, b = sorted(m.inspected for m in self.monkeys)[-2:]
        return a * b


text = Path("input.txt").read_text()
monkeys = parse(text)

print("Part 1:", Game(deepcopy(monkeys)).play(20))
print("Part 2:", Game(monkeys, divide_worry=False).play(10_000))
