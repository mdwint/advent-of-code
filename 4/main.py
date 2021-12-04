from collections import Counter
from dataclasses import dataclass, field
from typing import Dict, Iterator, List, Tuple


def main():
    with open("input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    head, *tail = lines
    numbers_to_draw = [int(x) for x in head.split(",")]
    boards = list(parse_boards(tail))

    for number in numbers_to_draw:
        for board in list(boards):
            board.try_mark(number)
            if board.is_complete():
                score = board.calc_score(number)
                print(f"{board}\nScore: {score}\n")

                # Part 1:
                # return

                # Part 2:
                boards.remove(board)


Pos = Tuple[int, int]


@dataclass
class Board:
    rows: List[List[int]]
    marked: Dict[Pos, int] = field(default_factory=dict)

    def __iter__(self) -> Iterator[Tuple[Pos, int]]:
        return (
            ((y, x), num)
            for y, row in enumerate(self.rows)
            for x, num in enumerate(row)
        )

    def __str__(self):
        text = ""
        for y, row in enumerate(self.rows):
            for x, num in enumerate(row):
                c = "X" if (y, x) in self.marked else str(num)
                text += c.rjust(2) + " "
            text += "\n"
        return text

    def try_mark(self, number: int):
        for pos, num in self:
            if num == number:
                self.marked[pos] = num
                return

    def is_complete(self) -> bool:
        if not self.marked:
            return False

        _, h = Counter([y for (y, _) in self.marked]).most_common(1)[0]
        if h == len(self.rows):
            return True

        _, w = Counter([x for (_, x) in self.marked]).most_common(1)[0]
        if w == len(self.rows[0]):
            return True

        return False

    def calc_score(self, final: int) -> int:
        unmarked = (num for pos, num in self if pos not in self.marked)
        return sum(unmarked) * final


def parse_boards(lines: List[str]) -> Iterator[Board]:
    b = Board([])
    for line in lines:
        if line == "":
            if b.rows:
                yield b
                b = Board([])
        else:
            row = [int(x) for x in line.split()]
            b.rows.append(row)
    if b.rows:
        yield b


if __name__ == "__main__":
    main()
