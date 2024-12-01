import itertools
from collections import Counter
from dataclasses import dataclass
from typing import List, Tuple


def main():
    with open("input.txt") as f:
        lines = f.read().splitlines()

    positions = [int(line.split(": ")[-1]) for line in lines]
    print("Part 1:", part1(positions))
    print("Part 2:", part2(positions))


@dataclass
class GameState:
    curr_player: int
    positions: List[int]
    scores: List[int]


def part1(positions, max_score=1000):
    s = GameState(0, list(positions), scores=[0, 0])
    die = itertools.cycle(range(1, 101))
    rolls = 0

    while all(s < max_score for s in s.scores):
        rolled = sum(next(die) for _ in range(3))
        rolls += 3
        i = s.curr_player
        new_pos = (s.positions[i] + rolled - 1) % 10 + 1
        s.positions[i] = new_pos
        s.scores[i] += new_pos
        s.curr_player = 1 - i

    return min(s.scores) * rolls


@dataclass(frozen=True)
class Universe:
    curr_player: int
    positions: Tuple[int, int]
    scores: Tuple[int, int]

    def split_off(self, curr_player: int, new_pos: int) -> "Universe":
        p1, p2 = self.positions
        s1, s2 = self.scores
        if curr_player == 0:
            pos = (new_pos, p2)
            scores = (s1 + new_pos, s2)
        else:
            pos = (p1, new_pos)
            scores = (s1, s2 + new_pos)
        return Universe(1 - curr_player, pos, scores)


def part2(positions, max_score=21):
    universes = {Universe(0, tuple(positions), scores=(0, 0)): 1}
    roll_outcomes = [sum(rolls) for rolls in itertools.product((1, 2, 3), repeat=3)]
    roll_stats = Counter(roll_outcomes).items()
    wins = [0, 0]

    while universes:
        u, universe_occurrence = universes.popitem()
        i = u.curr_player
        for rolled, roll_occurrence in roll_stats:
            new_pos = (u.positions[i] + rolled - 1) % 10 + 1
            s = u.split_off(i, new_pos)
            n = universe_occurrence * roll_occurrence
            if s.scores[i] >= max_score:
                wins[i] += n
            else:
                universes[s] = n

    return max(wins)


if __name__ == "__main__":
    main()
