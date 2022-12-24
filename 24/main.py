import math
from collections import defaultdict, deque
from dataclasses import dataclass
from functools import lru_cache

from aoc import DEBUG, read_input

Pos = tuple[int, int]
Map = dict[Pos, str]

L, R, U, D, S = (-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)


@dataclass
class Valley:
    w: int
    h: int
    bliz: Map
    start: Pos
    end: Pos

    def in_bounds(self, pos: Pos) -> bool:
        x, y = pos
        return (0 <= x < self.w and 0 <= y < self.h) or pos in (self.start, self.end)


def parse_map(text: str) -> Valley:
    map = {}
    for y, line in enumerate(text.splitlines()[1:-1]):
        for x, char in enumerate(line[1:-1]):
            if char != ".":
                map[(x, y)] = char

    w, h = x + 1, y + 1
    return Valley(w, h, map, start=(0, -1), end=(w - 1, h))


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
    period = math.lcm(v.w, v.h)

    @lru_cache(maxsize=None)
    def blizzards_at(time: int) -> Map:
        if time == 0:
            return v.bliz

        dirs = {"<": L, ">": R, "^": U, "v": D}

        new = defaultdict(list)
        for (x, y), chars in v.bliz.items():
            for char in chars:
                dx, dy = dirs[char]
                x = (x + dx * time) % v.w
                y = (y + dy * time) % v.h
                new[(x, y)].append(char)

        return {pos: "".join(sorted(chars)) for pos, chars in new.items()}

    todo = deque([(start, start_time)])
    seen = set()

    while todo:
        pos, time = todo.popleft()
        rel_time = time % period

        state = (pos, rel_time)
        if state in seen:
            continue
        seen.add(state)

        if pos == end:
            return time - 1

        bliz = blizzards_at(rel_time)
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
