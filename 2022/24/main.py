import math
from collections import defaultdict, deque
from dataclasses import InitVar, dataclass, field

from aoc import DEBUG, read_input

Pos = tuple[int, int]
Map = dict[Pos, str]

L, R, U, D, S = (-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)


@dataclass
class Valley:
    w: int
    h: int
    bliz: InitVar[Map]
    start: Pos
    end: Pos
    period: int = field(init=False)
    blizzards_at: dict[int, Map] = field(init=False)

    def __post_init__(self, bliz: Map):
        self.period = math.lcm(self.w, self.h)
        self.blizzards_at = {0: bliz}

        # Precompute blizzards at each time step:
        dirs = {"<": L, ">": R, "^": U, "v": D}
        for time in range(1, self.period):
            new = defaultdict(list)
            for (x, y), chars in bliz.items():
                for char in chars:
                    dx, dy = dirs[char]
                    x = (x + dx * time) % self.w
                    y = (y + dy * time) % self.h
                    new[(x, y)].append(char)

            b = {pos: "".join(sorted(chars)) for pos, chars in new.items()}
            self.blizzards_at[time] = b

    def in_bounds(self, pos: Pos) -> bool:
        x, y = pos
        return (0 <= x < self.w and 0 <= y < self.h) or pos in (self.start, self.end)


def parse_map(text: str) -> Valley:
    bliz = {}
    for y, line in enumerate(text.splitlines()[1:-1]):
        for x, char in enumerate(line[1:-1]):
            if char != ".":
                bliz[(x, y)] = char

    w, h = x + 1, y + 1
    return Valley(w, h, bliz, start=(0, -1), end=(w - 1, h))


def print_map(w: int, h: int, bliz: Map, pos: Pos) -> None:
    for y in range(h):
        for x in range(w):
            p = x, y
            chars = "E" if p == pos else bliz.get(p, ".")
            n = len(chars)
            print(chars if n == 1 else n, end="")
        print()
    input()


def shortest_path(v: Valley, start: Pos, end: Pos, start_time: int = 0) -> int:
    todo = deque([(start, start_time)])
    seen = set()

    while todo:
        pos, time = todo.popleft()
        rel_time = time % v.period

        state = (pos, rel_time)
        if state in seen:
            continue
        seen.add(state)

        if pos == end:
            return time - 1

        bliz = v.blizzards_at[rel_time]
        if DEBUG:
            print("Minute", time)
            print_map(v.w, v.h, bliz, pos)

        x, y = pos
        for new_pos in ((x + dx, y + dy) for dx, dy in (L, R, U, D, S)):
            if v.in_bounds(new_pos) and new_pos not in bliz:
                todo.append((new_pos, time + 1))

    raise Exception("No path found")


v = parse_map(read_input())

t1 = shortest_path(v, v.start, v.end)
print("Part 1:", t1)

t2 = shortest_path(v, v.end, v.start, t1)
t3 = shortest_path(v, v.start, v.end, t2)
print("Part 2:", t3)
